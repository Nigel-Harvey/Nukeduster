# Auther:     Nigel Harvey
# Purpose:    Contain the logic and rules of the game that the UI and game files can call upon


import random
from data import constants


def right_click(revealed, game_state_local):
    if revealed:
        return False
    if game_state_local != constants.IN_PROGRESS:
        return False
    return True


def left_click(revealed, flagged, game_state_local):
    # TODO make this inclusive instead of exclusive. Make it default return false
    # if not revealed and not flagged:
    #     return True
    if revealed or flagged:
        return False
    if game_state_local == constants.INITIATING or game_state_local == constants.OVER:
        return False
    return True


def nuke_generation(x_width_grid, y_width_grid, nukes_num, safe_tile_num, list_of_tiles):   
    lis_potential_nuke_tiles = list(range(0, x_width_grid*y_width_grid))    # generate a list of all tile nums
    lis_potential_nuke_tiles.pop(safe_tile_num)                             # remove the clicked tile from the list of tiles
    lis_nukes = random.sample(lis_potential_nuke_tiles, nukes_num)          # randomly pick a number of elements from the list equal to the total 
    # print(f"safe_tile_num: {safe_tile_num}")
    # print(f"lis_potential_nuke_tiles: {lis_potential_nuke_tiles}, \nlis_nukes: {lis_nukes}")
                                                                            # number of nukes desired and store the list of elements in lis_nukes
    # print("List of nukes: ", end="")
    for nuke_num in lis_nukes:                              # for each element in the list of nukes
        column = nuke_num % x_width_grid                    # find the column (x coord)
        row = int(nuke_num/x_width_grid)                    # find the row (y coord)
        # print(f"({column}, {row})", end=", ")
        list_of_tiles[row][column].nuke = True              # set the tile with those coords to be a nuke
        list_of_tiles[row][column].colour = constants.GREEN
    # print("")


def reveal_tile(list_of_tiles, tile_coords, grid_width, grid_length, curr_screen):
    # Set coordinates of current tile
    x_coord, y_coord = tile_coords

    # Set tile parameters to indicate it's been revealed
    list_of_tiles[y_coord][x_coord].revealed = True
    list_of_tiles[y_coord][x_coord].flagged = False
    list_of_tiles[y_coord][x_coord].colour = list_of_tiles[y_coord][x_coord].hover_colour

    # return False if it's a nuke
    if list_of_tiles[y_coord][x_coord].nuke:
        return False

    # Increment counter
    curr_screen.revealed_safe += 1
    print(f"Tile ({x_coord}, {y_coord}) is safe tile # \t{curr_screen.revealed_safe}")

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

    # if the tile has no adjacent nukes, use recursion to reveal adjacent tiles until the chunk is surrounded by tiles that have adjacent nukes
    if nuke_sum == 0:
        list_of_tiles[y_coord][x_coord].adj_nukes = 0       # Update tile attribute/parameter
        # reveal adjacent tiles to find their nuke sums
        # top
        if not edge_case[0]:
            # top left
            if (not edge_case[3]) and (list_of_tiles[y_coord-1][x_coord-1].revealed == 0):
                reveal_tile(list_of_tiles, (x_coord-1, y_coord-1), grid_width, grid_length, curr_screen)
            # top
            if (list_of_tiles[y_coord-1][x_coord].revealed == 0):
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
            if (list_of_tiles[y_coord+1][x_coord].revealed == 0):
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
    # TODO Check if this is the best method of doing this
    return True     # return True to reflect that the game is continuing
