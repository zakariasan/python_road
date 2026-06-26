#!/usr/bin/env bash
# ============================================================================
#  Codexion test harness
# ----------------------------------------------------------------------------
#  Thread scheduling is non-deterministic, so we validate INVARIANTS, not
#  byte-exact output. The few deterministic cases (1 coder, bad args) are
#  checked exactly.
#
#  Usage:
#     ./test_codexion.sh                 # functional tests only
#     ./test_codexion.sh --valgrind      # + memcheck (leaks)
#     ./test_codexion.sh --helgrind      # + race detection
#     ./test_codexion.sh --all           # everything
#
#  Tunables (env):
#     BIN=./codexion  TIMEOUT=10  TOL=80
#       BIN      path to the binary
#       TIMEOUT  per-run wall-clock limit in seconds (a hang => FAIL)
#       TOL      allowed slack in ms for timing assertions (OS jitter)
# ============================================================================

BIN="${BIN:-./codexion}"
TIMEOUT="${TIMEOUT:-10}"
TOL="${TOL:-80}"
WITH_VG=0
WITH_HG=0

for a in "$@"; do
	case "$a" in
		--valgrind) WITH_VG=1 ;;
		--helgrind) WITH_HG=1 ;;
		--all) WITH_VG=1; WITH_HG=1 ;;
		*) echo "unknown flag: $a"; exit 2 ;;
	esac
done

GREEN=$'\033[32m'; RED=$'\033[31m'; YEL=$'\033[33m'; DIM=$'\033[2m'; RST=$'\033[0m'
PASS=0; FAIL=0
OUT=""; RC=0; DUR=0

# ---------------------------------------------------------------------------
#  core runner: OUT=stdout+stderr, RC=exit code, DUR=duration(ms)
# ---------------------------------------------------------------------------
run() {
	local start end
	start=$(date +%s%N)
	OUT="$(timeout "$TIMEOUT" "$BIN" "$@" 2>&1)"
	RC=$?
	end=$(date +%s%N)
	DUR=$(( (end - start) / 1000000 ))
}

ok()   { PASS=$((PASS+1)); printf "  ${GREEN}PASS${RST} %s\n" "$1"; }
ko()   { FAIL=$((FAIL+1)); printf "  ${RED}FAIL${RST} %s\n" "$1";
         [ -n "$2" ] && printf "       ${DIM}%s${RST}\n" "$2"; }
hdr()  { printf "\n${YEL}== %s ==${RST}\n" "$1"; }
info() { printf "  ${DIM}input   : %s${RST}\n  ${DIM}expected: %s${RST}\n" "$1" "$2"; }

# ---------------------------------------------------------------------------
#  invariant checkers (operate on $OUT)
# ---------------------------------------------------------------------------

# every line must be:  <ms> <id> <known action>
check_format() {
	local bad
	bad="$(printf '%s\n' "$OUT" | grep -vE \
'^[0-9]+ [0-9]+ (has taken a dongle|is compiling|is debugging|is refactoring|burned out)$' \
		| grep -v '^$')"
	[ -z "$bad" ] && ok "log format valid" \
		|| ko "log format invalid" "offending: $(printf '%s' "$bad" | head -1)"
}

# timestamps never go backwards (output serialized under print_mutex)
check_monotonic() {
	local r
	r="$(printf '%s\n' "$OUT" | awk 'NF{if($1<prev){print "drop @"NR; bad=1} prev=$1}
		END{exit bad?1:0}')"
	[ -z "$r" ] && ok "timestamps monotonic" || ko "timestamps go backwards" "$r"
}

