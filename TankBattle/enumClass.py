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
    login = 0
    init = 1
    ready = 2
    start = 3
    levelChange = 4
    total = 5
    over = 6
    stop = 7

