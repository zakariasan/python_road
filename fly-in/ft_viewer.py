""" Where you can see the Game of Drones """
import pygame  # type: ignore
from typing import Tuple, List, Optional
from models import Zone, Game, Net, Drone, Hub
from ft_config import WIDTH, HEIGHT, \
        NODE_RADIUS, BORDER_WIDTH, BORDER_COLORS, \
        RECT_SIZE, to_screen
from ft_sim import ft_sim, ft_setup_drones, \
        ft_draw_drone, ft_update_drone, all_drones_arrived


def get_zone_color(
        zone: Zone,
        color: Optional[str]
        ) -> tuple[int, int, int]:
    """Return the Hub color accrding the ZOne or color """
    c = (170, 51, 106)
    if color:
        try:
            c_s = pygame.Color(color)
            c = (c_s.r, c_s.g, c_s.b)
        except ValueError:
            pass
    return c
    # return ZONE_COLORS.get(zone, (165, 42, 42))


def get_border_color(zone: Zone) -> tuple[int, int, int]:
    return BORDER_COLORS.get(zone, (55, 55, 55))


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


def draw_node(
        screen: pygame.Surface,
        hub: Hub,
        x: int,
        y: int,
        color: tuple[int, int, int],
        b_color: tuple[int, int, int]
        ) -> None:
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


def draw_hubs(
        screen: pygame.Surface,
        game: Game,
        bounds: tuple[int, int, int, int],
        font: pygame.font
        ) -> None:
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

        color: tuple[int, int, int] = get_zone_color(
                hub.meta.zone,
                hub.meta.color)

        b_color = get_border_color(hub.meta.zone)
        draw_node(screen, hub, x, y, color, b_color)

        nb = hub.meta.max_drones
        if pr % 2 == 0:
            text = font.render(f'{name}:{nb}', True, (255, 255, 255))
            screen.blit(text, (x, y - 45))
        else:
            text = font.render(f'{name}:{nb}', True, (255, 255, 255))
            screen.blit(text, (x, y + 45))
        pr += 1


def draw_connections(
        screen: pygame.Surface,
        game: Game,
        bounds: tuple[int, int, int, int]
        ) -> None:
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
    drones: List[Drone] = ft_setup_drones(game)
    turns: int = 0
    step_turn = False
    while running:
        screen.fill((30, 30, 30))

        step_turn = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    step_turn = True

        header = header_font.render(
                f"Number of drones : {game.nb_drones}", True, (0, 191, 255))
        turn_calc = header_font.render(
                f"Number of turnes: {turns}", True, (0, 190, 255))
        screen.blit(header, (10, 5))
        screen.blit(turn_calc, (WIDTH - 800, 5))
        draw_connections(screen, game, bounds)
        draw_hubs(screen, game, bounds, font)

        for drone in drones:
            ft_update_drone(drone, game)
            ft_draw_drone(screen, drone, bounds)

        if step_turn:
            if all_drones_arrived(drones):
                turns += ft_sim(game, drones, screen, bounds)
                step_turn = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
