from enum import Enum
from collections import namedtuple


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# UI
FOND_COLOR = (230, 230, 230)
TEXT_COLOR = (0, 0, 0)
FRUIT_COLOR = (200,0,0)
SNAKE_COLOR_BODY = (49, 220, 29)
SNAKE_COLOR_SHADOW = (34, 149, 21)
SNAKE_COLOR_EYES = (0, 50, 255)

# Game
BLOCK_SIZE = 20
SHADOW_SIZE = 4
SPEED = 1000

# Agent
POSITIVE_REWARD = 10
NEGATIVE_REWARD = -10

# Model
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
VITESSE_APPRENTISSAGE = 0.001
EPSILON_NB_GAMES = 100
HIDDEN_SIZE = 1024