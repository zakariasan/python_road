*This project has been created as part of the 42 curriculum by zhaouzan.*

# Fly-in :Drones are interesting.
Summary: Design an efficient drone routing system that navigates multiple drones
through connected zones while minimizing simulation turns and handling movement
constraints

## Description

**Fly-in** routes a fleet of drones from a single **start** zone to a single **end** zone across a network of connected zones, in the fewest possible simulation turns, while respecting a set of strict movement and capacity constraints.

The network is described in a plain-text map file: zones (hubs) have coordinates, a zone *type* that determines movement cost, and an optional capacity; connections are bidirectional edges between zones, each with its own capacity. The simulation advances in discrete turns, moving every drone that legally can move, and visualises the whole thing in a `pygame` window.

The project is fully object-oriented and type-safe (`flake8` + `mypy --strict` clean), and uses **no external graph library** — pathfinding is implemented from scratch.

The codebase is split by responsibility:

| File | Responsibility |
|------|----------------|
| `main.py` | Entry point — argument handling, wiring parser → sim → viewer |
| `errors.py` | Exception hierarchy (`FlyInError` → `ParseError`, `ValidationError`) |
| `models.py` | Data model: `Zone`, `Metadata`, `Hub`, `Net`, `Game`, `Drone` |
| `ft_parser.py` | Map-file parsing and validation |
| `ft_pathfinder.py` | Shortest-path search over the zone graph |
| `ft_sim.py` | Turn-by-turn simulation engine and movement scheduling |
| `ft_config.py` | Screen/coordinate configuration and colour mapping |
| `ft_viewer.py` | `pygame` visualisation and interactive controls |

## Project Structure

```
.
├── main.py             # Entry point — argument parsing, orchestration
├── models.py           # Data classes: Zone, Metadata, Hub, Net, Game, Drone
├── ft_parser.py        # Map file parser and validator
├── ft_pathfinder.py    # A* pathfinding algorithm
├── ft_sim.py           # Simulation engine (turn loop, movement rules)
├── ft_viewer.py        # pygame visualization window
├── ft_config.py        # Display configuration and coordinate mapping
├── errors.py           # Custom exception hierarchy
├── Makefile
└── README.md
```

---


## Instructions

### Requirements
- Python 3.10 or later
- `pygame` (installed via the Makefile)

### Map format
```
nb_drones: <positive integer>
start_hub: <name> <x> <y> [metadata]
end_hub:   <name> <x> <y> [metadata]
hub:       <name> <x> <y> [metadata]
connection: <name1>-<name2> [metadata]
# lines starting with '#' are comments
```

Metadata is optional and order-independent:
- Hubs: `zone=normal|blocked|restricted|priority`, `color=<word>`, `max_drones=<positive int>`
- Connections: `max_link_capacity=<positive int>`

Zone names may use any characters **except dashes and spaces** (dashes delimit connections). Coordinates are integers. There must be exactly one `start_hub` and one `end_hub`, each name and coordinate pair unique.

### Running
```bash
make install     # install dependencies
make run file=maps/example.txt
# or directly:
python main.py maps/example.txt
```

Other Makefile targets:
```bash
make debug file=maps/example.txt   # run under pdb
make lint                          # flake8 . && mypy . (mandatory flags)
make lint-strict                   # flake8 . && mypy . --strict
make clean                         # remove __pycache__, .mypy_cache, etc.
```

### Interactive controls (in the visualiser window)
| Key | Action |
|-----|--------|
| `p` | Pause / resume |
| `s` | Toggle step mode |
| `SPACE` | Advance one turn (in step mode) |
| `r` | Reset the simulation to the start |
| `x` | Close the window |

## Algorithm explanation

### Overview: two cooperating layers

The system separates **planning** from **scheduling**, because the two answer different questions:

1. **Pathfinding** (`ft_pathfinder.py`) answers *"what is the cheapest route to the end for this one drone, given the current map state?"* — ignoring turn-by-turn collisions.
2. **The simulation** (`ft_sim.py`) answers *"given everyone's intended route, who is actually allowed to move this turn without violating a capacity constraint?"*

