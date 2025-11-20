"""
Game constants and configuration
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (135, 206, 235)  # Sky blue
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Pipe colors (Mario style)
PIPE_GREEN = (0, 180, 0)  # Main pipe green
PIPE_DARK_GREEN = (0, 120, 0)  # Darker green for borders
PIPE_RIM_COLOR = (0, 100, 0)  # Rim/cap color
PIPE_HIGHLIGHT = (50, 220, 50)  # Light green for highlights

# Bird settings
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_START_X = 150
BIRD_START_Y = 300
GRAVITY = 0.5
JUMP_STRENGTH = -8
BIRD_MAX_VELOCITY = 10
BIRD_IMAGE_PATH = "assets/images/bird.png"  # Path to bird image (optional)

# Pipe settings
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 3
PIPE_SPAWN_DISTANCE = 300
PIPE_MIN_HEIGHT = 100
PIPE_MAX_HEIGHT = 400
PIPE_HORIZONTAL_PADDING = 20  # Horizontal extension at pipe openings (manhole effect)

# Coin settings
COIN_SIZE = 30
COIN_SPAWN_OFFSET = 50  # Offset from pipe gap center
COIN_ROTATION_SPEED = 5
COIN_SPAWN_PROBABILITY = 0.6  # 60% chance to spawn a coin (0.0 to 1.0)

# Game settings
INITIAL_LIVES = 3
SCORE_INCREMENT = 1
COIN_SCORE = 10

# Font settings
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# Sound settings
COIN_SOUND_PATH = "assets/sounds/coin.wav"  # Path to coin collection sound
COLLISION_SOUND_PATH = "assets/sounds/collision.wav"  # Path to collision sound
BACKGROUND_MUSIC_PATH = "assets/sounds/background.wav"  # Path to background music

