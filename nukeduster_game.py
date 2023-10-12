# Auther:   Nigel Harvey
# Purpose:  Be the runnable file that will go through the game sequence and call the modueles so that user can play minesweeper 


from ui import minesweeper_ui as ui
from data import constants
from logic import minesweeper_logic as logic
import pygame


def init_game(curr_screen):
    logic.nuke_generation(curr_screen.grid_width, curr_screen.grid_length, curr_screen.nukes, ui.Tile.last_used_tile_num, curr_screen.tile_list)
    ui.game_state = constants.IN_PROGRESS
    logic.reveal_tile(curr_screen.tile_list, ui.Tile.last_used_tile_coords, curr_screen.grid_width, curr_screen.grid_length)


def reset_game(curr_screen):
    for row in curr_screen.tile_list:
        for tile in row:
            tile.revealed = False
            tile.flagged = False
            tile.nuke = False
            tile.colour = constants.GREY
            tile.adj_nukes = 0
            tile.text = ""
            tile.text_colour = constants.BLACK  
    ui.game_state = constants.WAITING


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
    icon_nuke = pygame.image.load("data\\nuclear_bomb_32p.png")
    pygame.display.set_icon(icon_nuke)

    # loop until user presses close button or force closes with the "Quit" button
    running = True
    last_revealed_tile = None
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

            # draw all buttons, textboxes, etc
            current_screen.draw(screen)

            # loop through the button list and check for events such as hovering or clicks
            for button in current_screen.button_list:
                button.handle_event(event)
            if screen_state != constants.MENU:
                # loop through the tile list and check for events such as hovering or clicks
                for row in current_screen.tile_list:
                    for tile in row:
                        tile.handle_event(event)
                if ui.game_state == constants.IN_PROGRESS and (ui.Tile.last_used_tile_num != last_revealed_tile):
                    if not logic.reveal_tile(current_screen.tile_list, ui.Tile.last_used_tile_coords, current_screen.grid_width, current_screen.grid_length):
                        ui.game_state = constants.OVER
                elif ui.game_state == constants.INITIATING:
                    init_game(current_screen)
                elif ui.game_state == constants.RESET:
                    reset_game(current_screen)
                elif ui.game_state == constants.OVER:
                    # show all nukes and highlight the nuke that was clicked
                    x_coord, y_coord = ui.Tile.last_used_tile_coords
                    current_screen.tile_list[x_coord][y_coord].colour = constants.RED
                    for row in current_screen.tile_list:
                        for tile in row:
                            if tile.nuke:
                                tile.revealed = True

        last_revealed_tile = ui.Tile.last_used_tile_num

        # finally, update the display
        pygame.display.update()


    # show screen with option to continue, which doesn't impede sight of the game


    # once continue is chosen, show scoreboard and leave buttons to exit or play again
