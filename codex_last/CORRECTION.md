# Codexion — Evaluation / Correction Sheet

Derived from the project subject (no official public sheet exists; Codexion is a
Philosophers variant on the 42 intranet). Use this for self-eval and defense.

Legend:  [ ] todo · [x] verified · run commands from the project root after `make`.

---

## 0. Preliminary / Disqualifiers (any "yes" => grade 0)
- [ ] Crash (segfault, bus error, double free) on any reasonable input
- [ ] Global variable present  → `grep -nE '^[a-zA-Z].*;' *.c` (inspect for globals)
- [ ] Memory leak  → see §6
- [ ] Norm error (if norminette is required for this C piscine variant)
- [ ] Does not compile with `-Wall -Wextra -Werror -pthread`
- [ ] Makefile relinks unnecessarily  → run `make` twice, 2nd says "Nothing to be done"

```
make re && make            # second make must NOT recompile
```

---

## 1. Mandatory functions only
- [ ] Only allowed externals used: pthread_create/join/mutex_*(init/lock/unlock/destroy),
      pthread_cond_*(init/wait/timedwait/broadcast/destroy), gettimeofday, usleep,
      write, malloc, free, printf, fprintf, strcmp, strlen, atoi, memset
- [ ] No libft, no other libs

```
nm -u codexion | sort -u        # inspect undefined (external) symbols
```

---

## 2. Arguments & parsing
- [ ] Takes exactly 8 args: coders burnout compile debug refactor compiles cooldown scheduler
- [ ] Rejects: wrong arg count, negatives, non-integers, scheduler != fifo|edf
- [ ] Coder count 0 rejected

```
./codexion                              # usage error, exit != 0
./codexion 0 800 200 200 200 3 0 fifo   # rejected
./codexion -3 800 200 200 200 3 0 fifo  # rejected
./codexion 3 800 x 200 200 3 0 fifo     # rejected
./codexion 3 800 200 200 200 3 0 BAD    # rejected
```

---

## 3. Core simulation rules
- [ ] Each coder is a thread (pthread_create)
- [ ] N coders => N dongles; compiling needs 2 dongles (left + right)
- [ ] Each dongle protected by a mutex
- [ ] State logs exactly: "<ms> X has taken a dongle | is compiling | is debugging |
      is refactoring | burned out"
- [ ] Each "is compiling" preceded by TWO "has taken a dongle" (for N>1)
- [ ] Logs never interleave on a line (print mutex)
- [ ] Single coder: only 1 dongle => can never compile => must burn out

```
./codexion 5 800 200 200 200 3 0 fifo | head        # eyeball format
./codexion 1 300 200 200 200 5 0 fifo               # burns out ~300ms
```

---

## 4. Burnout / Monitor (precision <= 10ms)
- [ ] Separate monitor thread detects burnout
- [ ] "burned out" printed within 10ms of the actual deadline
- [ ] "burned out" is the LAST line; nothing prints after it
- [ ] Deadline rule: last_compile_START + time_to_burnout (NOT +compile)

```
./codexion 2 10 5000 200 200 3 100 fifo    # burnout ~10ms AND exits fast
./codexion 2 250 100 100 100 5 0 fifo      # cycle 300>250 => MUST burn out
```

---

## 5. Scheduling, cooldown, fairness
- [ ] fifo: dongle granted in request-arrival order
- [ ] edf: granted to earliest deadline (tie-break deterministic)
- [ ] Cooldown enforced: dongle unavailable for `dongle_cooldown` ms after release
- [ ] EDF liveness: no starvation when params feasible
- [ ] Priority queue / heap implemented by hand (no std priority queue)

```
./codexion 4 800 200 100 100 3 50 edf      # runs, completes
./codexion 2 200 50 50 50 5 100000 fifo    # huge cooldown => burnout, no hang
```

> Note in this implementation: the "heap" is a per-dongle 2-slot priority
> queue (a dongle only ever has <=2 waiters). Be ready to justify this design
> choice vs. a global N-ary heap during defense.

---

## 6. Memory (no leaks)
- [ ] 0 bytes in use at exit, every run path (complete, burnout, 1-coder, edf)

```
valgrind --leak-check=full ./codexion 5 800 200 200 200 3 0 fifo
valgrind --leak-check=full ./codexion 1 300 200 200 200 2 0 fifo
valgrind --leak-check=full ./codexion 3 100 200 200 200 9 100 fifo
```

---

## 7. Concurrency correctness (no races / deadlock)
- [ ] No data races (ThreadSanitizer is the authority)
- [ ] No deadlock / no hang on any feasible input
- [ ] Helgrind clean (use suppression for the known glibc condvar false positive)

```
# ThreadSanitizer (most accurate):
cc -Wall -Wextra -Werror -pthread -fsanitize=thread -g *.c -o cx_tsan
./cx_tsan 200 800 200 200 200 3 100 edf      # expect 0 warnings

# Helgrind (use suppression file for glibc>=2.34 internal-signal noise):
valgrind --tool=helgrind --suppressions=helgrind.supp ./codexion 4 800 200 100 100 3 100 fifo
```

> The helgrind "associated lock is not held by calling thread" inside
> pthread_cond_timedwait is a glibc-internal false positive — TSan confirms
> 0 races. See helgrind.supp for the explanation.

---

## 8. README requirements
- [ ] First line italic: *This project has been created as part of the 42 curriculum by <login>.*
- [ ] Description section
- [ ] Instructions (compile/run) section
- [ ] Resources section (refs + how AI was used)
- [ ] "Blocking cases handled" section (deadlock/Coffman, starvation, cooldown,
      burnout precision, log serialization)
- [ ] "Thread synchronization mechanisms" section (mutex, cond, monitor coord)

---

## 9. Defense recode readiness (be ready to modify live)
Practice these quick changes — typical recode asks:
- [ ] Change a log message / add a new state
- [ ] Switch a tie-break rule in EDF
- [ ] Add a field to a struct and use it
- [ ] Change cooldown semantics

---

## One-shot self-test
```
make && ./test_codexion.sh --all      # functional + memcheck + helgrind
```
Expect: PASS=N, FAIL=0.
```
