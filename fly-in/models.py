from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Set, Tuple, List
from errors import ValidationError, ParseError


class Zone(Enum):
    """ Zone Types in the mazw """
    normal = 'normal'
    blocked = 'blocked'
    restricted = 'restricted'
    priority = 'priority'


@dataclass
class Metadata:
    """Data about the hub or the connection"""
    zone: Zone = Zone.normal
    color: Optional[str] = None
    max_drones: int = 1
    max_link_capacity: int = 1

    def __post_init__(self) -> None:
        """Validate metadata after creation."""
        if not isinstance(self.max_drones, int) or self.max_drones <= 0:
            raise ValidationError("max_droes must be integer > 0")
        if not isinstance(self.max_link_capacity, int)\
                or self.max_link_capacity <= 0:
            raise ValidationError("Max_link must be int > 0.")


@dataclass
class Hub:
    """ Hub structure name x y metadata"""
    name: str
    x: int
    y: int
    meta: Metadata

    def __post_init__(self) -> None:
        """Validate Hub After creation."""
        if not self.name:
            raise ParseError("Hub name cannot be empty")
        if '-' in self.name or ' ' in self.name:
            raise ValidationError("Hub name cannot contain dashes.")
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise ValidationError("Hub x and y must be integer.")
        if self.meta is None:
            self.meta = Metadata()


@dataclass
class Net:
    """ Network structure """
    name1: str
    name2: str
    meta: Metadata

    def __post_init__(self) -> None:
        """ Check the network """
        if not self.name1 or not self.name2:
            raise ParseError("Connection Hub names canot be empty.")
        if self.name1 == self.name2:
            raise ValidationError("Connection cannot be the same hub.")
        if self.meta is None:
            self.meta = Metadata()


@dataclass
class Game:
    """Game structure that has data """
    nb_drones: int = 0
    s_hub: Optional[Hub] = None
    e_hub: Optional[Hub] = None
    hubs: Dict[str, Hub] = field(default_factory=dict)
    net: Dict[str, Net] = field(default_factory=dict)

    def all_hubs(self) -> Dict[str, dict]:
        """Return all hubs structure including start and end """
        res: Dict[str, dict] = dict(self.hubs)
        if self.s_hub:
            res[self.s_hub.name] = self.s_hub
        if self.e_hub:
            res[self.e_hub.name] = self.e_hub
        return res

    def all_names(self) -> Set[str]:
        """All known hub names."""
        return set(self.all_hubs().keys())

    def all_coords(self) -> set[tuple[int, int]]:
        """Return all used coordinates."""
        return {(hub.x, hub.y) for hub in self.all_hubs().values()}

    def check_dup_names(self) -> bool:
        """ Check names in the hubs """
        total = len(self.hubs)
        if self.s_hub:
            total += 1
        if self.e_hub:
            total += 1
        return len(self.all_names()) == total

    def check_corr(self) -> bool:
        """ Check duplicated corrdinates"""
        all_coor = list(self.all_hubs().values())
        coords = [(item.x, item.y) for item in all_coor]
        return len(coords) == len(set(coords))

    def check_game(self) -> bool:
        """ Check the format of the object """
        if self.s_hub is None or self.e_hub is None:
            return False
        if not self.check_dup_names() or not self.check_corr():
            return False
        if self.nb_drones <= 0:
            return False
        return True

    def get_neighbors(self, hub_name: Hub) -> List[Tuple[Hub, Net]]:
        """ get neighbors of a Hub"""
        neigbor = []
        if hub_name not in self.all_names():
            raise ValueError(f"Unknown hub: {hub_name}")
        all_hubs = self.all_hubs()

        for item in self.net.values():
            if item.name1 == hub_name:
                neigbor.append((all_hubs[item.name2], item))
            elif item.name2 == hub_name:
                neigbor.append((all_hubs[item.name1], item))
        return neigbor
