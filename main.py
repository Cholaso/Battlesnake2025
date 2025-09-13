# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import heapq
from collections import deque
from enum import Enum
#from collections import deque

MAX_ROW = 15
MAX_COL = 15

class OccupiedType:
    EMPTY = 0
    FOOD = 1
    SNAKE_BODY = 2
    SNAKE_HEAD = 3

class Coord:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.occupiedType = OccupiedType.EMPTY # 0 = empty, 1 = food, 2 = snake body, 3 = snake head
        
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination

# Helper functions

def manhattan(a: Coord, b: Coord) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

def is_valid(row, col):
    return (row >= 0) and (row < MAX_ROW) and (col >= 0) and (col < MAX_COL)

# Check if a cell is unblocked
def is_unblocked(grid: list[Coord], row, col):
    return grid[row][col].occupiedType != 2 and grid[row][col].occupiedType != 3

# Check if a cell is the destination
def is_destination(row, col, dest: Coord):
    return row == dest.x and col == dest.y

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest: Coord):
    return ((row - dest.x) ** 2 + (col - dest.y) ** 2) ** 0.5

# IMPROVE THIS
def trace_path(cell_details, dest: Coord):
    path = []
    row = dest.x
    col = dest.y

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        nextS = Coord()
        nextS.x = row
        nextS.y = col
        path.append(nextS)
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Reverse the path to get the path from source to destination
    path.reverse()
    # for i in path:
        # print(i.x, ",", i.y, "->", end=" ")
    return path

# Implement the A* search algorithm
def a_star_search(grid, src: Coord, dest: Coord):
    # Check if the source and destination are valid
    if not is_valid(src.x, src.y) or not is_valid(dest.x, dest.y):
        # print("Source or destination is invalid")
        return None

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src.x, src.y) or not is_unblocked(grid, dest.x, dest.y):
        # print("Source or the destination is blocked")
        return None

    # Check if we are already at the destination
    if is_destination(src.x, src.y, dest):
        # print("We are already at the destination")
        return None

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(MAX_COL)] for _ in range(MAX_ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(MAX_COL)] for _ in range(MAX_ROW)]

    # Initialize the start cell details
    i = src.x
    j = src.y
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    found_dest = True
                    if len(path) >= 1:
                        return path[0]
                    return None
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        # print("Failed to find the destination cell")
        return None

def getHazards(game_state: typing.Dict):
    return game_state['board']['hazards']
def getSnakes(game_state: typing.Dict):
    return game_state['board']['snakes']
def getFood(game_state: typing.Dict):
    return game_state['board']['food']



def getBoardCoords(game_state: typing.Dict):
    board = []
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]
    pointerSnakes = 0
    pointerFood = 0

    for i in range(MAX_ROW):
        board.append([])
        for j in range(MAX_COL):
            tile = Coord()
            tile.x = i
            tile.y = j
            tile.occupiedType = OccupiedType.EMPTY
            board[i].append(tile)
    for snake in getSnakes(game_state):
        for segment in snake['body']:
            if segment == my_head:
                board[segment['x']][segment['y']].occupiedType = OccupiedType.EMPTY
            else:
                board[segment['x']][segment['y']].occupiedType = OccupiedType.SNAKE_BODY
    for food in getFood(game_state):
        board[food['x']][food['y']].occupiedType = OccupiedType.FOOD
    return board
#
    

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#0FEA8E",  # TODO: Choose color
        "head": "all-seeing",  # TODO: Choose head
        "tail": "mlh-gene",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] <= 0:
        is_move_safe["left"] = False

    elif my_head["x"] >= board_width - 1:
        is_move_safe["right"] = False

    elif my_head["y"] >= board_height - 1:
        is_move_safe["up"] = False

    elif my_head["y"] <= 0:
        is_move_safe["down"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    for snake in game_state['board']['snakes']:
        snake_body = snake['body']
        for segment in snake_body:
            if (segment['x'] == my_head['x'] + 1) and (segment['y']
                                                       == my_head['y']):
                is_move_safe['right'] = False
            if (segment['x'] == my_head['x'] - 1) and (segment['y']
                                                       == my_head['y']):
                is_move_safe['left'] = False
            if (segment['x'] == my_head['x']) and (segment['y']
                                                   == my_head['y'] + 1):
                is_move_safe['up'] = False
            if (segment['x'] == my_head['x']) and (segment['y']
                                                   == my_head['y'] - 1):
                is_move_safe['down'] = False
    current_food = None
    current_distance = 1000
    next_step = None 
    
    sourcecoord = Coord()
    sourcecoord.x = my_head['x']
    sourcecoord.y = my_head['y']

    for food in game_state['board']['food']:
        foodcoord = Coord()
        foodcoord.x = food['x']
        foodcoord.y = food['y']
        foodcoord.occupiedType = OccupiedType.FOOD

        ns = a_star_search(getBoardCoords(game_state), sourcecoord, foodcoord)
        if ns != None:
            if manhattan(sourcecoord, foodcoord) < current_distance:
                for snake in game_state['board']['snakes']:
                    if snake['id'] != game_state['you']['id']:
                        head = Coord()
                        head.x = snake['head']['x']
                        head.y = snake['head']['y']
                        if manhattan(head, foodcoord) < manhattan(sourcecoord, foodcoord) or (manhattan(head, foodcoord) == manhattan(sourcecoord, foodcoord) and snake['length'] >= game_state['you']['length']):
                            # print("Another snake is closer to the food \n")
                            if ns.x == foodcoord.x and ns.y == foodcoord.y:
                                # print("Next step is the food \n")
                                if (ns.x == my_head['x'] + 1) and (ns.y
                                            == my_head['y']):
                                    is_move_safe['right'] = False
                                if (ns.x == my_head['x'] - 1) and (ns.y
                                                                            == my_head['y']):
                                    is_move_safe['left'] = False
                                if (ns.x == my_head['x']) and (ns.y
                                                                        == my_head['y'] + 1):
                                    is_move_safe['up'] = False
                                if (ns.x == my_head['x']) and (ns.y
                                                                        == my_head['y'] - 1):
                                    is_move_safe['down'] = False
                            next_step = None
                            break
                        else:
                            current_distance = manhattan(sourcecoord, foodcoord)
                            current_food = foodcoord
                            next_step = ns
            
           
        # else:
            # print("No path found to food \n")

    if current_food != None and next_step != None:
        # print(f"\nCurrent food: {current_food.x}, {current_food.y} \nNext step: {next_step.x}, {next_step.y}\n Current Pos: {sourcecoord.x}, {sourcecoord.y}")
        is_move_safe = {"up": False, "down": False, "left": False, "right": False}
        if (next_step.x == my_head['x'] + 1) and (next_step.y
                                                    == my_head['y']):
            is_move_safe['right'] = True
        if (next_step.x == my_head['x'] - 1) and (next_step.y
                                                    == my_head['y']):
            is_move_safe['left'] = True
        if (next_step.x == my_head['x']) and (next_step.y
                                                == my_head['y'] + 1):
            is_move_safe['up'] = True
        if (next_step.x == my_head['x']) and (next_step.y
                                                == my_head['y'] - 1):
            is_move_safe['down'] = True

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        # print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    # print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
    


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
    