# per-coder cycle order: take,take,compiling,debugging,refactoring (repeat)
# "burned out" is terminal; truncation at sim end is allowed.
check_sequence() {
	local r
	r="$(printf '%s\n' "$OUT" | awk '
		function e(i,a,x){print "coder "i": got ["a"] expected "x; bad=1}
		NF{
			id=$2; act=$0; sub(/^[0-9]+ [0-9]+ /,"",act)
			if(act=="burned out"){term[id]=1; next}
			if(term[id]){print "coder "id": event after burnout"; bad=1; next}
			s=st[id]+0
			if(s==0){if(act=="has taken a dongle")st[id]=1; else e(id,act,"take#1")}
			else if(s==1){if(act=="has taken a dongle")st[id]=2; else e(id,act,"take#2")}
			else if(s==2){if(act=="is compiling")st[id]=3; else e(id,act,"compiling")}
			else if(s==3){if(act=="is debugging")st[id]=4; else e(id,act,"debugging")}
			else if(s==4){if(act=="is refactoring")st[id]=0; else e(id,act,"refactoring")}
		}
		END{exit bad?1:0}')"
	[ -z "$r" ] && ok "per-coder cycle order valid (2 dongles before each compile)" \
		|| ko "cycle order violated" "$(printf '%s' "$r" | head -1)"
}

# burnout (if any) appears exactly once and is the last line; nothing after it
check_burnout_last() {
	local n last
	n="$(printf '%s\n' "$OUT" | grep -c 'burned out')"
	if [ "$n" -eq 0 ]; then ok "no burnout in this run"; return; fi
	[ "$n" -eq 1 ] || { ko "multiple burnout lines ($n)"; return; }
	last="$(printf '%s\n' "$OUT" | grep -v '^$' | tail -1)"
	printf '%s' "$last" | grep -q 'burned out' \
		&& ok "burnout is the last line, no output after it" \
		|| ko "output appears after burnout" "last line: $last"
}

# burnout timestamp within [expect-TOL, expect+TOL] ms
check_burnout_time() {
	local expect ts lo hi
	expect="$1"
	ts="$(printf '%s\n' "$OUT" | grep 'burned out' | head -1 | awk '{print $1}')"
	[ -n "$ts" ] || { ko "expected a burnout, none happened"; return; }
	lo=$((expect - TOL)); hi=$((expect + TOL))
	[ "$ts" -ge "$lo" ] && [ "$ts" -le "$hi" ] \
		&& ok "burnout at ${ts}ms (expected ~${expect}ms ±${TOL})" \
		|| ko "burnout timing off: ${ts}ms" "expected ${expect}ms ±${TOL} -> [$lo,$hi]"
}

# completion: no burnout, exit 0, every coder compiled >= required
check_completion() {
	local n req r
	n="$1"; req="$2"
	printf '%s\n' "$OUT" | grep -q 'burned out' && { ko "unexpected burnout"; return; }
	[ "$RC" -eq 0 ] || { ko "exit code $RC (expected 0)"; return; }
	r="$(printf '%s\n' "$OUT" | awk -v n="$n" -v req="$req" '
		/ is compiling$/{c[$2]++}
		END{
			seen=0
			for(k in c){seen++; if(c[k]<req){print "coder "k" only "c[k]"/"req; bad=1}}
			if(seen<n){print "only "seen"/"n" coders compiled"; bad=1}
			exit bad?1:0}')"
	[ -z "$r" ] && ok "all $n coders reached $req compiles, clean exit" \
		|| ko "completion not satisfied" "$r"
}

check_no_hang()    { [ "$RC" -ne 124 ] && ok "no hang (ran ${DUR}ms)" \
		|| ko "HANG: killed after ${TIMEOUT}s"; }
check_fast_exit()  { [ "$DUR" -le "$1" ] && ok "exited fast (${DUR}ms <= $1)" \
		|| ko "slow exit ${DUR}ms (budget $1)"; }
check_exit()       { [ "$RC" -eq "$1" ] && ok "exit code = $1" \
		|| ko "exit code $RC (expected $1)"; }
check_has_burnout(){ printf '%s\n' "$OUT" | grep -q 'burned out' \
		&& ok "burnout occurred (as expected)" || ko "expected a burnout"; }

# ===========================================================================
#  PRE-FLIGHT
# ===========================================================================
if [ ! -x "$BIN" ]; then
	echo "${RED}error:${RST} binary '$BIN' not found/executable. Run 'make' first."
	exit 2
