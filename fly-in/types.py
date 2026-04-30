from enum import Enum
from dataclasses import dataclass
from typing import List


class Zone(Enum):
    normal = 1
    blocked = 2
    restricted = 3
    priority = 4


@dataclass
class Metadata:
    zone: Zone
    color: str
    max_drones: int


@dataclass
class Hub:
    name: str
    x: int
    y: int
    meta: Metadata


@dataclass
class Net:
    name1: str
    name2: str
    meta: Metadata


class Game:
    nb_drones: int
    s_hub: Hub
    e_hub: Hub
    hubs = List[Hub]
    net = List[Net]
