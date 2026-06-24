_This project has been created as part of the 42 curriculum by zhaouzan._

# Codexion

## Description

Codexion is a concurrency simulation built with POSIX threads. It models a group
of **coders** working in a shared hub, competing for a limited number of **USB
dongles**. Each coder repeatedly **compiles**, **debugs**, and **refactors**.
Compiling requires holding **two dongles at once** (a left and a right one). If a
coder waits too long between compiles, it **burns out** and the simulation stops.
The simulation also stops successfully once every coder has compiled a required
number of times.

The project is a variant of the classic Dining Philosophers problem, with two
added constraints: a **cooldown** on each dongle after it is released, and a
configurable **scheduling policy** (FIFO or EDF) that decides which waiting coder
is served next when several compete for the same dongle. A dedicated **monitor**
thread watches every coder and detects burnout precisely.

## Instructions

Compile with the provided Makefile:

```
make        # builds ./codexion
make clean  # removes object files
make fclean # removes objects and the binary
make re     # fclean + make
```

The program is compiled with `-Wall -Wextra -Werror -pthread`.

Run it with eight mandatory arguments:

```
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug \
           time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

- `number_of_coders` — number of coders (and dongles).
- `time_to_burnout` (ms) — if a coder does not start a new compile within this
  time since its last compile (or the start), it burns out.
- `time_to_compile` (ms) — time spent compiling (two dongles held).
- `time_to_debug` (ms) — time spent debugging.
- `time_to_refactor` (ms) — time spent refactoring.
- `number_of_compiles_required` — once every coder reaches this count, the
  simulation ends successfully.
- `dongle_cooldown` (ms) — after release, a dongle cannot be retaken until this
  time has passed.
- `scheduler` — `fifo` or `edf`.

Example:

```
./codexion 3 800 100 50 50 2 10 edf
./codexion 1 200 100 50 50 3 10 edf      # single coder: burns out, cannot compile
```

State changes are logged as `timestamp_in_ms coder_id action`, with output
serialized so messages never interleave.

## Blocking cases handled

**Deadlock prevention (Coffman conditions).** A deadlock needs four conditions to
hold at once: mutual exclusion, hold-and-wait, no preemption, and circular wait.
Codexion breaks the **circular wait** condition through a fixed global lock
order: every coder acquires its two dongles in ascending dongle-id order (lowest
first), computed once in `get_order`. Because all coders follow the same order,
the cycle of "each holds one and waits for the next" can never form — at least
one coder always reaches for its dongles in the opposite direction.

**Starvation prevention / fair arbitration.** Each dongle owns a priority queue
that decides who is served next. Under FIFO the earliest arrival wins; under EDF
the earliest deadline wins, with the lower coder id as a deterministic
tie-breaker. A coder is only granted a dongle when it is the top-priority waiter,
so no coder is indefinitely overtaken.

**Cooldown handling.** After a dongle is released, its release timestamp is
recorded. A waiting coder may only acquire it once `dongle_cooldown` milliseconds
have elapsed since that release. When the cooldown is the only thing blocking an
otherwise-eligible coder, it sleeps precisely until the cooldown expires rather
than polling.

**Precise burnout detection.** A separate monitor thread tracks every coder's
deadline (`last_compile_start + time_to_burnout`). It polls on a short interval
and declares the first coder past its deadline as burned out, logging it well
within the required 10 ms window.

**Clean termination.** The simulation ends on exactly one of two events: every
coder has compiled the required number of times (success), or a coder burns out
(failure). On either event the monitor sets a shared `over` flag and wakes every
coder blocked on a dongle, so all threads observe the end, leave their queues,
and join cleanly with no hang and no leaked memory.

**Log serialization.** All output passes through a single print mutex, so two
state messages never interleave on one line.

## Thread synchronization mechanisms

**Primitives used.** The project uses `pthread_mutex_t` and `pthread_cond_t`
only (no global variables). Each dongle has its own mutex and condition variable;
the hub has an `over_mutex` guarding the shared `over` flag and the coders'
`deadline`/`counter` fields, and a `print_mutex` serializing output.

**Per-dongle mutex + condition variable.** A dongle's mutex protects its state
(`owner`, `released`, and its waiting queue). A coder acquiring a dongle holds
this mutex while it checks whether it may take the dongle and while it waits, so
the check-and-wait is atomic. The condition variable lets a waiting coder sleep
instead of busy-looping; on release, the holder broadcasts to wake all waiters so
the top-priority one can proceed.

**Avoiding lost wakeups.** Waiting always uses the pattern "hold the mutex, check
the condition in a loop, and wait with the mutex held." `pthread_cond_wait` and
`pthread_cond_timedwait` release the mutex only while actually sleeping and
re-acquire it on waking. This closes the race where a release could happen in the
gap between a coder's check and its sleep. After every wake the coder re-checks
the real state rather than trusting the wakeup, which also handles spurious
wakeups. The project uses `pthread_cond_broadcast` (not signal) so no waiter is
ever left behind.

**Coder–monitor communication.** Coders and the monitor share state through the
hub under `over_mutex`. A coder updates its `deadline` and `counter` under this
mutex when it compiles; the monitor reads those same fields under the same mutex
(in `find_burned` and `all_done`). Because every read and every write of a shared
field goes through the one common lock, there is no data race between coders and
the monitor. The monitor's main loop itself holds no lock — each of its helpers
takes `over_mutex` only briefly — so the monitor never blocks the coders while it
runs.

**Lock ordering safety.** `over_mutex` and the dongle mutexes are never held
nested: a coder takes `over_mutex` only when it holds no dongle mutex, the monitor
takes only `over_mutex`, and the shutdown wake takes only dongle mutexes. With no
lock-ordering cycle, the added synchronization cannot itself introduce a deadlock.

## Resources

- The Dining Philosophers problem (Dijkstra) — classic reference for resource
  sharing, deadlock, and starvation.
- POSIX Threads documentation — `man pthread_create`, `pthread_mutex_lock`,
  `pthread_cond_wait`, `pthread_cond_timedwait`, `pthread_cond_broadcast`.
- Coffman's four conditions for deadlock.
- Binary heap / priority queue — standard data-structures reference for the
  FIFO/EDF arbitration queue.

**Use of AI.** AI was used as a reviewer and debugging aid, not a code generator:
to reason through data races surfaced by Helgrind/ThreadSanitizer, to explain
the behavior of the pthreads primitives, to refactor long functions into smaller
named helpers, and to verify the priority-queue logic in isolation. All code was
reviewed, tested, and understood before being kept.
