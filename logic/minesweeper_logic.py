# Auther:     Nigel Harvey
# Purpose:    Contain the logic and rules of the game that the UI and game files can call upon


import random
from data import constants
from ui import ui_tile


def is_flaggable(is_revealed, game_state_local):
    # if the tile is not revealed and the game is in progress, allow a flag
    if not is_revealed and game_state_local == constants.IN_PROGRESS:
        return True
    return False


def is_revealable(is_revealed, is_flagged, game_state_local):
    # if the tile is not revealed and not flagged, and the game state is in progress or waiting, then allow a reveal 
    if ((not is_revealed and not is_flagged) and
        (game_state_local == constants.WAITING or game_state_local == constants.IN_PROGRESS)):
        return True
    return False


def nuke_generation(x_width_grid, y_width_grid, nukes_num, safe_tile_num, list_of_tiles):
    # generate the list of integers corresponding to which tiles will be nukes
    lis_potential_nuke_tiles = list(range(0, x_width_grid*y_width_grid))    # generate a list of all tile nums
    lis_potential_nuke_tiles.pop(safe_tile_num)                             # remove clicked tile from list of tiles
    lis_nukes = random.sample(lis_potential_nuke_tiles, nukes_num)          # randomly pick a num of elems from
                                                                            # the list equal to the total

    # number of nukes desired and store the list of elements in lis_nukes
    for nuke_num in lis_nukes:                              # for each element in the list of nukes
        column = nuke_num % x_width_grid                    # find the column (x coord)
        row = int(nuke_num/x_width_grid)                    # find the row (y coord))
        list_of_tiles[row][column].nuke = True              # set the tile with those coords to be a nuke


