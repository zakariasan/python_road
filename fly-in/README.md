*This project has been created as part of the 42 curriculum by zhaouzan.*

---

# 🚁 Fly-in — Drone Routing Simulation

> *Drones are interesting.*

---

## Description

**Fly-in** is a drone fleet routing simulation built in Python. Given a graph of interconnected zones, the system routes multiple drones from a shared starting hub to a target end hub in the fewest simulation turns possible.

The project covers three main concerns:

- **Parsing** a custom text-based map format defining zones, connections, and constraints.
- **Pathfinding** using a modified A\*(DIJIKSTRA) algorithm that accounts for zone types, movement costs, occupancy limits, and connection capacities.
- **Visualization** via a real-time pygame window showing drone positions, zone states, and simulation progress turn by turn.

### Key concepts

| Concept | Description |
|---|---|
| Zone types | `normal` (1 turn), `restricted` (2 turns), `priority` (1 turn, preferred), `blocked` (impassable) |
| Zone capacity | Each zone has a `max_drones` limit (default 1); start and end zones are uncapped |
| Link capacity | Each connection has a `max_link_capacity` limit (default 1) |
| Turns | Discrete simulation steps; drones can move, wait, or be in transit simultaneously |

---

## Instructions

### Requirements

- Python 3.10 or later
- pygame (installed via `make install`)

### Installation

```bash
make install
```

### Running the simulation

```bash
make run file=path/to/map.txt
# or directly:
python main.py path/to/map.txt
```

### Other Makefile targets

```bash
make debug file=path/to/map.txt   # Run with Python's pdb debugger
make lint                          # Run flake8 + mypy with standard flags
make lint-strict                   # Run mypy --strict
make clean                         # Remove __pycache__ and .mypy_cache
```

### Map file format

```
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
connection: hub-corridorA
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

- Comments begin with `#` and are ignored.
- Zone names must not contain dashes or spaces.
- Coordinates must be integers.
- Duplicate connections (both `a-b` and `b-a`) are rejected.

---

## Algorithm Design

### A\* Pathfinding (`ft_pathfinder.py`)

Each drone computes its route using a modified A\* search. The key design choices are:

**Cost function:**
- `normal` → cost 1
- `priority` → cost 0.99 (slightly preferred to break ties)
- `restricted` → cost 2
- `blocked` → `inf` (pruned)

If a neighbor zone is at full capacity (`len(drones) >= max_drones`), a penalty of `+1.2` is added to its g-score. This softly discourages routing through congested zones without hard-blocking them, which allows the algorithm to adapt when alternate paths are unavailable.

**Heuristic:** Manhattan distance (`|Δx| + |Δy|`) — admissible for grid-like zone graphs.

**Fallback:** If the straight path to the end is fully blocked, the algorithm tries routing to the first occupied (blocking) zone and recurses. This handles deadlock situations where waiting drones prevent forward progress.

> ⚠️ The algorithm recomputes paths every turn. This is intentional: since zone occupancy changes each turn (drones arrive, leave, transit), caching a static path would lead to collisions and constraint violations. Recomputation per turn ensures correctness at the cost of O(V log V) per drone per turn.

**Complexity:**
- A\* per call: O(V log V + E), where V = zones, E = connections
- Per turn: O(D × (V log V + E)), where D = number of drones
- Memory: O(V) per pathfinding call (open set, came_from, g/f score dicts)

### Simulation Engine (`ft_sim.py`)

The `Sim` class drives the discrete turn loop:

1. Each turn, every active drone calls `plane_drone()`.
2. The drone's current position is used as A\* start; the end hub as goal.
3. The next hop is extracted from the computed path.
4. Connection availability (`can_use()`) and zone capacity are checked before committing a move.
5. If the origin zone is `restricted`, the drone first moves to the midpoint of the connection (occupying it for 1 turn), then completes the move on the next turn — and **must** complete it (no waiting allowed on a restricted transit).
6. Drones leaving a zone free its capacity in the same turn, allowing the freed slot to be used by another drone moving in.
7. Drones reaching the end hub are flagged as landed and excluded from further scheduling.

### Concurrency and conflict avoidance

All drone decisions are made in a single pass per turn. Link usage is tracked with a `usage` counter on each `Net` object and checked via `can_use()` before any drone reserves it. Zone occupancy is tracked via `hub.drones` lists. This prevents two drones from claiming the same slot in the same turn.

---

## Visual Representation

The pygame viewer (`ft_viewer.py`) provides a real-time graphical interface of the simulation.

### Features

| Visual element | Meaning |
|---|---|
| **Circle** node | Normal or priority zone |
| **Square** node | Restricted zone |
| **Square with ×** | Blocked zone |
| **Node color** | Zone type or explicit `color=` from map file |
| **Border highlight** | Zone is currently occupied by at least one drone |
| **Blue link** | Connection with `max_link_capacity > 1` |
| **Gray link** | Standard single-capacity connection |
| **White circle** | Drone (with ID number) |
| Turn counter | Displayed top-right in real time |
| Drone count | Displayed top-left |

### Controls

| Key | Action |
|---|---|
| `p` | Pause / resume |
| `s` | Toggle step mode |
| `SPACE` | Advance one step (in step mode) |
| `r` | Reset simulation to initial state |
| `x` | Close the window |

### Simulation output (terminal)

Each turn is printed as a line of space-separated drone movements, following the required format:

```
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB
D1-goal D2-goal
```

For drones in transit through a restricted zone connection, the intermediate position is printed as `D<ID>-<name1>-<name2>`.

---

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

## Resources

### Topic references

- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). *A Formal Basis for the Heuristic Determination of Minimum Cost Paths.* IEEE Transactions on Systems Science and Cybernetics. — The original A\* paper.
- [Red Blob Games — Introduction to A\*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — Clear visual explanation of A\* and its variants.
- [pygame documentation](https://www.pygame.org/docs/) — Official reference for the visualization layer.
- [Python dataclasses — PEP 557](https://peps.python.org/pep-0557/) — Used throughout the models module.
- [mypy documentation](https://mypy.readthedocs.io/) — Static type checking setup and flag reference.
- [flake8 documentation](https://flake8.pycqa.org/) — Style enforcement.
