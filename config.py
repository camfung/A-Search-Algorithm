# config.py
from enum import Enum
# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BACKGROUND_COLOR = (3, 12, 23)  # Dark blue color

# Grid settings
SPOT_SIZE = 100
GRID_WIDTH = SCREEN_WIDTH // SPOT_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // SPOT_SIZE

# Additional settings
PASSAGE_WIDTH = 5
DEBUG = False
SHOW_OUTLINES = True
MAKE_BOARDER_WALLS = False


class SpotState(Enum):
    PATH = 1
    WALL = 2
    EMPTY = 3
    END = 4
    START = 5
