# Auther:   Nigel Harvey
# Purpose:  Be the runnable file that will go through the game sequence and call the modueles so that user can play minesweeper 


from ui import minesweeper_ui as ui
from data import constants
from logic import minesweeper_logic as logic
import pygame


def init_game(curr_screen):
    logic.nuke_generation(curr_screen.grid_width, curr_screen.grid_length, curr_screen.nukes, ui.Tile.last_used_tile_num, curr_screen.tile_list)
    ui.game_state = constants.IN_PROGRESS
    logic.reveal_tile(curr_screen.tile_list, ui.Tile.last_used_tile_coords, curr_screen.grid_width, curr_screen.grid_length, curr_screen)


def reset_game(curr_screen):
    # reset values for all tiles
    for row in curr_screen.tile_list:
        for tile in row:
            tile.revealed = False
            tile.flagged = False
            tile.nuke = False
            tile.colour = constants.GREY
            tile.hover_colour = constants.GREY_LIGHT
            tile.adj_nukes = 0
            tile.text = ""
            tile.text_colour = constants.BLACK
    curr_screen.revealed_safe = 0
    curr_screen.txt_game_result.text = ""
    ui.game_state = constants.WAITING
    return False


def game_over(curr_screen):
    # num of tiles
    total_safe_tiles = curr_screen.grid_width*curr_screen.grid_length - curr_screen.nukes

    # remove hover_colour
    for row in curr_screen.tile_list:
        for tile in row:
            if not tile.revealed:
                tile.hover_colour = tile.colour

    # Win condition
    if curr_screen.revealed_safe == total_safe_tiles:
        # show all nukes in flagged form
        for row in curr_screen.tile_list:
            for tile in row:
                if tile.nuke:
                    tile.flagged = True
        
        curr_screen.txt_game_result.text = "WIN!"
        print("You win!")
    # Lose condition
    else:
        # set coords to the last clicked tile, which would be the nuke clicked in this case
        x_coord, y_coord = ui.Tile.last_used_tile_coords

        # set tile colour and hover colour to RED
        curr_screen.tile_list[x_coord][y_coord].colour = constants.RED
        curr_screen.tile_list[x_coord][y_coord].hover_colour = constants.RED

        # show all nukes except flagged ones
        for row in curr_screen.tile_list:
            for tile in row:
                if tile.nuke:
                    tile.revealed = True

        print("GG LOSER")
        curr_screen.txt_game_result.text = "lose"
    print(f"Constant: {total_safe_tiles}. Revealed Safe Tiles: {curr_screen.revealed_safe}")

    return True


def play_game():
    pygame.init()

    # init screens and start in the menu
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
    end_game_reached = False
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

            # loop through the button list and check for events such as hovering or clicks
            for button in current_screen.button_list:
                button.handle_event(event)
            
            # if currently in a game (not the menu)
            if screen_state != constants.MENU:
                # loop through the tile list and check for events such as hovering or clicks
                for row in current_screen.tile_list:
                    for tile in row:
                        tile.handle_event(event)
                # if a game is in progress and a tile has just been clicked (this only runs immediately after a tile is clicked, and not again until a new tile is clicked)
                if (ui.game_state == constants.IN_PROGRESS) and (ui.Tile.last_used_tile_num != last_revealed_tile):
                    # if a bomb was clicked
                    if not logic.reveal_tile(current_screen.tile_list, ui.Tile.last_used_tile_coords, current_screen.grid_width, current_screen.grid_length, current_screen):
                        ui.game_state = constants.OVER
                    # if all safe tiles have been revealed
                    elif current_screen.revealed_safe == current_screen.grid_width*current_screen.grid_length - current_screen.nukes:
                        ui.game_state = constants.OVER
                # if the first tile has just been clicked
                elif ui.game_state == constants.INITIATING:
                    init_game(current_screen)
                # if the reset button is clicked
                elif ui.game_state == constants.RESET:
                    end_game_reached = reset_game(current_screen)
                # if a nuke is clicked or all safe tiles have been revealed
                elif ui.game_state == constants.OVER:
                    if not end_game_reached:
                        end_game_reached = game_over(current_screen)

        last_revealed_tile = ui.Tile.last_used_tile_num

        # draw all elements (buttons, textboxes, etc)
        current_screen.draw(screen)
        # finally, update the display
        pygame.display.update()


    # show screen with option to continue, which doesn't impede sight of the game


    # once continue is chosen, show scoreboard and leave buttons to exit or play again

if __name__ == "__main__":
    play_game()