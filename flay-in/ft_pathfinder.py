from models import Zone, Hub, Game, Net
from typing import Optional, List, Dict


class Pathfinder:
    """A* star pathfinder rout """

    def __init__(self, game: Game) -> None:
        """ get started with data of the environ"""
        self.game = game

    @staticmethod
    def move_cost(hub: Hub, net: Net) -> float:
        """Return the cost of the Hub"""
        costs = {
                Zone.normal: 1,
                Zone.priority: 0.8,
                Zone.restricted: 2,
                Zone.blocked: float('inf')
                }
        base = costs.get(hub.meta.zone, float('inf'))
        if base == float('inf'):
            return base

        #if len(hub.drones) >= hub.meta.max_drones:
        #    base += 0 # 0.02

        if net.usage >= net.meta.max_link_capacity:
            base += 0.1 # 0.07
        return base

    @staticmethod
    def reconstruct_path(
            came_from: Dict[str, Optional[str]],
            current: Optional[str]
            ) -> list[str]:
        """ Rebuild the path from the end back to start."""
        path: List[str] = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def A_star(self, start: Hub, end: Hub) -> list[str]:
        """Find the optimal path (list of Hubs) from start to end"""
        visited = []
        open_set = [start.name]
        came_from: Dict[str, Optional[str]] = {start.name: None}
        g_score = {start.name: 0.0}
        while open_set:
            current = min(open_set, key=lambda x: g_score.get(x, float('inf')))
            open_set.remove(current)

            if current == end.name:
                return self.reconstruct_path(came_from, current)

            visited.append(current)

            for n, net in self.game.get_neighbors(current):

                if n.name in visited:
                    continue

                if n.meta.zone == Zone.blocked:
                    continue
                cost = self.move_cost(n, net)
                new_g_score = g_score[current] + cost

                if n.name not in g_score or new_g_score < g_score[n.name]:

                    g_score[n.name] = new_g_score
                    # + self.heuristic(n, end)
                    came_from[n.name] = current
                    if n.name not in open_set:
                        open_set.append(n.name)
        return []
