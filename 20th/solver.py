import os
import heapq
import numpy as np
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    result = []
    for line in lines:
        result.append(list(line))
    return result

# up left down right
# N, W, S, E
# 0, 1, 2, 3
DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
DIRECTION_TO_NAME = ['North', 'West', 'South', 'East']

def posible_n_turns(maze, x, y, num_turns):
    result = set()

    def dfs(current_x, current_y, depth):
        if depth < num_turns:
            if 0 <= current_y < len(maze) and 0 <= current_x < len(maze[current_y]) and maze[current_y][current_x] != '#':
                result.add((current_x, current_y))
        if depth == 0:
            return
        for (dx, dy) in DIRECTIONS:
            new_x, new_y = current_x + dx, current_y + dy
            dfs(new_x, new_y, depth - 1)

    dfs(x, y, num_turns)
    return result

def posible_2_turns(maze, x, y):
    return posible_n_turns(maze, x, y, 2)

def get_next_direction(maze, x, y):
    result = []
    for (dx, dy) in DIRECTIONS:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[new_y]) and maze[new_y][new_x] != '#':
           result.append((new_x, new_y))
    return result

def print_maze(maze):
    max_len = max(len(str(cell)) for row in maze for cell in row)
    for line in maze:
        print(" ".join(str(cell).rjust(max_len) for cell in line))

def find_char(maze, char):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == char:
                return (x, y)
    return None

def enumerate_line(maze, start):
    x, y = start
    next_dirs = [(x, y)] # -1, -1 is a dummy value to not break the loop
    parent = None
    iteration = 0
    on_path = []
    while len(next_dirs) != 1 or iteration < 2:
        for pos in next_dirs:
            if pos != parent:
                parent = (x, y)
                x, y = pos
                maze[y][x] = iteration
                on_path.append((x, y))
                next_dirs = get_next_direction(maze, x, y)
                iteration += 1
                break
    return on_path

def solver1(puzzle_input_tup):
    puzzle_input, on_path = puzzle_input_tup

    cout_point = 100
    acc = 0
    for track in on_path:
        start_point = puzzle_input[track[1]][track[0]]
        cheats = posible_2_turns(puzzle_input, track[0], track[1])
        for cheat in cheats:
            end_point = puzzle_input[cheat[1]][cheat[0]]
            diff = end_point - start_point - 2
            if diff < cout_point:
                continue
            acc += 1

    return acc

def solver2(puzzle_input_tup):
    puzzle_input, on_path = puzzle_input_tup

    cout_point = 100
    acc = 0
    for track in on_path:
        start_point = puzzle_input[track[1]][track[0]]
        cheats = posible_n_turns(puzzle_input, track[0], track[1], 20)
        for cheat in cheats:
            end_point = puzzle_input[cheat[1]][cheat[0]]
            diff = end_point - start_point - 2
            if diff < cout_point:
                continue
            acc += 1

    return acc

def starter(puzzle_input):
    start = find_char(puzzle_input, 'S')
    on_path = enumerate_line(puzzle_input, start)
    return on_path


FILE = "input.txt"
#FILE = "test.txt"

INPUT = parser(file_reader(FILE))
PUZZLE_INPUT = (INPUT, starter(INPUT))


print("Advent of Code: Day 13")
print("Solution for Part 1:", solver1(PUZZLE_INPUT))
print("Solution for Part 2:", solver2(PUZZLE_INPUT))
