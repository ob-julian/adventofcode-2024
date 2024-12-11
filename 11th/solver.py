import os
from functools import cache
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    return lines[0].strip().split(" ")

def solver(puzzle_input):
    return sum(blink_recurse(int(n), 75) for n in puzzle_input)

def blink(number):
    if number == 0:
        return [1]
    str_nr = str(number)
    len_nr = len(str_nr)
    if len(str_nr) % 2 == 0:
        return [int(str_nr[:len_nr//2]), int(str_nr[len_nr//2:])]
    return [number * 2024]

@cache # that was rediculously effective
def blink_recurse(number, blinks):
    if blinks == 0:
        return 1
    newNumbers = blink(number)
    return sum(blink_recurse(n, blinks - 1) for n in newNumbers)


FILE = "input.txt"

INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 11")
print("Solution for Part 2:", solver(INPUT))
