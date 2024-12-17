import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import count
from numba import njit
import threading
import psutil
#pylint: disable=missing-function-docstring
#pylint: disable=global-statement

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(puzzle_input):
    a = int(puzzle_input[0].replace("Register A: ", ""))
    b = int(puzzle_input[1].replace("Register B: ", ""))
    c = int(puzzle_input[2].replace("Register C: ", ""))
    instructions = [int(x) for x in puzzle_input[4].replace("Program: ", "").split(",")]
    return a, b, c, np.array(instructions, dtype=np.int8)

# computer = [PC, A, B, C]
#PC, A, B, C = 0, 0, 0, 0
#OUTPUT = []

@njit
def get_combo_value(value, computer):
    value = int(value)
    if 0 <= value <= 3:
        return value
    if value == 4:
        return computer[1]
    if value == 5:
        return computer[2]
    if value == 6:
        return computer[3]
    raise ValueError("Reserve value")


# opcode 0
@njit
def adv(computer, value):
    computer[1] = computer[1] / 2 ** get_combo_value(value, computer)

# opcode 1
@njit
def bxl(computer, value):
    computer[2] = computer[2] ^ value

# opcode 2
@njit
def bst(computer, value):
    computer[2] = get_combo_value(value, computer) % 8

# opcode 3
@njit
def jnz(computer, value):
    if computer[1] != 0:
        computer[0] = value

# opcode 4
@njit
def bxc(computer):
    computer[2] = computer[2] ^ computer[3]

# opcode 5
@njit
def out(computer, value, output):
    output_value = get_combo_value(value, computer) % 8
    output[output[0]] = output_value
    output[0] += 1

# opcode 6
@njit
def bdv(computer, value):
    computer[2] = computer[1] / 2 ** get_combo_value(value, computer)

# opcode 7
@njit
def cdv(computer, value):
    computer[3] = computer[1] / 2 ** get_combo_value(value, computer)

@njit
def execute_instruction(computer, instruction, output):
    pc = computer[0]

    if pc >= len(instruction) - 1:
        # end of instructions
        return False
    if output[0] >= len(instruction) + 2:
        # output is full
        return False

    opcode = instruction[pc]
    value = instruction[pc + 1]
    computer[0] += 2
    if opcode == 0:
        adv(computer, value)
    elif opcode == 1:
        bxl(computer, value)
    elif opcode == 2:
        bst(computer, value)
    elif opcode == 3:
        jnz(computer, value)
    elif opcode == 4:
        bxc(computer)
    elif opcode == 5:
        out(computer, value, output)
    elif opcode == 6:
        bdv(computer, value)
    elif opcode == 7:
        cdv(computer, value)
    return True

@njit
def execute_instructions(a, b, c, instructions):
    output = np.zeros(instructions.shape[0] + 2, dtype=np.int8)
    output[0] = 1 # end of output pointer
    computer = np.array([0, a, b, c], dtype=np.int64)
    while execute_instruction(computer, instructions, output):
        pass
    if output[0] != len(instructions)+1 and output[0] != len(instructions):
        return False
    return np.all(np.equal(output[1:-1], instructions))


def solver2_old(puzzle_input):
    counter = 0
    while not execute_instructions(counter, puzzle_input[1], puzzle_input[2], puzzle_input[3]):
        counter += 1
    return counter

def task(counter, puzzle_input):
    return counter if execute_instructions(counter, puzzle_input[1], puzzle_input[2], puzzle_input[3]) else None

stop_event = threading.Event()

def worker(puzzle_input, counter, steps):
    for number in count(start=counter, step=steps):
        if stop_event.is_set():
            return None
        if execute_instructions(number, puzzle_input[1], puzzle_input[2], puzzle_input[3]):
            stop_event.set()
            return number
    return None



def solver2(puzzle_input):
    num_workers = 8
    worker_steps = num_workers
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker, puzzle_input, i, worker_steps) for i in range(num_workers)]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                return result
    return None

if __name__ == "__main__":
    FILE = "input.txt"
    #FILE = "test_2.txt"

    INPUT = parser(file_reader(FILE))

    print("Advent of Code: Day 13")
    print("Solution for Part 2:", solver2(INPUT))
