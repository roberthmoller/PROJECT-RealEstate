from typing import Tuple

TRANSPARENT = 'none'
WHITE = 'white'
RED = 'red'
BLUE = 'blue'
GREEN = 'green'
YELLOW = 'yellow'
MAGENTA = 'magenta'


def rgba(r: int, g: int, b: int, a: float = 1) -> Tuple[float, float, float, float]:
    return r / 255, g / 255, b / 255, a


class ColorScheme:
    LOAN = rgba(0, 153, 76, .5)
    MAINTENANCE = rgba(0, 102, 204, .5)
    SAVINGS = rgba(204, 0, 102, .5)
    INTEREST = RED
    RENT = MAGENTA
