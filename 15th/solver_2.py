import os
import numpy as np
import keyboard
#pylint: disable=missing-function-docstring

# there is not mutch so salvage from the previous solution, so I decided to use a different file

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

REPLACEMENTS = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@."
}

def parser(lines):
    warehouse = []
    directions = ""
    is_map = True
    for line in lines:
        if line == "":
            is_map = False
            continue
        if is_map:
            for key, value in REPLACEMENTS.items():
                line = line.replace(key, value)
            warehouse.append(list(line))
        else:
            directions += line
    return warehouse, directions

def get_bot_position(warehouse):
    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell == "@":
                warehouse[y][x] = "."
                return [x, y]
    return None

def move_bot_and_box(warehouse, position, direction):
    x, y = position
    new_x, new_y = [a + b for a, b in zip(position, direction)]
    add_x, add_y = direction
    if warehouse [new_y][new_x] == ".":
        return [x + add_x, y + add_y]
    if warehouse [new_y][new_x] == "#":
        return position
    if add_x != 0:
        was_movable = move_big_box_sideways(warehouse, [new_x, new_y], add_x)
    else:
        was_movable, boxes = move_big_box_up_down(warehouse, [new_x, new_y], add_y)
        if was_movable:
            for box in boxes:
                warehouse [box[1]][box[0]] = "["
                warehouse [box[1]][box[0]+1] = "]"
                warehouse [box[1]-add_y][box[0]] = "."
                warehouse [box[1]-add_y][box[0]+1] = "."
    if was_movable:
        return [new_x, new_y]
    return position

def move_big_box_sideways(warehouse, position, add_x):
    x, y = position
    if warehouse [y][x] == "]":
        x -= 1
    og_x = x
    try:
        while warehouse [y][x] != "#":
            x += add_x
            if warehouse [y][x] == ".":
                while x != og_x - add_x:
                    warehouse [y][x] = warehouse [y][x - add_x]
                    x -= add_x
                warehouse [y][x] = "."
                return True
        return False
    except IndexError:
        print("side IndexError")
        return False

def move_big_box_up_down(warehouse, position, add_y):
    x, y = position
    if warehouse [y][x] == "]":
        x -= 1
    y += add_y

    try:
        if warehouse [y][x] == "." and warehouse [y][x+1] == ".":
            return True, [[x, y]]
        if warehouse [y][x] == "#" or warehouse [y][x+1] == "#":
            return False, []
        if warehouse [y][x] == "[":
            was_movable, boxes = move_big_box_up_down(warehouse, [x, y], add_y)
            if was_movable:
                return True, boxes + [[x, y]]
            return False, []
        if warehouse [y][x] == "]" or warehouse [y][x+1] == "[":
            if warehouse [y][x] == "]":
                was_movable_1, boxes_1 = move_big_box_up_down(warehouse, [x, y], add_y)
            elif warehouse [y][x] == ".":
                was_movable_1 = True
                boxes_1 = []
            else:
                return False, []
            if warehouse [y][x+1] == "[":
                was_movable_2, boxes_2 = move_big_box_up_down(warehouse, [x+1, y], add_y)
            elif warehouse [y][x+1] == ".":
                was_movable_2 = True
                boxes_2 = []
            else:
                return False, []
            if was_movable_1 and was_movable_2:
                return True, boxes_1 + boxes_2 + [[x, y]]
            return False, []

    except IndexError:
        print("up_down IndexError")
    return False, []

def count_GPS_boxes(warehouse):
    count = 0
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            if cell == "[":
                count += i * 100 + j
    return count

DIRECTION = {
    "<": [-1, 0],
    ">": [1, 0],
    "^": [0, -1],
    "v": [0, 1],
    "nach-links": [-1, 0],
    "nach-rechts": [1, 0],
    "nach-oben": [0, -1],
    "nach-unten": [0, 1]
}

def solver2(puzzle_input):
    warehouse, directions = puzzle_input
    position = get_bot_position(warehouse)
    for direction in directions:
        position = move_bot_and_box(warehouse, position, DIRECTION[direction])
    print_wharehouse(warehouse, position)
    return count_GPS_boxes(warehouse)

def print_wharehouse(warehouse, position, direction = None):
    if direction:
        print("Moving", direction)
    warehouse[position[1]][position[0]] = "@"
    string = "\n".join("".join(row) for row in warehouse)
    print(string)
    warehouse[position[1]][position[0]] = "."

FILE = "input.txt"
#FILE = "test.txt"

INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 13")
print("Solution for Part 2:", solver2(INPUT))

def interactive(puzzle_input):
    warehouse, _ = puzzle_input
    position = get_bot_position(warehouse)

    def on_arrow_key(event):
        nonlocal position
        if event.name in ['nach-links', 'nach-rechts', 'nach-oben', 'nach-unten']:
            direction = event.name
            position = move_bot_and_box(warehouse, position, DIRECTION[direction])
            print_wharehouse(warehouse, position)

    print("Press arrow keys to go around the warehouse, press 'Esc' to exit")
    print_wharehouse(warehouse, position)

    keyboard.on_press(on_arrow_key)

    # Keep the program running until the user presses 'Esc'
    keyboard.wait('esc')

#interactive(INPUT)
