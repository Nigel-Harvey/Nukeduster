from ui import minesweeper_ui as ui
from data import constants
from logic import minesweeper_logic as logic
import pygame

if __name__ == "__main__":
    pygame.init()

    # init menu screen
    screen = pygame.display.set_mode((constants.MENU_WIDTH, constants.MENU_LENGTH))
    menu_screen =   ui.MenuScreen(constants.MENU)
    easy_screen =   ui.EasyScreen(constants.EASY)
    medium_screen = ui.MediumScreen(constants.MEDIUM)
    hard_screen =   ui.HardScreen(constants.HARD)
    current_screen = menu_screen

    # set the window caption
    pygame.display.set_caption("Nukeduster - A Python Project")

    # load the window icon
    icon_nuke = pygame.image.load("Minesweeper\data\\nuclear_bomb.png")
    pygame.display.set_icon(icon_nuke)


    # loop until user presses close button or force closes with the "Quit" button
    running = True
    while running:
        # loop through all pygame events
        for event in pygame.event.get():
            # close game if close button is pressed
            if event.type == pygame.QUIT:
                running = False

            # chose which screen is in use
            screen_state = ui.screen_state
            match screen_state:
                case constants.MENU:
                    current_screen = menu_screen
                case constants.EASY:
                    current_screen = easy_screen
                case constants.MEDIUM:
                    current_screen = medium_screen
                case constants.HARD:
                    current_screen = hard_screen


            current_screen.draw(screen)            # draw all menu buttons, textboxes, etc
            # loop through the button list and check for events such as hovering or clicks
            for button in current_screen.button_list:
                button.handle_event(event)
            if screen_state != constants.MENU:
                # loop through the tile list and check for events such as hovering or clicks
                for row in current_screen.tile_list:
                    for tile in row:
                        tile.handle_event(event)

        pygame.display.update()                 # finally, update the display


    # show screen with option to continue, which doesn't impede sight of the game


    # once continue is chosen, show scoreboard and leave buttons to exit or play again