from models import Game, Drone, Hub, Zone, Net
from typing import List, Union
from ft_pathfinder import Pathfinder
from math import sqrt


class Sim:
    """ where Fly-in start after parsing """

    def __init__(self, game: Game) -> None:
        """ get game Object and Path """
        self.game = game
        self.pathfinder = Pathfinder(self.game)
        self.drones: List[Drone] = []
        self.turns: int = 0
        self.ft_setup_drones()

    def ft_setup_drones(self) -> List[Drone]:
        """Set up the drones that we need to update later"""
        if self.game.s_hub is None:
            raise ValueError("Missing start hub")
        for i in range(self.game.nb_drones):
            self.drones.append(Drone(
                idx=i + 1,
                x=self.game.s_hub.x,
                y=self.game.s_hub.y,
                path=None,
                hub_name=self.game.s_hub.name))
            self.game.s_hub.drones.append(f'D-{self.drones[i].idx}')
        return self.drones

    def ft_update_drone(self, drone: Drone, dt) -> None:
        """Move drone from hub to next one if it's possible"""
        target: Union[Hub, Net]
        if not drone.next_hub:
            return
        if drone.next_hub in self.game.all_hubs():
            target = self.game.all_hubs()[drone.next_hub]
        else:
            if drone.net is None:
                return
            target = drone.net

        dx = target.x - drone.x
        dy = target.y - drone.y
        dist = sqrt(dx * dx + dy * dy)
        move_step = drone.speed * dt
        if dist <= drone.speed or\
                (drone.x == target.x and drone.y == target.y):
            drone.x = target.x
            drone.y = target.y
            if drone.next_hub not in self.game.all_hubs():
                return
            target_hub: Hub = self.game.all_hubs()[drone.next_hub]
            drone.hub_name = target_hub.name
            if drone.net:
                drone.net.usage -= 1
                drone.net = None
                drone.next_hub = None
                return

        vx = (dx / dist) * drone.speed
        vy = (dy / dist) * drone.speed
        drone.x += vx
        drone.y += vy

    def all_drones_arrived(self) -> bool:
        """ Check if drones are moving around the map"""
        for drone in self.drones:
            if drone.next_hub is not None:
                if drone.net is None or not drone.was_in(drone.net):
                    return False
        return True

    def sim_done(self) -> bool:
        """ check if all drones are in the e_hub"""
        for drone in self.drones:
            if self.game.e_hub and drone.hub_name != self.game.e_hub.name:
                return False
        return True

    def drone_land(self, drone: Drone) -> bool:
        """ check if the drone lands or still fly in"""
        if drone.hub_name is None:
            return True
        if self.game.e_hub is None:
            return False
        return drone.hub_name == self.game.e_hub.name

    def step(self) -> int:
        """Simulation goes here """
        moves = 0
        for drone in self.drones:
            if self.drone_land(drone):
                continue

            if self.plane_drone(drone):
                moves += 1
        if moves:
            print()
            self.turns += 1
        return 1 if moves else 0

    def plane_drone(self, drone: Drone) -> bool:
        """ Compute the path of a drone from it's xand y to the end"""

        if drone.hub_name is None or self.game.e_hub is None:
            return False
        origine: Hub = self.game.all_hubs()[drone.hub_name]
        end_p: Hub = self.game.e_hub

        if drone.next_hub is None:
            drone.path = self.pathfinder.A_star(origine, end_p)
        if len(drone.path) <= 1:
            return False
        target: Hub = self.game.all_hubs()[drone.path[1]]
        net = self.game.get_network(origine, target)
        if (not net) or (not net.can_use() and net != drone.net):
            drone.next_hub = None
            return False

        drone.net = net
        net.stay_in(origine, target)
        if len(target.drones) >= target.meta.max_drones:
            if origine.meta.zone != Zone.restricted or net.can_use():
                return False

        if target.meta.zone == Zone.restricted and not drone.was_in(net):
            drone.next_hub = net.get_name()
        else:
            drone.next_hub = drone.path[1]
            drone.path.pop(0)
            if origine.meta.zone == Zone.restricted:
                net.usage -= 2
        net.reserve()
        if f'D-{drone.idx}' in origine.drones:
            origine.drones.remove(f'D-{drone.idx}')
        if target.meta.zone == Zone.restricted and drone.was_in(net):
            target.drones.append(f'D-{drone.idx}')
        elif target.meta.zone != Zone.restricted:
            target.drones.append(f'D-{drone.idx}')

        drone.visited.append(origine.name)
        print(f'D{drone.idx}-{drone.next_hub} ', end='')

        return True

    def reset(self) -> None:
        """ reset the simulation back to where we start"""
        for hub in self.game.all_hubs().values():
            hub.drones.clear()

        for net in self.game.net.values():
            net.usage = 0

        self.drones.clear()
        self.turns = 0
        self.ft_setup_drones()
        print('<-----------------Again------------------->')
