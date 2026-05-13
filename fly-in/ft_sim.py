from models import Game, Drone, Hub, Zone
from typing import List
from ft_pathfinder import A_star
from math import sqrt
import pygame
from ft_config import HEIGHT, WIDTH, to_screen


# def ft_build_simple_path(game: Game):
#    """Build the simple path"""
#    return game.get_neighbors(game.s_hub.name)


def ft_setup_drones(game: Game) -> List[Drone]:
    """Set up the drones that we need to update later"""
    drone: List[Drone] = []
    if game.s_hub is None:
        raise ValueError("Missing start hub")
    for i in range(game.nb_drones):
        path = None
        drone.append(
                Drone(
                    i + 1, game.s_hub.x, game.s_hub.y, path, game.s_hub.name))
        game.s_hub.drones.append(f'D-{drone[i].idx}')
    return drone


def ft_update_drone(drone: Drone, game: Game) -> None:
    """Move drone from hub to next one if it's possible"""
    if not drone.next_hub:
        return

    target = game.all_hubs()[drone.next_hub]

    dx = target.x - drone.x
    dy = target.y - drone.y
    dist = sqrt(dx * dx + dy * dy)
    if dist <= drone.speed or (drone.x == target.x and drone.y == target.y):
        drone.x = target.x
        drone.y = target.y
        drone.hub_name = target.name
        if drone.net:
            drone.net.usage -= 1
            drone.net = None
        drone.next_hub = None
        return

    vx = (dx / dist) * drone.speed
    vy = (dy / dist) * drone.speed

    drone.x += vx
    drone.y += vy


def ft_draw_drone(
        screen: pygame.Surface,
        drone: Drone,
        bounds: tuple[int, int, int, int]) -> None:
    """Draw a drone shape"""
    min_x, max_x, min_y, max_y = bounds
    x = to_screen(drone.x, min_x, max_x, WIDTH)
    y = to_screen(drone.y, min_y, max_y, HEIGHT)
    pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 10)


def all_drones_arrived(drones: List[Drone]) -> bool:
    for drone in drones:
        if drone.next_hub is not None:
            return False

    return True


def ft_sim(
        game: Game,
        drones: List[Drone],
        screen: pygame.Surface,
        bounds: tuple[int, int, int, int]) -> int:
    """Simulation goes here """
    moves = 0
    turn = 1
    if game.e_hub is None:
        raise ValueError("Missing end hub")
    for drone in drones:
        if drone.hub_name is None:
            continue
        where: Hub = game.all_hubs()[drone.hub_name]
        to: Hub = game.e_hub
        if drone.hub_name and drone.hub_name == game.e_hub.name:
            continue
        drone.path = A_star(game, where, to)
        if len(drone.path) > 1:
            origine: Hub = game.all_hubs()[drone.hub_name]
            target: Hub = game.all_hubs()[drone.path[1]]

            if len(target.drones) >= target.meta.max_drones:
                continue
            net = game.get_network(origine, target)
            if not net or not net.can_use():
                drone.next_hub = None
                continue
            drone.next_hub = drone.path[1]
            drone.net = net
            net.reserve()
            if f'D-{drone.idx}' in origine.drones:
                origine.drones.remove(f'D-{drone.idx}')
            target.drones.append(f'D-{drone.idx}')
            drone.visited.append(origine.name)
            moves += 1
            print(f'D{drone.idx}-{target.name} ', end='')
            if target.meta.zone == Zone.restricted:
                turn = 2
            else:
                turn = 1
    print()
    if moves != 0:
        return turn
    return 0
