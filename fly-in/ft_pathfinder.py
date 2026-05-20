from models import Zone, Hub, Game
from typing import Optional, List, Dict


class Pathfinder:
    """A* star pathfinder rout """

    def __init__(self, game: Game) -> None:
        """ get started with data of the environ"""
        self.game = game

    @staticmethod
    def move_cost(hub: Hub) -> float:
        """Return the cost of the Hub"""
        costs = {
                Zone.normal: 1,
                Zone.priority: 0.8,
                Zone.restricted: 2,
                Zone.blocked: float('inf')
                }
        return costs.get(hub.meta.zone, float('inf'))

    @staticmethod
    def heuristic(a: Hub, b: Hub) -> float:
        """Calculate the probabily to get to the goal"""
        return (abs((a.x - b.x)) + abs((a.y - b.y)))

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

    def A_star(self, start: Hub, end: Hub, deep: int = 0) -> list[str]:
        """Find the optimal path (list of Hubs) from start to end"""
        if deep > len(self.game.all_hubs()):
            return []
        visited = []
        open_set = [start.name]
        came_from: Dict[str, Optional[str]] = {start.name: None}
        g_score = {start.name: 0.0}
        f_score = {start.name: self.heuristic(start, end)}
        blocked = []
        blocked.append(start.name)
        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            open_set.remove(current)

            if current == end.name:
                return self.reconstruct_path(came_from, current)

            visited.append(current)

            for n, net in self.game.get_neighbors(current):

                if n.name in visited:
                    continue

                if n.meta.zone == Zone.blocked:
                    continue
                cost = self.move_cost(n)

                # if n.meta.zone == Zone.priority:
                #    cost -= 0.01

                if len(n.drones) >= n.meta.max_drones:
                    cost += 0.8
                new_g_score = g_score[current] + cost

                if n.name not in g_score or new_g_score < g_score[n.name]:

                    g_score[n.name] = new_g_score

                    f_score[n.name] = new_g_score
                    # + self.heuristic(n, end)
                    came_from[n.name] = current
                    if n.name not in open_set:
                        open_set.append(n.name)

                if len(n.drones) >= n.meta.max_drones:
                    blocked.append(n.name)
                    if n.name == end.name:
                        return self.reconstruct_path(came_from, n.name)
                    continue

        if len(blocked) == 2:
            fallback = self.game.all_hubs()[blocked[1]]
            return self.A_star(start, fallback, deep + 1)
        return []
