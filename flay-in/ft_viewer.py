""" Where you can see the Game of Drones """
import sys
import os
try:
    import pygame
except ModuleNotFoundError:
    print("Usage: make install")
    sys.exit(1)

from models import Zone, Drone, Hub
from ft_config import Config
from ft_sim import Sim


class Viewer:
    """Window of the Fly-in visualization see the world"""

    def __init__(self, sim: Sim, config: Config) -> None:
        """Creating the window of fly-in"""
        self.sim = sim
        self.game = sim.game
        self.cfg = config
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000.0

        self.paused = not True
        self.steps = False
        pygame.init()
        os.system('clear')
        print('<------------------------------------------>')
        print('<--------------[  FLY-IN  ]---------------->')
        print('<------------------------------------------>')

        self.screen: pygame.Surface = pygame.display.set_mode((
            self.cfg.WIDTH,
            self.cfg.HEIGHT))
        pygame.display.set_caption("Fly-in Visualizer")

        self.msg_font = pygame.font.SysFont(None, 38)
        self.font = pygame.font.SysFont(None, 20)
        self.drone_font = pygame.font.SysFont(None, 15)
        self.header_font = pygame.font.SysFont(None, 64)

    def draw_node(
            self,
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
                x - self.cfg.RECT_SIZE / 2,
                y - self.cfg.RECT_SIZE / 2,
                self.cfg.RECT_SIZE,
                self.cfg.RECT_SIZE
            )
            pygame.draw.rect(self.screen, color, rect)
            if len(hub.drones) >= 1:
                pygame.draw.rect(
                        self.screen, b_color, rect, self.cfg.BORDER_WIDTH)
        elif zone == Zone.blocked:
            rect = pygame.Rect(
                    x - self.cfg.RECT_SIZE / 2,
                    y - self.cfg.RECT_SIZE / 2,
                    self.cfg.RECT_SIZE,
                    self.cfg.RECT_SIZE
                    )
            pygame.draw.rect(self.screen, color, rect)

            if len(hub.drones) >= 1:
                pygame.draw.rect(
                        self.screen, color, rect, self.cfg.BORDER_WIDTH)
            pygame.draw.line(
                    self.screen,
                    b_color,
                    rect.topleft,
                    rect.bottomright,
                    4
                    )
            pygame.draw.line(
                    self.screen,
                    b_color,
                    rect.topright,
                    rect.bottomleft,
                    4
                    )

        else:
            pygame.draw.circle(
                    self.screen,
                    color,
                    (x, y),
                    self.cfg.NODE_RADIUS
                    )
            if not len(hub.drones) >= 1:
                pygame.draw.circle(
                        self.screen,
                        b_color,
                        (x, y),
                        self.cfg.NODE_RADIUS,
                        self.cfg.BORDER_WIDTH)

    def draw_hubs(self) -> None:
        """
        Draw Each Hub with it;s Credentials
        """
        pr = 0
        for name, hub in self.game.all_hubs().items():
            x = self.cfg.to_screen_x(hub.x)
            y = self.cfg.to_screen_y(hub.y)

            color: tuple[int, int, int] = self.cfg.get_zone_color(
                    hub.meta.zone,
                    hub.meta.color)

            b_color = self.cfg.get_border_color(hub.meta.zone)
            self.draw_node(hub, x, y, color, b_color)

            nb = hub.meta.max_drones
            offset = -40 if pr % 2 == 0 else 40
            off_y = 8 if pr % 3 == 0 else 0
            text = self.font.render(f'{name}:{nb}', True, (255, 255, 255))
            self.screen.blit(text, (x - 30, y - offset + off_y))
            pr += 1

    def draw_connections(self) -> None:
        """ Draw Connection between hubs depend on max_link """
        hubs = self.game.all_hubs()

        for net in self.game.net.values():
            h1 = hubs[net.name1]
            h2 = hubs[net.name2]

            x1 = self.cfg.to_screen_x(h1.x)
            y1 = self.cfg.to_screen_y(h1.y)
            x2 = self.cfg.to_screen_x(h2.x)
            y2 = self.cfg.to_screen_y(h2.y)

            pygame.draw.line(
                self.screen,
                self.cfg.get_link_color(net),
                (x1, y1),
                (x2, y2),
                4
                )

    def display_msg(self, msg: str) -> None:
        """ display your msg simply"""
        msg_r: pygame.Surface = self.msg_font.render(
                msg, True, (100, 255, 180))
        self.screen.blit(
                msg_r,
                (self.cfg.WIDTH / 2 - 320, self.cfg.HEIGHT - 40))

    def ft_draw_drone(self, drone: Drone) -> None:
        """Draw a drone shape"""
        x = self.cfg.to_screen_x(drone.x)
        y = self.cfg.to_screen_y(drone.y)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 10)
        nbr = self.drone_font.render(str(drone.idx), True, (0, 0, 0))
        self.screen.blit(
                nbr,
                (int(x) - nbr.get_width() / 2, int(y) - nbr.get_height() / 2))

    def game_menu(self) -> None:
        """a box menu containe simulation directions"""
        keys = [
                '<x>  close the Window',
                '<r> reset mode',
                '<p>  pause mode / resume',
                '<s>  step mode',
                '<SPACE> next in step mode',
                ]
        pad = 10
        line_h = 20
        box_w = 200
        box_h = pad * 2 + len(keys) * line_h
        box_y = self.cfg.HEIGHT - box_h - 20
        box_x = self.cfg.WIDTH - box_w - 20
        pygame.draw.rect(
                self.screen, (80, 40, 80), (box_x, box_y, box_w, box_h), 3)
        for i, item in enumerate(keys):
            txt = self.font.render(item, True, (180, 180, 180))
            self.screen.blit(txt, (box_x + pad, box_y + pad + i * line_h))

    def ft_display_env(self) -> None:
        """ Display content in the window """
        self.game_menu()
        header = self.header_font.render(
                    f"Number of drones : {self.game.nb_drones}",
                    True,
                    (0, 191, 255))
        turn_calc = self.header_font.render(
                    f"Number of turnes: {self.sim.turns}",
                    True,
                    (0, 191, 255))
        self.screen.blit(header, (10, 5))
        self.screen.blit(turn_calc, (self.cfg.WIDTH - 460, 5))
        self.draw_connections()
        self.draw_hubs()

        for drone in self.sim.drones:
            self.ft_draw_drone(drone)
            if not self.paused:
                self.sim.ft_update_drone(drone, self.dt)

        if not self.paused and not self.steps:
            if self.sim.all_drones_arrived():
                self.sim.step()

        if self.paused and not self.steps:
            self.display_msg("PAUSED MODE (<p> to resume)")
        elif self.steps:
            self.display_msg(
                    "STEP MODE (<SPACE> to advance | <s> to exit)")
        elif self.sim.sim_done():
            self.display_msg(
                    "Simulation Done all drones arrived successfully in "
                    +
                    f"{self.sim.turns} turn.")
        else:
            self.display_msg("press <p> to pause <s> to slow down")
        pygame.display.flip()
        self.clock.tick(60)

    def run(self) -> None:
        """Run the simulation with pygame"""

        while self.running:
            self.screen.fill((30, 30, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.sim.reset()
                        self.paused = True
                        self.steps = False
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if event.key == pygame.K_s:
                        self.steps = not self.steps
                        self.paused = False
                    if event.key == pygame.K_SPACE and self.steps:
                        if self.sim.all_drones_arrived():
                            self.sim.step()
                    if event.key == pygame.K_x:
                        self.running = False
            self.ft_display_env()

        pygame.quit()
