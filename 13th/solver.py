import os
import numpy as np
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    result = []
    for i in range(0, len(lines), 4):
        current_claw_cachine = lines[i:i+4]
        a = current_claw_cachine[0].replace("Button A: X+", "").replace(" Y+", "").split(",") 
        b = current_claw_cachine[1].replace("Button B: X+", "").replace(" Y+", "").split(",")
        end = current_claw_cachine[2].replace("Prize: X=", "").replace(" Y=", "").split(",")
        result.append({
            "A": (int(a[0]), int(a[1])),
            "B": (int(b[0]), int(b[1])),
            "end": (int(end[0]), int(end[1]))
        })
    return result

def beat_claw_machine(a_x, a_y, b_x, b_y, end_x, end_y):
    A = np.array([
        [a_x, b_x],
        [a_y, b_y]
    ])
    b = np.array([end_x, end_y])
    return np.linalg.solve(A, b)

def solver1(puzzle_input):
    accumulator = 0
    for claw_machine in puzzle_input:
        result = beat_claw_machine(claw_machine["A"][0], claw_machine["A"][1], claw_machine["B"][0], claw_machine["B"][1], claw_machine["end"][0], claw_machine["end"][1])
        if is_vaild_cause_fu_floats(result[0]) and is_vaild_cause_fu_floats(result[1]):
            accumulator += 3*result[0] + 1*result[1]
    return int(accumulator)

def is_vaild_cause_fu_floats(a):
    return 0 <= a <= 100 and round(a, 10) % 1 == 0

def solver2(puzzle_input):
    accumulator = 0
    for claw_machine in puzzle_input:
        result = beat_claw_machine(claw_machine["A"][0], claw_machine["A"][1], claw_machine["B"][0], claw_machine["B"][1], claw_machine["end"][0]+10000000000000, claw_machine["end"][1]+ 10000000000000)
        if is_vaild_cause_fu_floats_2(result[0]) and is_vaild_cause_fu_floats_2(result[1]):
            accumulator += 3*result[0] + 1*result[1]
    return int(accumulator)

def is_vaild_cause_fu_floats_2(a):
    return 0 <= a and round(a, 2) % 1 == 0

FILE = "input.txt"
#FILE = "test.txt"

INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 13")
print("Solution for Part 1:", solver1(INPUT))
print("Solution for Part 2:", solver2(INPUT))