Conflict avoidance lives in the **scheduler**, not the pathfinder. The pathfinder only nudges drones to spread out via a soft congestion penalty; the hard guarantees (zone capacity, link capacity, the restricted-zone rule) are enforced when a move is committed.

### The pathfinding search, step by step

A note on naming first: the method is called `A_star`, but with the heuristic term disabled it is **Dijkstra's algorithm** (equivalently, uniform-cost search) — A\* with `h = 0`. This is a deliberate choice, not an unfinished implementation. The edge cost depends only on the *destination zone type* (and congestion), and is **decoupled from the hubs' (x, y) geometry** — a hub can be physically distant but cheap to reach, or adjacent but expensive. Because of that decoupling there is no cheap, admissible distance-based heuristic to plug in, so a straight-line heuristic would either break optimality or collapse to zero. For this cost structure Dijkstra is the correct, optimal algorithm; the subject requires "a pathfinding algorithm capable of minimizing total turns," not A\* by name.

Movement costs by destination zone type:

| Zone | Cost | Notes |
|------|------|-------|
| `priority` | 0.8 | preferred — cheapest, so the search favours it |
| `normal` | 1 | default |
| `restricted` | 2 | sensitive zone, costs two turns to enter |
| `blocked` | ∞ | never entered (skipped outright) |

The search proceeds:

1. **Initialise.** `open_set = [start]`, `g_score[start] = 0`, `came_from[start] = None`, `visited = []`.
2. **Select.** Pick the node in `open_set` with the lowest `g_score` (lowest accumulated cost so far). This is the Dijkstra selection rule.
3. **Goal test.** If it is the end hub, rebuild the path by walking `came_from` backwards and reverse it — done.
4. **Close it.** Add the node to `visited`; it will never be reconsidered. This is valid because all edge costs are non-negative (the minimum is 0.8 > 0), so the first time a node is popped its cost is already final.
5. **Relax neighbours.** For each connected neighbour that isn't already closed and isn't `blocked`:
   - compute `cost = move_cost(neighbour)`;
   - add a **congestion penalty of +1.8** if the neighbour is currently at or over its `max_drones` — this makes crowded routes look more expensive so later drones naturally pick alternates;
   - if `g_score[current] + cost` improves the neighbour's best known cost, record the new cost and parent, and add it to the open set.
6. **Loop** until the end is reached or the open set empties (no path → returns `[]`).

### The simulation, step by step

Each call to `step()` walks every still-flying drone once and asks `plane_drone()` whether it can move:

1. **Skip the delivered.** Drones already at the end hub are ignored.
2. **(Re)plan if needed.** A drone with no committed `next_hub` recomputes its path from its current hub. This means paths adapt to live congestion rather than being fixed once at the start.
3. **Find the next edge.** Take the connection from the current hub to the next hub on the path.
4. **Capacity gate.** A drone may step onto a connection only if the connection has spare capacity. The cap used is `effective_capacity(target)` — the **tighter** of the link's `max_link_capacity` and, for a restricted destination, the hub's `max_drones`. This is what stops a wide link (`max_link_capacity ≥ 2`) from shoving more drones at a one-slot restricted hub than it can receive.
5. **Commit the move**, with three cases:
   - **Entering a restricted zone** (a two-turn move): the drone moves onto the *connection midpoint* this turn and **claims both** the link slot and the destination hub slot for the whole transit. It is then *forced* to land next turn — the subject forbids waiting on a connection.
   - **The forced landing turn**: the drone arrives at the restricted hub. Its slots were already claimed on entry, so it commits without re-reserving (this avoids double-counting link usage and avoids a drone blocking itself with its own reservation).
   - **A normal one-turn hop**: reserve the link, occupy the destination, free the origin.
6. **Free the origin.** The drone is removed from its old hub's occupancy list in the same turn it leaves — so the slot it vacates is immediately available to another drone that turn (per the "drones moving out free up capacity" rule).
7. **Emit output.** Each moving drone prints `D<id>-<dest>` for that turn.

The run ends when every drone's `hub_name` is the end hub (`sim_done()`).

### Why occupancy is claimed on *entry*, not on *arrival*

