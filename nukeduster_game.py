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


# reveal the tile clicked and report if it was a nuke or if it was the last safe tile clicked
def reveal_evaluate(curr_screen):
    total_safe_tiles = curr_screen.grid_width*curr_screen.grid_length - curr_screen.nukes

    # if a nuke was clicked
    if not logic.reveal_tile(
    curr_screen.tile_list, ui.Tile.last_used_tile_coords, curr_screen.grid_width,
    curr_screen.grid_length, curr_screen):
        ui.game_state = constants.OVER

    # if all safe tiles have been revealed
    elif (curr_screen.revealed_safe == total_safe_tiles):
        ui.game_state = constants.OVER


# handle what happens when tiles are clicked
def handle_tile_events(curr_screen, event_type):
    for list_row in curr_screen.tile_list:
        for tile in list_row:
            tile.handle_tile_event(event_type)
            if tile.is_left_clicked:
                ui.left_click_action(tile)
            if tile.is_right_clicked:
                ui.right_click_action(tile, curr_screen)


# handle the event in the game that result from clicking buttons and tile updates
def handle_game_events(curr_screen, is_end_game, prev_revealed_tile, is_recorded):
# events are ordered in likeliness of occurring
    # if a game is in progress and a new tile has just been clicked
    if (ui.game_state == constants.IN_PROGRESS) and (ui.Tile.last_used_tile_num != prev_revealed_tile):
        reveal_evaluate(curr_screen)

    # if the reset button is clicked
    elif ui.game_state == constants.RESET:
        is_end_game = not reset_game(curr_screen)
        is_recorded = False
        return is_end_game, is_recorded

    # if the first tile has just been clicked
    elif ui.game_state == constants.INITIATING:
        init_game(curr_screen)

    # if a nuke is clicked or all safe tiles have been revealed
    elif ui.game_state == constants.OVER:
        if not is_end_game:
            is_end_game = game_over(curr_screen)
            # is_recorded = False

    return is_end_game, is_recorded


# update the timer in the GUI with the elapsed time
def update_timer(scrn_state, curr_screen):
        # if currently in a game -> leads to updating the timer
        if ((scrn_state == constants.EASY or scrn_state == constants.MEDIUM or scrn_state == constants.HARD) and 
            (ui.game_state == constants.INITIATING or ui.game_state == constants.IN_PROGRESS)):
            # update timer on the GUI
            curr_screen.time_played_s = time.time() - curr_screen.start_time
            if int(curr_screen.time_played_s/10) == 0:
                curr_screen.txt_timer.text = "00" + str(int(curr_screen.time_played_s))
            elif int(curr_screen.time_played_s/100) == 0:
                curr_screen.txt_timer.text = "0" + str(int(curr_screen.time_played_s))
            elif int(curr_screen.time_played_s/1000) == 0:
                curr_screen.txt_timer.text = str(int(curr_screen.time_played_s))


# record the player's score and name into the text file at file_pth
def record_player_data(file_pth, curr_screen, menu_scrn):
    print("Recording Data")
    try:
        # open the file and allow writing by appending a new line
        with open(file_pth, 'a') as file:
            # store time values
            current_struct_time = time.localtime()
            year =  current_struct_time.tm_year
            month = current_struct_time.tm_mon
            day =   current_struct_time.tm_mday
            hour =  current_struct_time.tm_hour
            min =   current_struct_time.tm_min

            # if the miniute is less than 10, convert it to a str with a leading '0'
            if int(min/10) == 0:
                min = "0" + str(min)

            # if the user didn't enter anything in the textbox, set to the default name
            if menu_scrn.tbox_e.text != "":
                menu_scrn.player_name = menu_scrn.tbox_e.text

            # Format:
            # <MODE>, <TIMER_SCORE>, <NAME>, <CURRENT TIME>, <CURRENT_DATE>
            # write content to the file
            string_to_write =   f"{curr_screen.mode_name}, {curr_screen.txt_timer.text}, " \
                                f"{menu_scrn.player_name}, {hour}:{min}, {day} {month} {year}\n"
            file.write(string_to_write)
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied to open the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return True


# go through the sequence that runs the game
def play_game():
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

    # define necessary variables
    is_running = True
    last_revealed_tile = None
    has_end_game_reached = False
    has_been_recorded = False

    # loop until user presses close button or force closes with the "Quit" button
    while is_running:
        # loop through all pygame events
        for event in pygame.event.get():
            # close game if close button is pressed
            if event.type == pygame.QUIT:
                is_running = False

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

            # loop through the current screen's button list and check for events such as hovering or clicks
            for button in current_screen.button_list:
                button.handle_event(event)

            # if currently in a game
            if screen_state == constants.EASY or screen_state == constants.MEDIUM or screen_state == constants.HARD:
                # loop through the tile list and check for events such as hovering or clicks
                handle_tile_events(current_screen, event)

                # depending on recent game update, take action, such as reveal tile
                has_end_game_reached, has_been_recorded = handle_game_events(   current_screen, has_end_game_reached, 
                                                                                last_revealed_tile, has_been_recorded)
            # if in the menu screen check for name box events
            elif screen_state == constants.MENU:
                current_screen.tbox_e.handle_event(event)

            # overwrite old last tile with new last tile
            last_revealed_tile = ui.Tile.last_used_tile_num

        # update the timer value in the GUI
        update_timer(screen_state, current_screen)

        # if in a game screen, the score hasn't been recorded, the game is over, and the user won
        if ((screen_state == constants.EASY or screen_state == constants.MEDIUM or screen_state == constants.HARD) and 
        not has_been_recorded and
        ui.game_state == constants.OVER and
        current_screen.txt_game_result.text == "WIN"):
            # record player score and data into the text file defined below
            file_path = 'data\log_game_scores.txt'
            has_been_recorded = record_player_data(file_path, current_screen, menu_screen)

        # draw all elements (buttons, textboxes, etc)
        current_screen.draw(screen)

        # finally, update the display
        pygame.display.update()


# if the nukeduster_game.py file is ran
if __name__ == "__main__":
    play_game()
