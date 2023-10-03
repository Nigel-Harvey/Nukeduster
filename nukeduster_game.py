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
            if screen_state == constants.MENU:
                menu_screen.draw(screen)            # draw all menu buttons, textboxes, etc

                # loop through the button list and check for events such as hovering or clicks
                for button in menu_screen.button_list:
                    button.handle_event(event)

            elif screen_state == constants.EASY:
                ui.change_state(constants.MENU)

            elif ui.screen_state == constants.MEDIUM:
                pass
            
            elif ui.screen_state == constants.HARD:
                pass            


        pygame.display.update()                 # finally, update the display


    # show screen with option to continue, which doesn't impede sight of the game


    # once continue is chosen, show scoreboard and leave buttons to exit or play again