fi
echo "binary=$BIN  timeout=${TIMEOUT}s  tol=${TOL}ms  valgrind=$WITH_VG helgrind=$WITH_HG"

# ===========================================================================
#  1. ARGUMENT VALIDATION  (deterministic, exact)
# ===========================================================================
hdr "1. argument validation"

info "no args" "usage error, exit != 0"
run; check_exit 1

info "5 4 200 200 200 3 0 fifo (too few args)" "usage error, exit 1"
run 5 4 200 200 200 3 0; check_exit 1

info "0 800 200 200 200 3 0 fifo (zero coders)" "rejected, exit 1"
run 0 800 200 200 200 3 0 fifo; check_exit 1

info "-3 800 200 200 200 3 0 fifo (negative)" "rejected, exit 1"
run -3 800 200 200 200 3 0 fifo; check_exit 1

info "3 800 abc 200 200 3 0 fifo (non-number)" "rejected, exit 1"
run 3 800 abc 200 200 3 0 fifo; check_exit 1

info "3 800 200 200 200 3 0 banana (bad scheduler)" "rejected, exit 1"
run 3 800 200 200 200 3 0 banana; check_exit 1

info "3 800 200 200 200 3 0 FIFO (uppercase != fifo)" "rejected, exit 1"
run 3 800 200 200 200 3 0 FIFO; check_exit 1

# ===========================================================================
#  2. NORMAL RUNS  (everyone should finish, nobody burns out)
# ===========================================================================
hdr "2. normal completion (fifo)"
info "5 800 200 200 200 3 0 fifo" "no burnout, all 5 reach 3 compiles, exit 0"
run 5 800 200 200 200 3 0 fifo
check_no_hang; check_format; check_monotonic; check_sequence
check_burnout_last; check_completion 5 3

hdr "2b. normal completion (edf)"
info "4 800 200 100 100 3 50 edf" "no burnout, all 4 reach 3 compiles, exit 0"
run 4 800 200 100 100 3 50 edf
check_no_hang; check_format; check_monotonic; check_sequence
check_burnout_last; check_completion 4 3

hdr "2c. many compiles required"
info "3 1500 100 100 100 20 0 fifo" "all 3 reach 20 compiles, no burnout"
run 3 1500 100 100 100 20 0 fifo
check_no_hang; check_format; check_sequence; check_completion 3 20

# ===========================================================================
#  3. HARD BURNOUT
# ===========================================================================
hdr "3. hard burnout — burnout shorter than a compile"
info "5 80 200 200 200 3 100 fifo" "someone burns out ~80ms, exit 0, burnout last line"
run 5 80 200 200 200 3 100 fifo
check_no_hang; check_format; check_monotonic; check_sequence
check_burnout_last; check_burnout_time 80; check_exit 0

hdr "3b. extreme burnout (=1ms)"
info "4 1 200 200 200 3 0 fifo" "near-instant burnout (~1ms ±tol), no hang"
run 4 1 200 200 200 3 0 fifo
check_no_hang; check_format; check_burnout_last; check_has_burnout

hdr "3c. burnout vs huge compile must still exit FAST"
info "2 10 5000 200 200 3 100 fifo" "burnout ~10ms AND process exits quickly (interruptible sleep)"
run 2 10 5000 200 200 3 100 fifo
check_no_hang; check_burnout_last; check_burnout_time 10; check_fast_exit 300

# ===========================================================================
#  4. HARD COOLDOWN
# ===========================================================================
hdr "4. hard cooldown — dongle locked far longer than burnout"
info "2 200 50 50 50 5 100000 fifo" "1st compile ok, then cooldown starves -> burnout, no hang"
run 2 200 50 50 50 5 100000 fifo
check_no_hang; check_format; check_sequence; check_burnout_last; check_has_burnout

hdr "4b. cooldown = 0 (no cooldown)"
info "4 800 100 100 100 5 0 fifo" "fast turnover, all finish, no burnout"
run 4 800 100 100 100 5 0 fifo
check_no_hang; check_sequence; check_completion 4 5

