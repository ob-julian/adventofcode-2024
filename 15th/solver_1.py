import os
import numpy as np
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    warehouse = []
    directions = ""
    is_map = True
    for line in lines:
        if line == "":
            is_map = False
            continue
        if is_map:
            warehouse.append(list(line))
        else:
            directions += line
    return warehouse, directions

def get_bot_position(warehouse):
    for y, row in enumerate(warehouse):
        for x, cell in enumerate(row):
            if cell == "@":
                warehouse [y][x] = "."
                return [x, y]

def move_bot_and_box(warehouse, position, direction):
    x, y = position
    og_x, og_y = [a + b for a, b in zip(position, direction)]
    add_x, add_y = direction
    if warehouse [y + add_y][x + add_x] == ".":
        return [x + add_x, y + add_y]
    while warehouse [y][x] != "#":
        x += add_x
        y += add_y
        if warehouse [y][x] == ".":
            warehouse [y][x] = "O"
            warehouse [og_y][og_x] = "."
            return [og_x, og_y]
    return position

def count_GPS_boxes(warehouse):
    count = 0
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            if cell == "O":
                count += i * 100 + j
    return count

DIRECTION = {
    "<": [-1, 0],
    ">": [1, 0],
    "^": [0, -1],
    "v": [0, 1]
}

def solver1(puzzle_input):
    warehouse, directions = puzzle_input
    position = get_bot_position(warehouse)
    for direction in directions:
        position = move_bot_and_box(warehouse, position, DIRECTION[direction])
    return count_GPS_boxes(warehouse)


FILE = "input.txt"
#FILE = "test.txt"

INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 13")
print("Solution for Part 1:", solver1(INPUT))