This is the subtle correctness point of the whole engine. A restricted move spans two turns with the drone sitting on the connection in between. If the destination hub's slot were only claimed on arrival, then during transit the hub would *look* empty, and the only thing gating entry would be the link capacity — so several drones could pile onto one connection and then be unable to land. By claiming the hub slot the instant a drone steps onto the connection (and holding it through transit), any other drone — even one arriving via a *different* connection into the same hub — correctly sees the hub as full and waits at its origin instead of getting stranded mid-air.

## Visual representation features

The `pygame` viewer turns the abstract graph and the per-turn output into something you can actually watch and reason about:

- **Zones are drawn by type**, so the map's structure is readable at a glance:
  - normal / priority zones → circles
  - restricted zones → squares
  - blocked zones → squares with a red cross (visibly impassable)
- **Colour coding** uses each zone type's palette, and respects any explicit `color=` from the map file, with a sensible default fallback.
- **Connection capacity is visible**: links with `max_link_capacity > 1` are drawn in a distinct colour, so high-throughput corridors stand out from single-file ones.
- **Occupancy feedback**: a hub's border is highlighted while it holds a drone, making capacity pressure and queuing visible in real time.
- **Live counters**: the header shows the number of drones and the running turn count, which is the project's actual score — so you watch the metric you're optimising as it climbs.
- **Drones** are rendered as numbered tokens that animate smoothly between zones (interpolated motion), including the mid-connection position during restricted, two-turn moves — so the "in transit" state is something you can literally see.
- **Interactive control** — pause, single-step, and reset — lets a reviewer freeze any turn, advance one move at a time to verify scheduling decisions, or restart to re-watch a tricky sequence. Step mode in particular makes it easy to confirm, turn by turn, that no capacity rule is ever violated.

Together these turn "trust the turn count" into "see *why* the turn count is what it is" — which is exactly what helps a peer evaluate the algorithm's behaviour.

## Example

### Input — `maps/example.txt`
```
nb_drones: 2
start_hub: start 0 0
hub: mid 5 0
end_hub: goal 10 0
connection: start-mid
connection: mid-goal
```

Here `mid` is a default zone (`max_drones = 1`) on single-capacity links, so the two drones cannot pile through together — they must pipeline.

### Expected output
```
D1-mid
D1-goal D2-mid
D2-goal
```

Reading it turn by turn:
- **Turn 1** — `D1` moves into `mid`. `D2` cannot follow (`mid` is full) and waits at `start`.
- **Turn 2** — `D1` advances `mid → goal`, freeing `mid` in the same turn, so `D2` moves into the now-empty `mid`.
- **Turn 3** — `D2` advances to `goal`. All drones delivered in **3 turns**.

(The visualiser shows the same sequence with the counter ticking 0 → 3 and the `mid` border lighting up as each drone passes through.)

## Complexity, accuracy, and performance

### Current complexity

Within one pathfinding call the frontier (`open_set`) is a Python **list**, and the closed set (`visited`) is also a list. That makes the hot operations linear scans:

- `min(open_set, ...)` to select the next node → **O(V)**
- `open_set.remove(...)` → **O(V)**
- `n.name in visited` membership test → **O(V)**

So a single search is on the order of **O(V²)** (more precisely O(V² + E)). And `plane_drone()` recomputes the path **per drone, per turn**, so a run costs roughly **O(T · D · V²)** for `T` turns and `D` drones. On small and medium maps this is fine; on the 15- and 25-drone maps it becomes the dominant cost.

Memory per search is **O(V)** for the `g_score`, `came_from`, `visited`, and `open_set` structures.

### Is it accurate?

Yes — Dijkstra returns the true minimum-cost path because every edge cost is non-negative (minimum 0.8), which is exactly the condition under which closing a node on first pop is sound. The capacity and restricted-zone rules are enforced in the scheduler, and the on-entry slot-claiming closes the one correctness gap (drones stranded on connections) that a naive on-arrival scheme would create. To keep it accurate while optimising, the invariant to preserve is the **resource lifecycle**: every link slot and hub slot claimed when a drone leaves a zone must be released exactly once when it arrives — never double-counted, never leaked. The current restricted handling reserves on entry and commits (without re-reserving) on the forced landing precisely to keep that balanced.

### How to make it more performant

These are the higher-value optimisations, roughly in order of impact:

