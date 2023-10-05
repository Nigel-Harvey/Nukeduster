# Colours
WHITE =         (255, 255, 255)
BLACK =         (0, 0, 0)
GREY_DARK =     (100, 100, 100)
GREY =          (150, 150, 150)
GREY_LIGHT =    (200, 200, 200)

PURPLE =        (83, 20, 120)
RED =           (255, 0, 0)
ORANGE =        (255, 128, 0)
BLUE =          (0, 0, 255)
BLUE_LIGHT =    (255, 102, 102)
YELLOW =        (255, 255, 0)
GREEN =         (0, 255, 0)
GREEN_DARK =    (0, 102, 0)
PINK =          (255, 0, 255)

# Screen states
MENU =      0
EASY =      1
MEDIUM =    2
HARD =      3

# Grid sizes (number of tiles)
EASY_GRID_WIDTH =       9
EASY_GRID_LENGTH =      9
MEDIUM_GRID_WIDTH =     16
MEDIUM_GRID_LENGTH =    16
HARD_GRID_WIDTH =       30
HARD_GRID_LENGTH =      16

# Number of nukes
EASY_NUKES =    10
MEDIUM_NUKES =  40
HARD_NUKES =    100

# Game states
STARTING =      0
IN_PROGRESS =   1
OVER =          2

# Screen sizes
MENU_WIDTH =    600
MENU_LENGTH =   800
#               space between the edge of the window and tiles + the # of tiles + an offset
#               no offset for WIDTH, 45 pixel on top and bottom for buttons and display
EASY_WIDTH =    2 + 27*EASY_GRID_WIDTH
EASY_LENGTH =   2 + 27*EASY_GRID_LENGTH + 45*2
MEDIUM_WIDTH =  2 + 27*MEDIUM_GRID_WIDTH
MEDIUM_LENGTH = 2 + 27*MEDIUM_GRID_LENGTH + 45*2
HARD_WIDTH =    2 + 27*HARD_GRID_WIDTH
HARD_LENGTH =   2 + 27*HARD_GRID_LENGTH + 45*2