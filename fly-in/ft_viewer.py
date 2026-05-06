""" Where you can see the Game of Drones """
import pygame
from typing import Tuple
from models import Zone, Game, Net

WIDTH, HEIGHT = 1900, 920
PADDING = 90
NODE_RADIUS = 20
BORDER_WIDTH = 4
RECT_SIZE = 40
ZONE_COLORS = {
    Zone.normal: (200, 200, 255),
    Zone.blocked: (100, 100, 100),
    Zone.restricted: (255, 100, 100),
    Zone.priority: (100, 255, 100),
}
BORDER_COLORS = {
    Zone.normal: (100, 100, 255),
    Zone.blocked: (0, 0, 100),
    Zone.restricted: (255, 0, 0),
    Zone.priority: (200, 155, 200),
}
START_COLOR = (0, 255, 0)
END_COLOR = (255, 255, 0)


def get_zone_color(zone: Zone):
    return ZONE_COLORS.get(zone, (255, 255, 255))  # fallback = white


def get_border_color(zone: Zone):
    return BORDER_COLORS.get(zone, (55, 55, 55))


def get_radius(zone: Zone) -> int:
    """Optional: different size per zone."""
    if zone == Zone.priority:
        return 100
    if zone == Zone.blocked:
        return 40
    return 500


def to_screen(val: int, min_val: int, max_val: int, size: int) -> int:
    """ convert from graph into screen according our size """
    if max_val == min_val:
        return size // 2
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
            x - RECT_SIZE // 2,
            y - RECT_SIZE // 2,
            RECT_SIZE,
            RECT_SIZE
        )

        pygame.draw.rect(screen, color, rect)  # fill
        pygame.draw.rect(screen, b_color, rect, BORDER_WIDTH)  # border

    else:
        pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)
        pygame.draw.circle(screen, b_color, (x, y),
                           NODE_RADIUS, BORDER_WIDTH)


def draw_hubs(screen, game: Game, bounds, font):
    min_x, max_x, min_y, max_y = bounds

    for name, hub in game.all_hubs().items():
        x = to_screen(hub.x, min_x, max_x, WIDTH)
        y = to_screen(hub.y, min_y, max_y, HEIGHT)

        # Start / End override
        if game.s_hub and name == game.s_hub.name:
            color = START_COLOR
        elif game.e_hub and name == game.e_hub.name:
            color = END_COLOR
        else:
            color = get_zone_color(hub.meta.zone)

        b_color = get_border_color(hub.meta.zone)
        draw_node(screen, hub, x, y, color, b_color)

        # Label
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (x + 6, y + 6))


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
            2
        )


def run(game: Game) -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in Visualizer")

    font = pygame.font.SysFont(None, 18)
    bounds = get_bounds(game)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((30, 30, 30))  # background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw order matters
        draw_connections(screen, game, bounds)
        draw_hubs(screen, game, bounds, font)

        pygame.display.flip()
        clock.tick(60)  # smooth rendering

    pygame.quit()
