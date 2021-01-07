from enum import Enum


class Direction(Enum):
    right = 0
    left = 1
    up = 2
    down = 3


class MapType(Enum):
    null = 0
    brick = 1
    steel = 2
    seawater = 3
    grassland = 4
    snow = 5
    home = 6


class GameStep(Enum):
    init = 0
    ready = 1
    start = 2
    levelChange = 3
    over = 4
    stop = 5
