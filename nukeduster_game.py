from ui import minesweeper_ui as ui
from data import constants
from logic import minesweeper_logic as logic
import pygame

if __name__ == "__main__":
    pygame.init()

    # open game window
    screen = pygame.display.set_mode((constants.MENU_WIDTH, constants.MENU_LENGTH))
    
    # set the window caption
    pygame.display.set_caption("Nukeduster - A Python Project")

    # load the window icon
    dir_data = "Minesweeper\data\\"
    icon_nuke = pygame.image.load(dir_data + "nuclear_bomb.png")
    pygame.display.set_icon(icon_nuke)

    # let user input name and select difficulty
    button_list = []
    but_difficulty_easy =   ui.Button(100, 675, 100, 50, "Easy", constants.WHITE, constants.GREY, ui.difficulty_easy_action)
    but_difficulty_medium = ui.Button(250, 675, 100, 50, "Medium", constants.WHITE, constants.GREY, ui.difficulty_medium_action)
    but_difficulty_hard =   ui.Button(400, 675, 100, 50, "Hard", constants.WHITE, constants.GREY, ui.difficulty_hard_action)
    but_quit =              ui.Button(530, 760, 60, 30, "Quit", constants.WHITE, constants.GREY, ui.quit_action)
    txt_welcome =           ui.TextBox(200, 50, "Welcome to", 50, constants.WHITE)
    txt_nuke_duster =       ui.TextBox(200, 100, "Nukeduster", 64)

    txt_welcome.set_position((constants.MENU_WIDTH - txt_welcome.width) / 2, 50)
    txt_nuke_duster.set_position((constants.MENU_WIDTH - 240) / 2, 100)
    
    img_nuke = pygame.image.load(dir_data + "nuclear-bomb.png")

    button_list += but_difficulty_easy, but_difficulty_medium, but_difficulty_hard, but_quit

    # set new window based on difficulty chosen


    # load in game data and set clock to 0


    # wait for first click, then start the clock


    # loop through game logic until "Game Over" through either winning or losing
    running = True
    print(f"screen Type: {type(screen)}")
    while running:
        # close game is close button is pressed
        for event in pygame.event.get():        # loop through all pygame events
            if event.type == pygame.QUIT:       # if the close button is pressed
                running = False

            for button in button_list:
                button.handle_event(event)

        screen.fill(constants.PURPLE)           # sets the screen fill and overwrites other things


        but_difficulty_easy.draw(screen)
        but_difficulty_medium.draw(screen)
        but_difficulty_hard.draw(screen)
        but_quit.draw(screen)
        txt_welcome.draw(screen)
        txt_nuke_duster.draw(screen)
        screen.blit(img_nuke, (45, 150))


        pygame.display.update()                 # finally, update the display

    # show screen with option to continue, which doesn't impede sight of the game


    # once continue is chosen, show scoreboard and leave buttons to exit or play again