1. **Replace the list frontier with a binary heap.** Using `heapq` for the open set and a `set` for the closed set turns selection and membership from O(V) into O(log V) and O(1), bringing each search to **O(E log V)**. `heapq` is a generic data structure, not a graph library, so it's allowed under the "no graph library" constraint. This is the single biggest win.
2. **Cache paths instead of recomputing every turn.** Most turns a drone's situation hasn't changed; recomputing the full search per drone per turn is wasteful. Cache a drone's path and only re-search when its route is actually invalidated (e.g. it gets blocked, or congestion ahead changes). This cuts the `D · per-turn` factor dramatically.
3. **Precompute the neighbour adjacency once.** `get_neighbors` currently scans every connection in the graph on each call; building an adjacency map once at startup makes neighbour lookup O(1) per node.
4. **Tune the congestion penalty / distribute across disjoint paths.** The flat `+1.8` penalty spreads drones heuristically; for the hard maps, explicitly allocating drones across disjoint or overlapping paths (rather than relying on the soft penalty alone) reduces total turns further.

The order matters: items 1–3 are pure speed (same answer, faster), while item 4 trades search effort for fewer turns — the actual scoring metric.

## Technical choices

- **Dijkstra over A\*** — edge cost depends on zone *type* and congestion, not on
  geometry, so no admissible distance heuristic exists; the geometry-free heuristic
  is 0, which makes A* identical to Dijkstra. Dijkstra is therefore optimal here,
  not a fallback.
- **Planning separated from scheduling** — the pathfinder finds cheap routes
  ignoring collisions; the simulation enforces all hard capacity rules at commit
  time. This keeps each layer simple and testable.
- **Conflict avoidance via on-entry reservation** — a drone claims its destination
  slot the moment it steps onto a connection, so capacity is respected even across
  multiple links feeding one restricted hub, and drones are never stranded mid-transit.
- **Adaptive re-planning** — paths are recomputed when a drone's route is invalidated,
  so routing responds to live congestion rather than being fixed once at the start.
- **No external graph library** — all pathfinding and graph traversal are implemented
  from scratch, as required.


  ## Error handling & validation

All failures raise typed exceptions from a single hierarchy (`FlyInError` →
`ParseError`, `ValidationError`) and are caught at the top level, so the program
exits with a clear message instead of a traceback. Parsing reports the **line
number** and cause of any malformed input. Validation rejects: missing/duplicate
start or end hubs, duplicate hub names or coordinates, unknown zone types,
non-positive capacities, connections referencing undefined hubs, duplicate
connections (`a-b` ≡ `b-a`), and maps with no valid path from start to end. File
handles are managed with a context manager.


## Resources

### References
- E. W. Dijkstra, "A Note on Two Problems in Connexion with Graphs" (1959) — the
  shortest-path algorithm this project's pathfinder is based on.
- Hart, Nilsson & Raphael, "A Formal Basis for the Heuristic Determination of
  Minimum Cost Paths" (1968) — the A* paper; useful for understanding why A*
  reduces to Dijkstra when the heuristic is zero, which is the case here.
- Red Blob Games — *Introduction to A\* / Pathfinding*
  (https://www.redblobgames.com/pathfinding/a-star/introduction.html) — clear,
  visual explanation of uniform-cost search, frontiers, and heuristics.
- Python `heapq` documentation
  (https://docs.python.org/3/library/heapq.html) — priority-queue structure for
  an O(E log V) frontier.
- pygame documentation (https://www.pygame.org/docs/) — rendering and event loop.

### Topic references

- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). *A Formal Basis for the Heuristic Determination of Minimum Cost Paths.* IEEE Transactions on Systems Science and Cybernetics. — The original A\* paper.
- [Red Blob Games — Introduction to A\*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — Clear visual explanation of A\* and its variants.
- [pygame documentation](https://www.pygame.org/docs/) — Official reference for the visualization layer.
- [Python dataclasses — PEP 557](https://peps.python.org/pep-0557/) — Used throughout the models module.
- [mypy documentation](https://mypy.readthedocs.io/) — Static type checking setup and flag reference.
- [flake8 documentation](https://flake8.pycqa.org/) — Style enforcement.
