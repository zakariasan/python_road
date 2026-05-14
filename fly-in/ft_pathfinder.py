from models import Zone, Hub, Game
from typing import Optional, List, Dict


def move_cost(hub: Hub) -> float:
    """Return the cost of the Hub"""
    costs = {
            Zone.normal: 1,
            Zone.priority: 1,
            Zone.restricted: 2,
            Zone.blocked: float('inf')
            }
    return costs.get(hub.meta.zone, 1)


def heuristic(a: Hub, b: Hub) -> float:
    """Calculate the probabily to get to the goal"""
    return abs((a.x - b.x)) + abs((a.y - b.y))


def reconstruct_path(
        came_from: Dict[str, Optional[str]],
        current: Optional[str]
        ) -> list[str]:
    """ Rebuild the path from the end to start."""
    path: List[str] = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def A_star(game: Game, start: Hub, end: Hub) -> list[str]:
    """Find the optimal path (list of Hubs) from s to e
    """
    visited = []

    open_set = [start.name]
    came_from: Dict[str, Optional[str]] = {start.name: None}

    g_score = {start.name: 0.0}
    f_score = {start.name: heuristic(start, end)}

    blocked = []
    blocked.append(start.name)
    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        open_set.remove(current)

        if current == end.name:
            return reconstruct_path(came_from, current)

        visited.append(current)

        for n, net in game.get_neighbors(current):

            if n.name in visited:
                continue

            if n.meta.zone == Zone.blocked:
                continue
            # if not net.can_use():
            #    continue

            cost = move_cost(n)
            new_g_score = g_score[current] + cost

            if n.name not in g_score or new_g_score < g_score[n.name]:
                g_score[n.name] = new_g_score
                f_score[n.name] = new_g_score + heuristic(n, end)
                came_from[n.name] = current
                if n.name not in open_set:
                    open_set.append(n.name)
            if len(n.drones) >= n.meta.max_drones:
                blocked.append(n.name)
                if n.name == end.name:
                    return reconstruct_path(came_from, n.name)
                continue
    if len(blocked) == 2:
        end = game.all_hubs()[blocked[1]]
        return A_star(game, start, end)
    #    return reconstruct_path(came_from, current)
    return []
    # return reconstruct_path(came_from, current)
    # return []
