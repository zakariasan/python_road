""" Where you can see the Game of Drones """
import pygame
from math import sqrt
from typing import Tuple
from models import Zone, Game, Net, Drone
from ft_config import WIDTH, HEIGHT, PADDING, \
        NODE_RADIUS, BORDER_WIDTH, BORDER_COLORS, \
        RECT_SIZE, ZONE_COLORS
from ft_pathfinder import A_star


def get_zone_color(zone: Zone, color: str):
    """Return the Hub color accrding the ZOne or color """
    if color:
        try:
            color = pygame.Color(color)
        except ValueError:
            color = (170, 51, 106)
    return ZONE_COLORS.get(zone, (165, 42, 42))


def get_border_color(zone: Zone):
    return BORDER_COLORS.get(zone, (55, 55, 55))


def to_screen(val: int, min_val: int, max_val: int, size: int) -> int:
    """ convert from graph into screen according our size """
    if max_val == min_val:
        return size / 2
    return int(((val - min_val) / (max_val - min_val)) * (size - 2 * PADDING)
               + PADDING)


def get_bounds(game: Game) -> Tuple[int, int, int, int]:
    """ get max and min corrdinates """
    hubs = game.all_hubs().values()
    x = [h.x for h in hubs]
    y = [h.y for h in hubs]
    return min(x), max(x), min(y), max(y)


def get_link_color(net: Net) -> Tuple[int, int, int]:
    """Color based on link capacity."""
    if net.meta.max_link_capacity > 1:
        return (0, 200, 255)
    return (180, 180, 180)


def draw_node(screen, hub, x, y, color, b_color):
    """Draw a hub with shape + border depending on zone"""

    zone = hub.meta.zone

    if zone == Zone.restricted:
        rect = pygame.Rect(
            x - RECT_SIZE / 2,
            y - RECT_SIZE / 2,
            RECT_SIZE,
            RECT_SIZE
        )

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, b_color, rect, BORDER_WIDTH)
    elif zone == Zone.blocked:
        rect = pygame.Rect(
                x - RECT_SIZE / 2,
                y - RECT_SIZE / 2,
                RECT_SIZE,
                RECT_SIZE
                )
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, color, rect, BORDER_WIDTH)
        pygame.draw.line(screen, b_color, rect.topleft, rect.bottomright, 4)
        pygame.draw.line(screen, b_color, rect.topright, rect.bottomleft, 4)

    else:
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, b_color, (x, y),
                           NODE_RADIUS, BORDER_WIDTH)


def draw_hubs(screen, game: Game, bounds, font):
    """
    Draw Each Hub with it;s Credentials

    Args:
        screen: where you can see the world.
        game: object has the world.
        bounds: bounds of the object.
        font: type of the text.
    """
    min_x, max_x, min_y, max_y = bounds
    pr = 0
    for name, hub in game.all_hubs().items():
        x = to_screen(hub.x, min_x, max_x, WIDTH)
        y = to_screen(hub.y, min_y, max_y, HEIGHT)

        color = get_zone_color(hub.meta.zone, hub.meta.color)

        b_color = get_border_color(hub.meta.zone)
        draw_node(screen, hub, x, y, color, b_color)

        if pr % 2 == 0:
            text = font.render(name, True, (255, 255, 255))
            screen.blit(text, (x, y - 45))
        else:
            text = font.render(name, True, (255, 255, 255))
            screen.blit(text, (x, y + 45))
        pr += 1


def draw_connections(screen, game: Game, bounds):
    min_x, max_x, min_y, max_y = bounds
    hubs = game.all_hubs()

    for net in game.net.values():
        h1 = hubs[net.name1]
        h2 = hubs[net.name2]

        x1 = to_screen(h1.x, min_x, max_x, WIDTH)
        y1 = to_screen(h1.y, min_y, max_y, HEIGHT)

        x2 = to_screen(h2.x, min_x, max_x, WIDTH)
        y2 = to_screen(h2.y, min_y, max_y, HEIGHT)

        pygame.draw.line(
            screen,
            get_link_color(net),
            (x1, y1),
            (x2, y2),
            4
        )


def ft_build_simple_path(game: Game):
    """Build the simple path"""
    ne = game.get_neighbors(game.s_hub.name)
    return ne


def ft_setup_drones(game: Game):
    """Set up the drones that we need to update later"""
    drone: [Drone] = []
    path = ft_build_simple_path(game)
    # path = A_star(game)
    for i in range(game.nb_drones):
        drone.append(Drone(i, game.s_hub.x, game.s_hub.y, path))
    return drone


def ft_draw_drone(screen, drone: Drone, bounds):
    """Draw a drone shape"""
    min_x, max_x, min_y, max_y = bounds
    x = to_screen(drone.x, min_x, max_x, WIDTH)
    y = to_screen(drone.y, min_y, max_y, HEIGHT)
    pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 10)


def ft_update_drone(drone: Drone, game: Game):

    if drone.current_index >= len(drone.path):
        return

    target = drone.path[drone.current_index]
    target = game.all_hubs()[target]

    dx = target.x - drone.x
    dy = target.y - drone.y
    dist = sqrt(dx * dx + dy * dy)

    if dist < drone.speed:
        drone.x = target.x
        drone.y = target.y
        drone.current_index += 1
        return

    vx = (dx / dist) * drone.speed
    vy = (dy / dist) * drone.speed

    drone.x += vx
    drone.y += vy


def run(game: Game) -> None:
    """Run the simulation with pygame"""

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in Visualizer")

    font = pygame.font.SysFont(None, 20)
    header_font = pygame.font.SysFont(None, 64)
    bounds = get_bounds(game)

    running = True
    clock = pygame.time.Clock()
    drones: [Drone] = ft_setup_drones(game)
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        header = header_font.render(
                f"Number of drones : {game.nb_drones}", True, (0, 191, 255))

        screen.blit(header, (WIDTH / 2 - 250, 0))
        draw_connections(screen, game, bounds)
        draw_hubs(screen, game, bounds, font)

        for drone in drones:
            drone.path = A_star(game)
            ft_update_drone(drone, game)
            ft_draw_drone(screen, drone, bounds)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
