# 🧩 Codexion — Architecture & Synchronization Map

![language](https://img.shields.io/badge/language-C-blue)
![threads](https://img.shields.io/badge/pthreads-mutex%20%2B%20cond-informational)
![norminette](https://img.shields.io/badge/norminette-OK-success)
![helgrind](https://img.shields.io/badge/helgrind-0%20errors-success)
![tsan](https://img.shields.io/badge/ThreadSanitizer-0%20warnings-success)
![valgrind](https://img.shields.io/badge/valgrind-0%20leaks-success)

> A visual deep-dive into **every part** of the project: the threads, the data,
> and **every mutex / condition variable** — where it lives and **why**.

---

## 📑 Table of contents
1. [Big picture](#1--big-picture--threads--shared-state)
2. [The circular table](#2--the-circular-table)
3. [The three lock families](#3--the-three-lock-families)
4. [A coder's life](#4--a-coders-life)
5. [Dongle acquisition](#5--dongle-acquisition--arbitration--cooldown)
6. [The monitor](#6--the-monitor)
7. [Deadlock prevention](#7--deadlock-prevention)
8. [Shutdown](#8--shutdown)
9. [File & function map](#9--file--function-map)
10. [What was done](#10--summary--what-was-done)

---

## 1. 🗺️ Big picture — threads & shared state

```mermaid
flowchart TD
    subgraph HUB["🧠 t_hub (one shared struct)"]
        OVER["over flag<br/>over_mutex + over_cond"]:::lock
        PRINT["print_mutex → stdout"]:::lock
        ARR["coders[]  •  dongles[]  •  params"]:::data
    end

    MON["🩺 MONITOR thread<br/>monitor_routine"]:::mon
    C["🧵 CODER threads × N<br/>coder_routine"]:::coder
    D["🔌 DONGLES × N<br/>each: mutex + cond + queue[2]"]:::dongle

    MON -->|"reads deadlines/counters<br/>sets over, broadcasts"| OVER
    C -->|"write deadline/counter<br/>signal on compile"| OVER
    C -->|"serialized logs"| PRINT
    C <-->|"acquire / release"| D
    MON -->|"wake_all_dongles on stop"| D

    classDef mon fill:#fde68a,stroke:#d97706,color:#111
    classDef coder fill:#bfdbfe,stroke:#2563eb,color:#111
    classDef dongle fill:#bbf7d0,stroke:#16a34a,color:#111
    classDef lock fill:#fecaca,stroke:#dc2626,color:#111
    classDef data fill:#e9d5ff,stroke:#7c3aed,color:#111
```

> **Key idea:** `1 monitor + N coders`. **No** global server, **no** polling manager.
> Each dongle arbitrates its own (at most 2) waiters.

---

## 2. ⭕ The circular table

```mermaid
flowchart LR
    C1((Coder 1)):::coder ---|d0| C2((Coder 2)):::coder
    C2 ---|d1| C3((Coder 3)):::coder
    C3 ---|d2| C4((Coder 4)):::coder
    C4 ---|d3 ⤵ wraps to d0| C1

    classDef coder fill:#bfdbfe,stroke:#2563eb,color:#111
```

```c
/* init_coder():  dongles[i].id = i + 1 */
coder->right = &hub->dongles[id - 1];
coder->left  = &hub->dongles[id % hub->num_coders];
```

> 🔑 **`dongle[k]` is shared by EXACTLY 2 neighbours** (left of coder k, right of coder k+1).
> So a dongle can **never** have more than 2 waiters → a **2-slot queue is provably enough**.

---

## 3. 🔒 The three lock families

| 🔐 Lock | 📄 File | 🛡️ Protects | ❓ Why it exists |
|---|---|---|---|
| 🟢 `dongle->mutex` + `cond` | `dongles.c` | `owner`, `released`, `queue[2]` | Two neighbours grab the same dongle → must be exclusive *(subject: "protect each dongle with a mutex")*. Cond = wait for availability / cooldown. |
| 🔴 `over_mutex` + `over_cond` | `ft_over.c` / `monitor.c` | `over`, every `deadline`, every `counter` | Monitor **reads** deadlines/counters while coders **write** them. Cond = monitor sleeps to nearest deadline; coders sleep phases but wake instantly on `over`. |
| 🟡 `print_mutex` | `logtime.c` | `stdout` | *Subject: "two messages never interleave on a line."* |

---

## 4. 🧵 A coder's life

```mermaid
flowchart TD
    S([start]):::se --> O{over?}:::dec
    O -- yes --> X([exit]):::se
    O -- no --> T["take_dongles()<br/>🔌 lock first then second (lower id first)"]:::coder
    T --> L1["📝 'has taken a dongle' ×2<br/>(print_mutex)"]:::log
    L1 --> CT["compile_time()<br/>🔴 set deadline + signal"]:::lock
    CT --> L2["📝 'is compiling'"]:::log
    L2 --> CNT["counter++<br/>🔴 (after the log!) + signal"]:::lock
    CNT --> SC["💤 u_sleep(compile)"]:::sleep
    SC --> R["🔌 release both (broadcast cond)"]:::dongle
    R --> L3["📝 'is debugging' → 💤 u_sleep(debug)"]:::log
    L3 --> L4["📝 'is refactoring' → 💤 u_sleep(refactor)"]:::log
    L4 --> O

    classDef se fill:#e5e7eb,stroke:#6b7280,color:#111
    classDef dec fill:#fde68a,stroke:#d97706,color:#111
    classDef coder fill:#bfdbfe,stroke:#2563eb,color:#111
    classDef dongle fill:#bbf7d0,stroke:#16a34a,color:#111
    classDef lock fill:#fecaca,stroke:#dc2626,color:#111
    classDef log fill:#fef9c3,stroke:#ca8a04,color:#111
    classDef sleep fill:#cffafe,stroke:#0891b2,color:#111
```

> ⚠️ **`counter++` happens AFTER `is compiling` is logged** so the printed log always
> matches the count (a compile can't "count" without being announced).

---

## 5. 🔌 Dongle acquisition — arbitration + cooldown

```mermaid
flowchart TD
    A["lock(dongle->mutex)"]:::dongle --> P["dq_push(me) → 2-slot queue"]:::dongle
    P --> W{"over?"}:::dec
    W -- yes --> EX["dq_pop(me); unlock; return"]:::se
    W -- no --> MT{"my_turn?<br/>owner==-1 && dq_best()==me"}:::dec
    MT -- "no" --> CW["💤 cond_wait (until release/over)"]:::sleep --> W
    MT -- "yes, cooldown pending" --> CD["💤 wait_cooldown<br/>timedwait → released+cooldown"]:::sleep --> W
    MT -- "yes, cooldown elapsed" --> G["owner=me; dq_pop;<br/>unlock; ✅ return"]:::ok

    classDef dongle fill:#bbf7d0,stroke:#16a34a,color:#111
    classDef dec fill:#fde68a,stroke:#d97706,color:#111
    classDef sleep fill:#cffafe,stroke:#0891b2,color:#111
    classDef ok fill:#86efac,stroke:#15803d,color:#111
    classDef se fill:#e5e7eb,stroke:#6b7280,color:#111
```

> 🏁 **`dq_best()`** — FIFO: smallest `arrived` • EDF: smallest `deadline` (tie → lower `id`).

---

## 6. 🩺 The monitor — precise, event-driven

```mermaid
flowchart TD
    L["lock(over_mutex)"]:::lock --> W{"over?"}:::dec
    W -- yes --> U
    W -- no --> F{"find_burned()<br/>now > deadline ?"}:::dec
    F -- burned --> SET["over=1; broadcast(over_cond)"]:::lock --> U["unlock(over_mutex)"]:::lock
    F -- none --> AD{"all_done()?"}:::dec
    AD -- yes --> SET
    AD -- no --> WD["💤 wait_deadline()<br/>timedwait UNTIL nearest deadline"]:::sleep --> W
    U --> LOG["📝 if burned: 'burned out'<br/>(AFTER unlock — lock-order safe)"]:::log
    LOG --> WK["wake_all_dongles()<br/>(AFTER unlock)"]:::dongle

    classDef lock fill:#fecaca,stroke:#dc2626,color:#111
    classDef dec fill:#fde68a,stroke:#d97706,color:#111
    classDef sleep fill:#cffafe,stroke:#0891b2,color:#111
    classDef log fill:#fef9c3,stroke:#ca8a04,color:#111
    classDef dongle fill:#bbf7d0,stroke:#16a34a,color:#111
```

> 💡 **Why `cond_timedwait`, not `usleep` polling?** It wakes **exactly** at the
> nearest deadline → catches every miss within timer latency (no 1ms poll gap to
> slip through), near-zero idle CPU, and a coder's compile-signal wakes it to
> notice completion immediately.

---

## 7. 🛡️ Deadlock prevention

```mermaid
flowchart LR
    R1["RULE 1 — Resource ordering<br/>always lock LOWER-id dongle first<br/>(coder N is asymmetric)"]:::ok
    R2["RULE 2 — Lock order (no inversion)<br/>dongle->mutex ▶ over_mutex<br/>print_mutex ▶ over_mutex<br/>NEVER reverse"]:::ok
    R1 --> NC["❌ no circular wait"]:::bad
    R2 --> NI["❌ no lock-order inversion"]:::bad
    classDef ok fill:#86efac,stroke:#15803d,color:#111
    classDef bad fill:#fecaca,stroke:#dc2626,color:#111
```

> The monitor **releases `over_mutex`** before calling `loging()` or
> `wake_all_dongles()` (both take other locks) — that's what keeps Rule 2 intact.

---

## 8. 🛑 Shutdown

```mermaid
sequenceDiagram
    participant M as 🩺 Monitor
    participant Cd as over_cond
    participant Dg as dongle conds
    participant C as 🧵 Coders
    M->>M: over = 1
    M->>Cd: broadcast(over_cond)
    Note over C: wakes coders in u_sleep / wait_deadline
    M->>Dg: wake_all_dongles (broadcast each)
    Note over C: wakes coders blocked in dongle_acquire
    C->>C: loop sees !over false → return
    M->>C: ft_over joins monitor + all coders
    M->>M: destroy_hub (free + destroy locks)
```

---

## 9. 🗃️ File & function map

> Norminette: **≤ 5 functions / file**, **≤ 25 lines / function**, no globals.

| 📄 File | 🔧 Functions | Role |
|---|---|---|
| `main.c` | `ft_codexion`, `fail_start`, `main` | spawn / join / cleanup |
| `parser.c` | `ft_parser`, `ft_check_params`, `is_number`, `ft_get_values` | argument validation |
| `init.c` | `ft_init_hub`, `destroy_hub`, `destroy_dongles`, `queue_free` | alloc / free |
| `coders.c` | `init_coder`, `compile_time`, `work_time`, `coder_routine` | coder lifecycle |
| `coder_utils.c` | `get_order`, `release_owned`, `take_dongles` | acquire helpers |
| `dongles.c` | `init_dongle`, `my_turn`, `wait_cooldown`, `dongle_acquire`, `dongle_release` | dongle + cooldown |
| `queue_utils.c` | `dq_push`, `dq_pop`, `winner`, `dq_best` | 2-slot priority queue |
| `monitor.c` | `wake_all_dongles`, `find_burned`, `all_done`, `wait_deadline`, `monitor_routine` | burnout/completion |
| `ft_over.c` | `ft_over`, `is_over`, `set_over` | join + over flag |
| `logtime.c` | `get_time_ms`, `loging`, `u_sleep` | clock / log / sleep |

---

## 10. ✅ Summary — what was done

| Area | Outcome |
|---|---|
| 🏗️ **Architecture** | Replaced global *server + manager* with **per-dongle arbitration** + single **monitor**. |
| 🎯 **Correctness** | Deadline = `last_compile_start + burnout`; `u_sleep` units; `counter++` after the log; interruptible sleeps; log-ordering race fixed; clean cleanup on `pthread_create` failure. |
| 🩺 **Precise monitor** | `cond_timedwait` to nearest deadline (not polling) → burnout caught precisely; fixed the `u_sleep` `while`-loop + strict `>` it exposed. |
| 🧪 **Concurrency** | ThreadSanitizer **0**, Helgrind **0** (+ `helgrind.supp` for glibc condvar false positive), Valgrind **0 leaks**. |
| 🧹 **Norm & hygiene** | norminette OK, ≤5 funcs/file, no globals, comments stripped, no relink. |
| 🛠️ **Tooling & docs** | `test_codexion.sh` (79 checks incl. INT_MAX/overflow), `CORRECTION.md`, this file, `helgrind.supp`. |
| 🧩 **Edge cases** | 1 coder, huge N / INT_MAX, zero work-times, huge cooldown, FIFO/EDF, `burnout≈cycle` boundary. |

> **Verified state:** build clean • norminette OK • **79/79** suite • TSan / Helgrind / Valgrind all **0**.
