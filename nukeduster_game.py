# Auther:   Nigel Harvey
# Purpose:  Be the runnable file that will go through the game sequence and
#           call the modules so that user can play minesweeper


from ui import minesweeper_ui as ui
from data import constants
from logic import minesweeper_logic as logic
import pygame
import time


def init_game(curr_screen):
    # generate nukes
    logic.nuke_generation(
        curr_screen.grid_width, curr_screen.grid_length, curr_screen.nukes, ui.Tile.last_used_tile_num, curr_screen.tile_list
    )

    # put the game state into IN_PROGRESS and start the timer
    ui.game_state = constants.IN_PROGRESS
    curr_screen.start_time = time.time()

    # reveal the first clicked tile
    logic.reveal_tile(
        curr_screen.tile_list, ui.Tile.last_used_tile_coords, curr_screen.grid_width, curr_screen.grid_length, curr_screen
    )


def reset_game(curr_screen):
    # reset values for all tiles
    for row in curr_screen.tile_list:
        for tile in row:
            tile.revealed = False
            tile.flagged = False
            tile.nuke = False
            tile.colour = constants.GREY
            # tile.hover_colour = constants.GREY_LIGHT
            tile.hover_colour = constants.GREY_DARK
            tile.adj_nukes = 0
            tile.text = ""
            tile.text_colour = constants.BLACK
    curr_screen.revealed_safe = 0
    curr_screen.txt_nuke_count.text = str(curr_screen.nukes)
    curr_screen.txt_game_result.text = ""
    curr_screen.txt_timer.text = "000"
    ui.game_state = constants.WAITING
    return True


def game_over(curr_screen):
    # num of tiles
    total_safe_tiles = curr_screen.grid_width*curr_screen.grid_length - curr_screen.nukes

    # remove hover_colour
    for list_row in curr_screen.tile_list:
        for tile in list_row:
            if not tile.revealed:
                tile.hover_colour = tile.colour

    # Win condition
    if curr_screen.revealed_safe == total_safe_tiles:
        # show all nukes in flagged form
        for row in curr_screen.tile_list:
            for tile in row:
                if tile.nuke:
                    tile.flagged = True
        
        curr_screen.txt_nuke_count.text = "0"
        curr_screen.txt_game_result.text = "WIN"

    # Lose condition
    else:
        # set coords to the last clicked tile, which would be the nuke clicked in this case
        x_coord, y_coord = ui.Tile.last_used_tile_coords

        # set the clicked nuke tile's colour and hover colour to RED
        curr_screen.tile_list[y_coord][x_coord].colour = constants.RED
        curr_screen.tile_list[y_coord][x_coord].hover_colour = constants.RED

        # show all nukes except flagged ones
        for row in curr_screen.tile_list:
            for tile in row:
                # if a tile is a nuke, reveal it
                if tile.nuke:
                    tile.revealed = True
                # if a tile is wrongly flagged, highlight it pink
                elif tile.flagged and not tile.nuke:
                    tile.colour = constants.PINK
                    tile.hover_colour = constants.PINK
        curr_screen.txt_game_result.text = "lose"

    return True


def play_game():
    # set player name
    player_name = input("\nPlease input your name: ")

    pygame.init()

    # init instances of screens and prepare to start in the menu_screen
    screen = pygame.display.set_mode((constants.MENU_WIDTH, constants.MENU_LENGTH))
    menu_screen = ui.MenuScreen(constants.MENU)
    easy_screen = ui.EasyScreen()
    medium_screen = ui.MediumScreen()
    hard_screen = ui.HardScreen()
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
    has_been_recorded = False
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
                for list_row in current_screen.tile_list:
                    for tile in list_row:
                        tile.handle_event(event, current_screen)

                # if a game is in progress and a tile has just been clicked
                # (this only runs immediately after a tile is clicked, and not again until a new tile is clicked)
                if (ui.game_state == constants.IN_PROGRESS) and (ui.Tile.last_used_tile_num != last_revealed_tile):
                    # if a nuke was clicked
                    if not logic.reveal_tile(
                        current_screen.tile_list, ui.Tile.last_used_tile_coords, current_screen.grid_width,
                        current_screen.grid_length, current_screen
                        ):
                        # set game state to over
                        ui.game_state = constants.OVER

                    # if all safe tiles have been revealed
                    elif (
                        current_screen.revealed_safe ==
                        current_screen.grid_width*current_screen.grid_length - current_screen.nukes
                        ):
                        # set game state to over
                        ui.game_state = constants.OVER

                # if the first tile has just been clicked
                elif ui.game_state == constants.INITIATING:
                    init_game(current_screen)
                # if the reset button is clicked
                elif ui.game_state == constants.RESET:
                    end_game_reached = not reset_game(current_screen)

                # if a nuke is clicked or all safe tiles have been revealed
                elif ui.game_state == constants.OVER:
                    if not end_game_reached:
                        end_game_reached = game_over(current_screen)
                        has_been_recorded = False

            # overwrite old last tile with new last tile
            last_revealed_tile = ui.Tile.last_used_tile_num

        # if currently in a game (not the menu)
        if screen_state != constants.MENU and ui.game_state != constants.OVER and ui.game_state != constants.WAITING:
            # update timer
            current_screen.time_played_s = time.time() - current_screen.start_time
            if int(current_screen.time_played_s/10) == 0:
                current_screen.txt_timer.text = "00" + str(int(current_screen.time_played_s))
            elif int(current_screen.time_played_s/100) == 0:
                current_screen.txt_timer.text = "0" + str(int(current_screen.time_played_s))
            elif int(current_screen.time_played_s/1000) == 0:
                current_screen.txt_timer.text = str(int(current_screen.time_played_s))

        # if in a game screen and the score hasn't been recorded yet (to prevent multiple writes)
        if screen_state != constants.MENU and not has_been_recorded:
            # if the game is over and the user won
            if ui.game_state == constants.OVER and current_screen.txt_game_result.text == "WIN":
                has_been_recorded = True
                print("Recording Data")
                file_path = 'data\log_game_scores.txt'

                try:
                    # with open(file_path, 'w', encoding='utf-8') as file:
                    with open(file_path, 'a') as file:
                        # store time values
                        current_struct_time = time.localtime()
                        year =  current_struct_time.tm_year
                        month = current_struct_time.tm_mon
                        day =   current_struct_time.tm_mday
                        hour =  current_struct_time.tm_hour
                        min =   current_struct_time.tm_min
                        if int(min/10) == 0:
                            min = "0" + str(min)

                        # write content to the file
                        string_to_write = f"{current_screen.mode_name}, {current_screen.txt_timer.text}, {player_name}, {hour}:{min}, {day} {month} {year}\n"
                        file.write(string_to_write)
                except FileNotFoundError:
                    print("File not found.")
                except PermissionError:
                    print("Permission denied to open the file.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        # draw all elements (buttons, textboxes, etc)
        current_screen.draw(screen)

        # finally, update the display
        pygame.display.update()


# if the nukeduster_game.py file is ran
if __name__ == "__main__":
    play_game()