hdr "4c. moderate cooldown still completes when feasible"
info "3 2000 100 100 100 4 150 edf" "cooldown small vs burnout -> all 3 finish"
run 3 2000 100 100 100 4 150 edf
check_no_hang; check_sequence; check_completion 3 4

# ===========================================================================
#  5. EDGE CASES
# ===========================================================================
hdr "5. single coder (1 dongle, can never compile -> must burn out)"
info "1 300 200 200 200 5 0 fifo" "burns out at ~300ms (no 2nd dongle), exit 0"
run 1 300 200 200 200 5 0 fifo
check_no_hang; check_format; check_burnout_last; check_burnout_time 300

hdr "5b. two coders, one shared pair of dongles"
info "2 800 100 100 100 4 0 edf" "both alternate, finish, no burnout"
run 2 800 100 100 100 4 0 edf
check_no_hang; check_sequence; check_completion 2 4

hdr "5c. all-zero work times (compile/debug/refactor = 0)"
info "3 1000 0 0 0 5 0 fifo" "spins through compiles instantly, completes, no hang"
run 3 1000 0 0 0 5 0 fifo
check_no_hang; check_format; check_completion 3 5

hdr "5d. compiles_required = 1 (minimal goal)"
info "4 800 100 100 100 1 0 fifo" "each compiles once, exit 0"
run 4 800 100 100 100 1 0 fifo
check_no_hang; check_sequence; check_completion 4 1

hdr "5e. larger herd"
info "20 1500 80 80 80 3 20 fifo" "20 coders, all reach 3 compiles or clean burnout, no hang"
run 20 1500 80 80 80 3 20 fifo
check_no_hang; check_format; check_monotonic; check_sequence; check_burnout_last

# ===========================================================================
#  6. MEMORY  (valgrind memcheck)  -- opt-in
# ===========================================================================
if [ "$WITH_VG" -eq 1 ]; then
	hdr "6. valgrind memcheck (leaks / invalid access)"
	for args in "5 800 200 200 200 3 0 fifo" "1 300 200 200 200 2 0 fifo" \
	            "3 80 200 200 200 9 100 fifo" "4 800 200 100 100 3 50 edf"; do
		info "$args" "0 bytes in use at exit, 0 errors"
		log="$(valgrind --leak-check=full --errors-for-leak-kinds=all \
			--error-exitcode=99 timeout "$TIMEOUT" "$BIN" $args 2>&1 >/dev/null)"
		rc=$?
		leak="$(printf '%s\n' "$log" | grep 'in use at exit' | head -1)"
		if [ "$rc" -ne 99 ] && printf '%s' "$leak" | grep -q '0 bytes'; then
			ok "clean [$args] ($leak)"
		else
			ko "memcheck issue [$args]" \
				"$(printf '%s\n' "$log" | grep -E 'ERROR SUMMARY|in use at exit' | head -2)"
		fi
	done
fi

# ===========================================================================
#  7. RACES  (helgrind)  -- opt-in
# ===========================================================================
if [ "$WITH_HG" -eq 1 ]; then
	hdr "7. helgrind (data races / lock-order)"
	for args in "4 800 200 100 100 3 100 fifo" "3 80 200 200 200 9 0 edf" \
	            "1 300 200 200 200 2 0 fifo"; do
		info "$args" "ERROR SUMMARY: 0 errors"
		log="$(valgrind --tool=helgrind --error-exitcode=99 \
			timeout "$TIMEOUT" "$BIN" $args 2>&1 >/dev/null)"
		rc=$?
		sum="$(printf '%s\n' "$log" | grep 'ERROR SUMMARY' | head -1)"
		if [ "$rc" -ne 99 ] && printf '%s' "$sum" | grep -q '0 errors'; then
			ok "race-free [$args]"
		else
			ko "helgrind issue [$args]" "$sum"
		fi
	done
fi

# ===========================================================================
#  SUMMARY
# ===========================================================================
printf "\n========================================\n"
printf "  ${GREEN}PASS=%d${RST}   ${RED}FAIL=%d${RST}\n" "$PASS" "$FAIL"
printf "========================================\n"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
