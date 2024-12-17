import os
import heapq
import numpy as np
#pylint: disable=missing-function-docstring
#pylint: disable=global-statement

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(puzzle_input):
    global A, B, C
    A = int(puzzle_input[0].replace("Register A: ", ""))
    B = int(puzzle_input[1].replace("Register B: ", ""))
    C = int(puzzle_input[2].replace("Register C: ", ""))
    return [int(x) for x in puzzle_input[4].replace("Program: ", "").split(",")]


PC, A, B, C = 0, 0, 0, 0
OUTPUT = []

def get_literal_value(value):
    return int(value)

def get_combo_value(value):
    value = int(value)
    if 0 <= value <= 3:
        return value
    if value == 4:
        return A
    if value == 5:
        return B
    if value == 6:
        return C
    raise ValueError("Reserve value")
        

# opcode 0
def adv(value):
    global A
    A = int(A / 2 ** get_combo_value(value))

# opcode 1
def bxl(value):
    global B
    B = B ^ get_literal_value(value)

# opcode 2
def bst(value):
    global B
    B = get_combo_value(value) % 8


# opcode 3
def jnz(value):
    global PC
    if A != 0:
        PC = get_literal_value(value) - 2

# opcode 4
def bxc(value):
    global B
    B = B ^ C

# opcode 5
def out(value):
    output_value = get_combo_value(value) % 8
    OUTPUT.append(output_value)

# opcode 6
def bdv(value):
    global B
    B = int(A / 2 ** get_combo_value(value))

# opcode 7
def cdv(value):
    global C
    C = int(A / 2 ** get_combo_value(value))

def opcode_lookup(opcode):
    opcodes = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    return opcodes[opcode]


def execute_instructions(instructions):
    global PC
    while PC < len(instructions):
        opcode = instructions[PC]
        value = instructions[PC + 1]
        opcode_lookup(opcode)(value)
        PC += 2

def solver1(puzzle_input):
    execute_instructions(puzzle_input)
    return ",".join([str(x) for x in OUTPUT])

#FILE = "input.txt"
FILE = "test_2.txt"

INPUT = parser(file_reader(FILE))


print("Advent of Code: Day 13")
print("Solution for Part 2:", solver1(INPUT))
