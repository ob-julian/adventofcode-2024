import os
import numpy as np

# pylint: disable=missing-function-docstring

def read_file(file):
    file_path = os.path.join(os.path.dirname(__file__), file)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def parse_data(data):
    result = []
    tmp = []
    for line in data:
        if line == "":
            result.append(np.array(tmp, dtype=bool))
            tmp = []
        else:
            tmp.append([x == "#" for x in line])
    result.append(np.array(tmp))
    return result

def convert_to_pin_layout(schema):
    #width = len(schema[0])
    #height = len(schema)
    width, height = 5, 7 # should be fix
    w, h = schema.shape
    pin_layout = np.zeros(width, dtype=int)
    for i, line in enumerate(schema):
        pin_layout[i] = sum(line) - 1
    return pin_layout
        

def solve1(puzzle_input):
    keys = []
    locks = []
    for schema in puzzle_input:
        if schema[0][0] == 0:
            # is key, top row can only have 0
            append_to = locks
        else:
            schema = np.flipud(schema) # unified schema
            append_to = keys
        schema = np.rot90(schema, 3) # first column is now the first row
        pin_layout = convert_to_pin_layout(schema)
        append_to.append(pin_layout)

    # for now we bruteforce and decide later if we need to optimize
    # nop run time for actual input is 0.3s
    counter = 0
    for key in keys:
        for lock in locks:
            if not any(key + lock > 5):
                counter += 1
    return counter

def solve2(puzzle_input):
    return

DATA = parse_data(read_file("input.txt"))
#DATA = parse_data(read_file("test.txt"))

print("Advent of Code: 19th")
print("Part 1:", solve1(DATA))
print("Part 2:", solve2(DATA))
