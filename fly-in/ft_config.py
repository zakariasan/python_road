from models import Zone
from typing import Tuple, Dict, Optional
import pygame
from models import Game, Net


class Config:
    """All config/prams to run the simulation"""

    def __init__(self, game: Game):
        """ config the erea of the game"""
        self.game = game

        self.WIDTH: int = 1920
        self.HEIGHT: int = 961
        self.PADDING: int = 100

        self.NODE_RADIUS: int = 30
        self.BORDER_WIDTH: int = 5
        self.RECT_SIZE: int = 35

        self.START_COLOR: Tuple = (0, 255, 0)
        self.END_COLOR: Tuple = (255, 255, 0)

        bounds = self.get_bounds()
        self.MIN_X, self.MAX_X, self.MIN_Y, self.MAX_Y = bounds

        self.ZONE_COLORS: Dict[Zone, Tuple[int, int, int]] = {
                Zone.normal: (200, 200, 255),
                Zone.blocked: (100, 100, 100),
                Zone.restricted: (255, 100, 100),
                Zone.priority: (100, 255, 100),
            }
        self.BORDER_COLORS = {
                Zone.normal: (100, 100, 255),
                Zone.blocked: (255, 0, 0),
                Zone.restricted: (125, 0, 0),
                Zone.priority: (200, 155, 200)
            }

    def get_zone_color(
            self,
            zone: Zone,
            color: Optional[str]
            ) -> tuple[int, int, int]:
        """Return the Hub color accrding the ZOne or color """
        if color:
            try:
                c_s = pygame.Color(color)
                return (c_s.r, c_s.g, c_s.b)
            except ValueError:
                pass
        return self.ZONE_COLORS.get(zone, (170, 51, 106))

    def get_border_color(self, zone: Zone) -> tuple[int, int, int]:
        """get color border form the zone border"""
        return self.BORDER_COLORS.get(zone, (55, 55, 55))

    def get_bounds(self) -> Tuple[int, int, int, int]:
        """ get max and min corrdinates """
        hubs = self.game.all_hubs().values()
        x = [h.x for h in hubs]
        y = [h.y for h in hubs]
        return min(x), max(x), min(y), max(y)

    @staticmethod
    def get_link_color(net: Net) -> Tuple[int, int, int]:
        """Color based on link capacity."""
        if net.meta.max_link_capacity > 1:
            return (0, 200, 255)
        return (180, 180, 180)

    def zoom_in(
            self,
            val: float,
            min_val: int,
            max_val: int,
            size: int
            ) -> int:
        """ convert from graph into screen according our size """
        if max_val == min_val:
            return int(size / 2)
        return int(((val - min_val) / (max_val - min_val)) *
                   (size - 2 * self.PADDING) + self.PADDING)

    def to_screen_x(self, val: float) -> int:
        """Shorthand: convert an x coordinate using self.width."""
        return self.zoom_in(val, self.MIN_X, self.MAX_X, self.WIDTH)

    def to_screen_y(self, val: float) -> int:
        """Shorthand: convert a y coordinate using self.height."""
        return self.zoom_in(val, self.MIN_Y, self.MAX_Y, self.HEIGHT)
