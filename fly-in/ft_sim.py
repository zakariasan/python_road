from models import Game, Drone
from ft_pathfinder import A_star
from math import sqrt
import pygame
from ft_config import HEIGHT, WIDTH, to_screen


def ft_build_simple_path(game: Game):
    """Build the simple path"""
    ne = game.get_neighbors(game.s_hub.name)
    return ne


def ft_setup_drones(game: Game):
    """Set up the drones that we need to update later"""
    drone: [Drone] = []
    for i in range(game.nb_drones):
        path = A_star(game, game.s_hub)
        drone.append(Drone(i + 1, game.s_hub.x, game.s_hub.y, path, game.s_hub.name))
        game.s_hub.drones.append(f'D-{drone[i].idx}')
    return drone


def ft_update_drone(drone: Drone, game: Game):

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
        drone.next_hub = None
        
        return

    vx = (dx / dist) * drone.speed
    vy = (dy / dist) * drone.speed

    drone.x += vx
    drone.y += vy


def ft_draw_drone(screen, drone: Drone, bounds):
    """Draw a drone shape"""
    min_x, max_x, min_y, max_y = bounds
    x = to_screen(drone.x, min_x, max_x, WIDTH)
    y = to_screen(drone.y, min_y, max_y, HEIGHT)
    pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 10)


def all_drones_arrived(drones):
    for drone in drones:
        if drone.next_hub is not None:
            return False

    return True


def ft_sim(game, drones, screen, bounds):
    """Simulation goes here """
    moves: int = 0
    for drone in drones:
        where = game.all_hubs()[drone.hub_name]
        if drone.hub_name == game.e_hub.name:
            continue
        drone.path = []
        drone.path = A_star(game, where, drone.visited)
        if len(drone.path) > 1:
            drone.next_hub = drone.path[1]
            origine = game.all_hubs()[drone.hub_name]
            target = game.all_hubs()[drone.next_hub]
            if f'D-{drone.idx}' in origine.drones:
                origine.drones.remove(f'D-{drone.idx}')
            target.drones.append(f'D-{drone.idx}')
            drone.visited.append(origine.name)
            moves += 1
    if moves != 0:
        return 1
    return 0
