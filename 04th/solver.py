import os
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    result = []
    for line in lines:
        result.append(list(line.strip()))
    return result

def solver1(input):
    return search_all(input, "XMAS")

def solver2(input):
    return search_x_mas(input)

def search_wrapper(grid, word, x_start, y_start, x_dir, y_dir, x_step, y_step):
    x = x_start
    y = y_start
    max_y = len(grid)
    max_x = len(grid[0])
    word_pos = 0
    accumulator = 0
    while 0 <= x < max_x and 0 <= y < max_y:
        accumulator += search_single(grid, word, x, y, max_x, max_y, x_dir, y_dir, word_pos)
        x += x_step
        y += y_step
    return accumulator

def search_single(grid, word, x, y, max_x, max_y, x_dir, y_dir, word_pos):
    accumulator = 0
    while 0 <= x < max_x and 0 <= y < max_y:
        if grid[y][x] == word[word_pos]:
            word_pos += 1
            if word_pos == len(word):
                accumulator += 1
                word_pos = 0
        elif grid[y][x] == word[0]:
            word_pos = 1
        else:
            word_pos = 0
        x += x_dir
        y += y_dir
    return accumulator


def search_horizontal(grid, word):
    return search_wrapper(grid, word, 0, 0, 1, 0, 0, 1)

def search_vertical(grid, word):
    return search_wrapper(grid, word, 0, 0, 0, 1, 1, 0)

def search_diagonal(grid, word):
    accumulator = 0
    #print("-diag x-")
    accumulator += search_wrapper(grid, word, 0, 0, 1, 1, 1, 0)
    accumulator += search_wrapper(grid, word, 0, 1, 1, 1, 0, 1)
    #print("-diag y-")
    accumulator += search_wrapper(grid, word, len(grid[0]) - 1, 0, -1, 1, -1, 0)
    accumulator += search_wrapper(grid, word, len(grid[0]) - 1, 1, -1, 1, 0, 1)
    return accumulator


def search_all(grid, word):
    inverted_word = word[::-1]
    accumulator = 0
    accumulator += search_horizontal(grid, word)
    accumulator += search_horizontal(grid, inverted_word)
    accumulator += search_vertical(grid, word)
    accumulator += search_vertical(grid, inverted_word)
    accumulator += search_diagonal(grid, word)
    accumulator += search_diagonal(grid, inverted_word)
    return accumulator


def search_x_mas(grid):
    accumulator = 0
    for x in range(1, len(grid[0])-1):
        for y in range(1, len(grid)-1):
            # first diagonal
            if grid[y][x] == "A" and check_mas(grid, x, y):
                accumulator += 1
    return accumulator


def check_mas_wrapper(grid, x, y, direction_x, direction_y, letter_1, letter_2):
    return grid[y+direction_y][x+direction_x] == letter_1 and grid[y-direction_y][x-direction_x] == letter_2

def check_mas_diag_wrapper(grid, x, y, direction_x, direction_y):
    return check_mas_wrapper(grid, x, y, direction_x, direction_y, "M", "S") or check_mas_wrapper(grid, x, y, direction_x, direction_y, "S", "M")

def check_mas(grid, x, y):
    return check_mas_diag_wrapper(grid, x, y, 1, 1) and check_mas_diag_wrapper(grid, x, y, 1, -1)


FILE = "input.txt"
#FILE = "test.txt"

INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 4")
print("Solution for Part 1:", solver1(INPUT))
print("Solution for Part 2:", solver2(INPUT))
