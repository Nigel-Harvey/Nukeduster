# Auther:     Nigel Harvey
# Purpose:    Contain the logic and rules of the game in the form of functions and classes


import random
from data import constants


def right_click(revealed, game_state):
    if revealed:
        return False
    if game_state == 0 or game_state == 2:
        return False
    return True


def left_click(revealed, flagged, game_state):
    if revealed or flagged:
        return False
    if game_state == constants.OVER:
        return False
    return True


def nuke_generation(x_width_grid, y_width_grid, nukes_num, safe_tile_num, list_of_tiles):
    lis_potential_nuke_tiles = list(range(0, x_width_grid*y_width_grid))
    lis_potential_nuke_tiles.pop(safe_tile_num)
    lis_nukes = random.sample(lis_potential_nuke_tiles, nukes_num)
    for nuke_num in lis_nukes:
        column = nuke_num % y_width_grid
        row = (nuke_num - (column))/y_width_grid
        list_of_tiles[row][column].nuke = True


def reveal_tile(list_of_tiles, tile_column, tile_row):
    pass