def reveal_tile(list_of_tiles, tile_coords, grid_width, grid_length, curr_screen):
    # Set coordinates of current tile
    x_coord, y_coord = tile_coords

    # Set tile parameters to indicate it's been revealed
    list_of_tiles[y_coord][x_coord].revealed = True
    list_of_tiles[y_coord][x_coord].flagged = False

    # keep tile colour constant as the reveal colour
    list_of_tiles[y_coord][x_coord].colour = list_of_tiles[y_coord][x_coord].reveal_colour
    list_of_tiles[y_coord][x_coord].hover_colour = list_of_tiles[y_coord][x_coord].reveal_colour

    # return False if it's a nuke
    if list_of_tiles[y_coord][x_coord].nuke:
        return False

    # Increment counter
    curr_screen.revealed_safe += 1

    # Check if the tile is on an edge (0 = top, 1 = right, 2 = bottom, 3 = left)
    edge_case = [False, False, False, False]
    if x_coord == 0:                    # left edge
        edge_case[3] = True
    elif x_coord == (grid_width-1):     # right edge
        edge_case[1] = True
    if y_coord == 0:                    # top edge
        edge_case[0] = True
    elif y_coord == (grid_length-1):    # bottom edge
        edge_case[2] = True

    # sum all nukes around the tile starting above and to the left and going clockwise
    nuke_sum = 0
    # top
    if not edge_case[0]:
        # top left
        if not edge_case[3]:
            if list_of_tiles[y_coord-1][x_coord-1].nuke:
                nuke_sum += 1
        # top
        if list_of_tiles[y_coord-1][x_coord].nuke:
            nuke_sum += 1
        # top right
        if not edge_case[1]:
            if list_of_tiles[y_coord-1][x_coord+1].nuke:
                nuke_sum += 1
    # right
    if not edge_case[1]:
        if list_of_tiles[y_coord][x_coord+1].nuke:
            nuke_sum += 1
    # bottom
    if not edge_case[2]:
        # bottom right
        if not edge_case[1]:
            if list_of_tiles[y_coord+1][x_coord+1].nuke:
                nuke_sum += 1
        # bottom
        if list_of_tiles[y_coord+1][x_coord].nuke:
            nuke_sum += 1
        # bottom left
        if not edge_case[3]:
            if list_of_tiles[y_coord+1][x_coord-1].nuke:
                nuke_sum += 1
    # left
    if not edge_case[3]:
        if list_of_tiles[y_coord][x_coord-1].nuke:
            nuke_sum += 1

    # if the tile has no adjacent nukes, use recursion to reveal adj tiles until surrounded by tiles that have adj nukes
    if nuke_sum == 0:
        list_of_tiles[y_coord][x_coord].adj_nukes = 0       # Update tile attribute/parameter
        # reveal adjacent tiles to find their nuke sums
        # top
        if not edge_case[0]:
            # top left
            if (not edge_case[3]) and (list_of_tiles[y_coord-1][x_coord-1].revealed == 0):
                reveal_tile(list_of_tiles, (x_coord-1, y_coord-1), grid_width, grid_length, curr_screen)
            # top
            if list_of_tiles[y_coord-1][x_coord].revealed == 0:
                reveal_tile(list_of_tiles, (x_coord, y_coord-1), grid_width, grid_length, curr_screen)
            # top right
            if (not edge_case[1]) and (list_of_tiles[y_coord-1][x_coord+1].revealed == 0):
                reveal_tile(list_of_tiles, (x_coord+1, y_coord-1), grid_width, grid_length, curr_screen)
        # bottom
        if not edge_case[2]:
            # bottom right
            if (not edge_case[1]) and (list_of_tiles[y_coord+1][x_coord+1].revealed == 0):
                reveal_tile(list_of_tiles, (x_coord+1, y_coord+1), grid_width, grid_length, curr_screen)
            # bottom
            if list_of_tiles[y_coord+1][x_coord].revealed == 0:
                reveal_tile(list_of_tiles, (x_coord, y_coord+1), grid_width, grid_length, curr_screen)
            # bottom left
            if (not edge_case[3]) and (list_of_tiles[y_coord+1][x_coord-1].revealed == 0):
                reveal_tile(list_of_tiles, (x_coord-1, y_coord+1), grid_width, grid_length, curr_screen)
        # right
        if not edge_case[1] and (list_of_tiles[y_coord][x_coord+1].revealed == 0):
            reveal_tile(list_of_tiles, (x_coord+1, y_coord), grid_width, grid_length, curr_screen)
        # left
        if not edge_case[3] and (list_of_tiles[y_coord][x_coord-1].revealed == 0):
            reveal_tile(list_of_tiles, (x_coord-1, y_coord), grid_width, grid_length, curr_screen)

    # if there is more than 0 adjacent nukes for the current tile instance
    else:
        list_of_tiles[y_coord][x_coord].adj_nukes = nuke_sum    # set attribute/parameter

    return True     # return True to reflect that the game is continuing


def tile_generation(x_tiles, y_tiles, x_coord_offset=0, y_coord_offset=0):
    # generate a 2D list to store all the tile objects
    tile_list = [[0 for i in range(x_tiles)] for j in range(y_tiles)]

    # generate all the tile objects
    y_coord = constants.SPACE_BETWEEN_TILES + y_coord_offset            # init the y coordinate with an offset of 2 pixels + a set offset purely for visuals
    for list_row in range(y_tiles):                                     # loop through all list_row, which are represented by y
        x_coord = constants.SPACE_BETWEEN_TILES + x_coord_offset        # init the x coordinate with an offset of 2 pixels + a set offset purely for visuals
        for row_element in range(x_tiles):                              # loop through all row_elements, which are represented by x
            # store a Tile instance in the tile_list list at the correct index
            tile_list[list_row][row_element] = ui_tile.Tile(
                                                    x_coord, y_coord, constants.TILE_WIDTH, constants.TILE_WIDTH, 
                                                    constants.GREY, constants.GREY_DARK, constants.GREY_LIGHT,
                                                    (row_element + list_row*x_tiles), row_element, list_row)
            x_coord += constants.SPACE_BETWEEN_TILES + constants.TILE_WIDTH     # increase the x coordinate so that tiles don't overlap
        y_coord += constants.SPACE_BETWEEN_TILES + constants.TILE_WIDTH         # increase the y coordinate so that tiles don't overlap
    return tile_list
