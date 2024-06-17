# Auther:   Nigel Harvey
# Purpose:  Module that will create the game window in which the user can play minesweeper 
#           using their mouse with the GUI to click and navigate through the game

import pygame
import sys
import csv
from data import constants
from logic import minesweeper_logic as logic
from .ui_button import Button
from .ui_textbox import TextBox
from .ui_tile import Tile
from .ui_tbox_edit import TBoxEdit


global screen_state
screen_state = constants.MENU


def change_screen_state(new_state):
    global screen_state
    screen_state = new_state


global game_state
game_state = constants.WAITING  # start with game-state = 0, which is waiting mode


def change_game_state(new_state):
    global game_state
    game_state = new_state


def left_click_action(tile):
    # run through logic to see if the tile_reveal function should be called
    global game_state
    if logic.is_revealable(tile.revealed, tile.flagged, game_state):
        # if the game hasn't begun then set it to INITIATING after the first left click on a tile
        if game_state == constants.WAITING:
            game_state = constants.INITIATING

        # store the previously clicked tile
        # (to help decide when tiles should be revealed and prevents multiple reveals of the same tile)
        Tile.last_used_tile_num = tile.tile_num
        Tile.last_used_tile_coords = tile.tile_num_x, tile.tile_num_y
    tile.is_left_clicked = False


def right_click_action(tile, current_screen_fn):
    if logic.is_flaggable(tile.revealed, game_state):
        # toggle the flag
        tile.flagged = not tile.flagged

        # adjust the nuke count output
        if tile.flagged:
            current_screen_fn.txt_nuke_count.text = str(int(current_screen_fn.txt_nuke_count.text)-1)
        else:
            current_screen_fn.txt_nuke_count.text = str(int(current_screen_fn.txt_nuke_count.text)+1)
    tile.is_right_clicked = False


# define all the actions that different buttons have
def difficulty_easy_action():
    change_screen_state(constants.EASY)
    pygame.display.set_mode((constants.EASY_WIDTH, constants.EASY_LENGTH))


def difficulty_medium_action():
    change_screen_state(constants.MEDIUM)
    pygame.display.set_mode((constants.MEDIUM_WIDTH, constants.MEDIUM_LENGTH))


def difficulty_hard_action():
    change_screen_state(constants.HARD)
    pygame.display.set_mode((constants.HARD_WIDTH, constants.HARD_LENGTH))


def quit_action():
    pygame.quit()
    sys.exit()


def scor_action():
    change_screen_state(constants.SCORE)
    pygame.display.set_mode((constants.SCORE_WIDTH, constants.SCORE_LENGTH))


def reset_action():
    change_game_state(constants.RESET)


def menu_action():
    change_screen_state(constants.MENU)
    pygame.display.set_mode((constants.MENU_WIDTH, constants.MENU_LENGTH))

    # reset if the player goes from the game to the menu
    reset_action()


class MenuScreen:
    def __init__(self, screen_type):
        self.screen_type = screen_type
        self.player_name = "Player"

        # create UI elements for the menu screen
        self.button_list = []
        self.but_difficulty_easy = Button(100, 690, 100, 50, "Easy", constants.WHITE, constants.GREY, difficulty_easy_action)
        self.but_difficulty_medium = Button(250, 690, 100, 50, "Medium", constants.WHITE, constants.GREY, difficulty_medium_action)
        self.but_difficulty_hard = Button(400, 690, 100, 50, "Hard", constants.WHITE, constants.GREY, difficulty_hard_action)
        self.but_quit = Button(510, 760, 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)

        scor_width = 150
        scor_offset = constants.MENU_WIDTH/2 - scor_width/2
        self.but_scor = Button(scor_offset, 475, scor_width, 50, "Scoreboard", constants.WHITE, constants.GREY, scor_action)

        self.button_list += self.but_difficulty_easy, self.but_difficulty_medium, self.but_difficulty_hard, self.but_quit, self.but_scor

        self.txt_welcome = TextBox(200, 25, "Welcome to", 50, constants.WHITE)
        self.txt_nuke_duster = TextBox(200, 75, "Nukeduster", 64)
        self.txt_name = TextBox(200, 25, "Enter Name:", 50, constants.WHITE)
        self.txt_welcome.set_position((constants.MENU_WIDTH - self.txt_welcome.width) / 2, 35)
        self.txt_nuke_duster.set_position((constants.MENU_WIDTH - 240) / 2, 85)
        self.txt_name.set_position((constants.MENU_WIDTH)/2 - self.txt_name.width/2, 550)

        self.tbox_e = TBoxEdit((constants.MENU_WIDTH)/2 - 300/2, 600, 300, 50)

        self.img_nuke = pygame.image.load("data/nuclear_bomb_256p.png")

    def draw(self, game_screen):
        game_screen.fill(constants.PURPLE)           # sets the screen fill and overwrites other things

        self.but_difficulty_easy.draw(game_screen)
        self.but_difficulty_medium.draw(game_screen)
        self.but_difficulty_hard.draw(game_screen)
        self.but_quit.draw(game_screen)

        self.but_scor.draw(game_screen)

        self.txt_welcome.draw(game_screen)
        self.txt_nuke_duster.draw(game_screen)
        self.txt_name.draw(game_screen)
        self.tbox_e.draw(game_screen)

        game_screen.blit(self.img_nuke, (constants.MENU_WIDTH/2 - 256/2, 200))
        # game_screen.blit(self.img_nuke, (45, 150))


class DifficultyScreen:
    def __init__(self):
        self.revealed_safe = 0      # all screens start with the same num of safe revealed tiles, which starts at 0
        self.start_time = 0         # all screens start with the same start time, which starts at 0
        self.time_played_s = 0      # all screens start with the same time played, which starts at 0

    def draw(self, game_screen, colour, textbox_list=None):
        game_screen.fill(colour)    # sets the screen fill (colour) and overwrites evrything

        # draw button updates
        for button in self.button_list:
            button.draw(game_screen)

        # draw tile updates (where list_row represents which list to use, which is equivalent to the y coord)
        for list_row in self.tile_list:
            for tile in list_row:
                tile.draw(game_screen)

        # draw textbox updates
        for textbox in textbox_list:
            textbox.draw(game_screen)


class EasyScreen(DifficultyScreen):
    def __init__(self):
        # inherit revealed_safe, start_time, time_played_s
        super().__init__()

        # define dimensions and settings
        self.grid_width = constants.EASY_GRID_WIDTH
        self.grid_length = constants.EASY_GRID_LENGTH
        self.screen_width = constants.EASY_WIDTH
        self.screen_length = constants.EASY_LENGTH
        self.nukes = constants.EASY_NUKES
        self.screen_colour = constants.GREEN_DARK
        self.mode_name = "Easy"

        # create Button instances and store all Button instances in button_list
        self.but_menu = Button(10, self.screen_length - (30 + 10), 80, 30, "Menu", constants.WHITE, constants.GREY, menu_action)
        self.but_quit = Button(self.screen_width - (80 + 10), self.screen_length - (30 + 10), 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.but_reset = Button(self.screen_width/2 - 40, 10, 80, 30, "Reset", constants.WHITE, constants.GREY, reset_action)
        self.button_list = []
        self.button_list += self.but_menu, self.but_quit, self.but_reset
        
        # create TextBox instances and store all TextBox instances in textbox_list
        self.txt_game_result = TextBox(80, 30, "", 36, constants.WHITE)
        self.txt_nuke_count = TextBox(80, 30, str(self.nukes), 36, constants.WHITE)
        self.txt_timer = TextBox(60, 30, "000", 36, constants.WHITE)
        self.txt_game_result.set_position(self.screen_width/2 - self.txt_game_result.length + 5, self.screen_length - (30 + 10))
        self.txt_nuke_count.set_position(20, 10)
        self.txt_timer.set_position(self.screen_width - self.txt_timer.width, 10)
        self.textbox_list = []
        self.textbox_list += self.txt_game_result, self.txt_nuke_count, self.txt_timer

        # set the screen_type which is used to change the screen_state when switching between screens
        self.screen_type = constants.EASY

        # generate Tile instances in a grid and store them in tile_list
        self.tile_list = logic.tile_generation(self.grid_width, self.grid_length, x_coord_offset=0, y_coord_offset=45)

    def draw(self, game_screen):
        super().draw(game_screen, self.screen_colour, self.textbox_list)


class MediumScreen(DifficultyScreen):
    def __init__(self):
        # inherit revealed_safe, start_time, time_played_s
        super().__init__()

        # define dimensions and settings
        self.grid_width = constants.MEDIUM_GRID_WIDTH
        self.grid_length = constants.MEDIUM_GRID_LENGTH
        self.screen_width = constants.MEDIUM_WIDTH
        self.screen_length = constants.MEDIUM_LENGTH
        self.nukes = constants.MEDIUM_NUKES
        self.screen_colour = constants.ORANGE
        self.mode_name = "Medium"

        # create Button instances and store all Button instances in button_list
        self.but_menu = Button(10, self.screen_length - (30 + 10), 80, 30, "Menu", constants.WHITE, constants.GREY, menu_action)
        self.but_quit = Button(self.screen_width - (80 + 10), self.screen_length - (30 + 10), 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.but_reset = Button(self.screen_width/2 - 40, 10, 80, 30, "Reset", constants.WHITE, constants.GREY, reset_action)
        self.button_list = []
        self.button_list += self.but_menu, self.but_quit, self.but_reset
        
        # create TextBox instances and store all TextBox instances in textbox_list
        self.txt_game_result = TextBox(80, 30, "", 36, constants.WHITE)
        self.txt_nuke_count = TextBox(80, 30, str(self.nukes), 36, constants.WHITE)
        self.txt_timer = TextBox(60, 30, "000", 36, constants.WHITE)
        self.txt_game_result.set_position(self.screen_width/2 - self.txt_game_result.length + 5, self.screen_length - (30 + 10))
        self.txt_nuke_count.set_position(20, 10)
        self.txt_timer.set_position(self.screen_width - self.txt_timer.width, 10)
        self.textbox_list = []
        self.textbox_list += self.txt_game_result, self.txt_nuke_count, self.txt_timer

        # set the screen_type which is used to change the screen_state when switching between screens
        self.screen_type = constants.MEDIUM

        # generate Tile instances in a grid and store them in tile_list
        self.tile_list = logic.tile_generation(self.grid_width, self.grid_length, x_coord_offset=0, y_coord_offset=45)

    def draw(self, game_screen):
        super().draw(game_screen, self.screen_colour, self.textbox_list)


class HardScreen(DifficultyScreen):
    def __init__(self):
        # inherit revealed_safe, start_time, time_played_s
        super().__init__()

        # define dimensions and settings
        self.grid_width = constants.HARD_GRID_WIDTH
        self.grid_length = constants.HARD_GRID_LENGTH
        self.screen_width = constants.HARD_WIDTH
        self.screen_length = constants.HARD_LENGTH
        self.nukes = constants.HARD_NUKES
        self.screen_colour = constants.RED_DARK
        self.mode_name = "Hard"

        # create Button instances and store all Button instances in button_list
        self.but_menu = Button(10, self.screen_length - (30 + 10), 80, 30, "Menu", constants.WHITE, constants.GREY, menu_action)
        self.but_quit = Button(self.screen_width - (80 + 10), self.screen_length - (30 + 10), 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.but_reset = Button(self.screen_width/2 - 40, 10, 80, 30, "Reset", constants.WHITE, constants.GREY, reset_action)
        self.button_list = []
        self.button_list += self.but_menu, self.but_quit, self.but_reset

        # create TextBox instances and store all TextBox instances in textbox_list
        self.txt_game_result = TextBox(80, 30, "", 36, constants.WHITE)
        self.txt_nuke_count = TextBox(80, 30, str(self.nukes), 36, constants.WHITE)
        self.txt_timer = TextBox(60, 30, "000", 36, constants.WHITE)
        self.txt_game_result.set_position(self.screen_width/2 - self.txt_game_result.length + 5, self.screen_length - (30 + 10))
        self.txt_nuke_count.set_position(20, 10)
        self.txt_timer.set_position(self.screen_width - self.txt_timer.width, 10)
        self.textbox_list =  []
        self.textbox_list += self.txt_game_result, self.txt_nuke_count, self.txt_timer

        # set the screen_type which is used to change the screen_state when switching between screens
        self.screen_type = constants.HARD

        # generate Tile instances in a grid and store them in tile_list
        self.tile_list = logic.tile_generation(self.grid_width, self.grid_length, x_coord_offset=0, y_coord_offset=45)

    def draw(self, game_screen):
        super().draw(game_screen, self.screen_colour, self.textbox_list)


class ScorScreen:
    def __init__(self):
        # define dimensions and settings
        self.screen_width = constants.SCORE_WIDTH
        self.screen_length = constants.SCORE_LENGTH
        # self.screen_colour = constants.BLUE
        self.screen_colour = constants.GREEN_DARK

        # NOTE: Mode may be unneccesary
        self.mode = "Easy"   # set default mode to Easy

        # create Button instances and store all Button instances in button_list
        self.but_menu = Button(10, self.screen_length - (30 + 10), 80, 30, "Menu", constants.WHITE, constants.GREY, menu_action)
        self.but_quit = Button(self.screen_width - (80 + 10), self.screen_length - (30 + 10), 80, 30, "Quit", constants.WHITE, constants.GREY, quit_action)
        self.but_easy_scor = Button(100, 690, 100, 50, "Easy", constants.WHITE, constants.GREY, self.easy_scor_action)
        self.but_medium_scor = Button(250, 690, 100, 50, "Medium", constants.WHITE, constants.GREY, self.medium_scor_action)
        self.but_hard_scor = Button(400, 690, 100, 50, "Hard", constants.WHITE, constants.GREY, self.hard_scor_action)
        
        self.button_list = []
        self.button_list += self.but_menu, self.but_quit, self.but_easy_scor, self.but_medium_scor, self.but_hard_scor
        
        # create TextBox instances and store all TextBox instances in textbox_list
        self.textbox_list = []

        self.txt_leader = TextBox(250, 25, "Leaderboard", 64, constants.WHITE)
        self.txt_leader.set_position((self.screen_width - self.txt_leader.width) / 2, 35)
        self.textbox_list.append(self.txt_leader)
        
        self.txt_mode = TextBox(100, 75, self.mode, 50, constants.WHITE)
        self.txt_mode.set_position(50, 85)
        self.textbox_list.append(self.txt_mode)

        for placement in range(1, 11):
            var_name = f"txt_place{placement}"
            textbox = TextBox(300, 75, f"{placement}", 50, constants.WHITE)
            textbox.set_position(50, 85 + 50*placement)
            setattr(self, var_name, textbox)
            self.textbox_list.append(textbox)

            var_name = f"txt_name{placement}"
            textbox = TextBox(300, 75, "", 40, constants.WHITE)
            textbox.set_position(120, 85 + 50*placement)
            setattr(self, var_name, textbox)
            self.textbox_list.append(textbox)

            var_name = f"txt_score{placement}"
            textbox = TextBox(300, 75, "", 40, constants.WHITE)
            textbox.set_position(400, 85 + 50*placement)
            setattr(self, var_name, textbox)
            self.textbox_list.append(textbox)

            var_name = f"txt_date{placement}"
            textbox = TextBox(300, 75, "", 40, constants.WHITE)
            textbox.set_position(450, 85 + 50*placement)
            setattr(self, var_name, textbox)
            self.textbox_list.append(textbox)

        # set the screen_type which is used to change the screen_state when switching between screens
        self.screen_type = constants.SCORE


    def draw(self, game_screen):
        game_screen.fill(self.screen_colour)    # sets the screen fill (colour) and overwrites evrything

        # draw button updates
        for button in self.button_list:
            button.draw(game_screen)

        # draw textbox updates
        for textbox in self.textbox_list:
            textbox.draw(game_screen)


    def easy_scor_action(self):
        self.screen_colour = constants.GREEN_DARK
        self.txt_mode.text = "Easy"
        csv_scores_easy = 'data/easy_scores_sorted.csv'
        with open(csv_scores_easy, mode='r', newline='') as file:
            reader = csv.reader(file)
            row_count = 0
            top_10 = []
            for row in reader:
                if row_count < 10:
                    top_10.append(row)
                    row_count += 1
                else:
                    break  # Exit the loop after reading 10 rows
            self.txt_name1.text = top_10[0][2]
            self.txt_score1.text = top_10[0][1]
            self.txt_date1.text = top_10[0][4]
            
            self.txt_name2.text = top_10[1][2]
            self.txt_score2.text = top_10[1][1]
            self.txt_date2.text = top_10[1][4]

            self.txt_name3.text = top_10[2][2]
            self.txt_score3.text = top_10[2][1]
            self.txt_date3.text = top_10[2][4]

            self.txt_name4.text = top_10[3][2]
            self.txt_score4.text = top_10[3][1]
            self.txt_date4.text = top_10[3][4]

            self.txt_name5.text = top_10[4][2]
            self.txt_score5.text = top_10[4][1]
            self.txt_date5.text = top_10[4][4]

            self.txt_name6.text = top_10[5][2]
            self.txt_score6.text = top_10[5][1]
            self.txt_date6.text = top_10[5][4]

            self.txt_name7.text = top_10[6][2]
            self.txt_score7.text = top_10[6][1]
            self.txt_date7.text = top_10[6][4]

            self.txt_name8.text = top_10[7][2]
            self.txt_score8.text = top_10[7][1]
            self.txt_date8.text = top_10[7][4]

            self.txt_name9.text = top_10[8][2]
            self.txt_score9.text = top_10[8][1]
            self.txt_date9.text = top_10[8][4]

            self.txt_name10.text = top_10[9][2]
            self.txt_score10.text = top_10[9][1]
            self.txt_date10.text = top_10[9][4]

    def medium_scor_action(self):
        self.screen_colour = constants.ORANGE
        self.txt_mode.text = "Medium"
        csv_scores_easy = 'data/med_scores_sorted.csv'
        with open(csv_scores_easy, mode='r', newline='') as file:
            reader = csv.reader(file)
            row_count = 0
            top_10 = []
            for row in reader:
                if row_count < 10:
                    top_10.append(row)
                    row_count += 1
                else:
                    break  # Exit the loop after reading 10 rows
            self.txt_name1.text = top_10[0][2]
            self.txt_score1.text = top_10[0][1]
            self.txt_date1.text = top_10[0][4]
            
            self.txt_name2.text = top_10[1][2]
            self.txt_score2.text = top_10[1][1]
            self.txt_date2.text = top_10[1][4]

            self.txt_name3.text = top_10[2][2]
            self.txt_score3.text = top_10[2][1]
            self.txt_date3.text = top_10[2][4]

            self.txt_name4.text = top_10[3][2]
            self.txt_score4.text = top_10[3][1]
            self.txt_date4.text = top_10[3][4]

            self.txt_name5.text = top_10[4][2]
            self.txt_score5.text = top_10[4][1]
            self.txt_date5.text = top_10[4][4]

            self.txt_name6.text = top_10[5][2]
            self.txt_score6.text = top_10[5][1]
            self.txt_date6.text = top_10[5][4]

            self.txt_name7.text = top_10[6][2]
            self.txt_score7.text = top_10[6][1]
            self.txt_date7.text = top_10[6][4]

            self.txt_name8.text = top_10[7][2]
            self.txt_score8.text = top_10[7][1]
            self.txt_date8.text = top_10[7][4]

            self.txt_name9.text = top_10[8][2]
            self.txt_score9.text = top_10[8][1]
            self.txt_date9.text = top_10[8][4]

            self.txt_name10.text = top_10[9][2]
            self.txt_score10.text = top_10[9][1]
            self.txt_date10.text = top_10[9][4]


    def hard_scor_action(self):
        self.screen_colour = constants.RED
        self.txt_mode.text = "Hard"
        csv_scores_easy = 'data/hard_scores_sorted.csv'
        with open(csv_scores_easy, mode='r', newline='') as file:
            reader = csv.reader(file)
            row_count = 0
            top_10 = []
            for row in reader:
                if row_count < 10:
                    top_10.append(row)
                    row_count += 1
                else:
                    break  # Exit the loop after reading 10 rows

            self.txt_name1.text = top_10[0][2]
            self.txt_score1.text = top_10[0][1]
            self.txt_date1.text = top_10[0][4]

            self.txt_name2.text = top_10[1][2]
            self.txt_score2.text = top_10[1][1]
            self.txt_date2.text = top_10[1][4]

            self.txt_name3.text = top_10[2][2]
            self.txt_score3.text = top_10[2][1]
            self.txt_date3.text = top_10[2][4]

            self.txt_name4.text = top_10[3][2]
            self.txt_score4.text = top_10[3][1]
            self.txt_date4.text = top_10[3][4]

            self.txt_name5.text = top_10[4][2]
            self.txt_score5.text = top_10[4][1]
            self.txt_date5.text = top_10[4][4]

            # NOTE need to change data type to dictionary to fix this. Only 5 scores logged rn
            # self.txt_name6.text = top_10[5][2]
            # self.txt_score6.text = top_10[5][1]
            # self.txt_date6.text = top_10[5][4]

            # self.txt_name7.text = top_10[6][2]
            # self.txt_score7.text = top_10[6][1]
            # self.txt_date7.text = top_10[6][4]

            # self.txt_name8.text = top_10[7][2]
            # self.txt_score8.text = top_10[7][1]
            # self.txt_date8.text = top_10[7][4]

            # self.txt_name9.text = top_10[8][2]
            # self.txt_score9.text = top_10[8][1]
            # self.txt_date9.text = top_10[8][4]

            # self.txt_name10.text = top_10[9][2]
            # self.txt_score10.text = top_10[9][1]
            # self.txt_date10.text = top_10[9][4]
