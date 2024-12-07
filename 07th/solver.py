import os
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    result = []
    for line in lines:
        tmp = line.split(": ")
        result.append({
            "result": int(tmp[0]),
            "elements": [int(x) for x in tmp[1].split(" ")]
        })
    return result

def solver1(puzzle_input):
    operators = [
        lambda x, y: x + y,
        lambda x, y: x * y
    ]
    return count_correct_equations(puzzle_input, operators)

def solver2(puzzle_input):
    operators = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        lambda x, y: x * (10 ** len(str(y))) + y
    ]
    return count_correct_equations(puzzle_input, operators)

def count_correct_equations(puzzle_input, operators):
    accumulator = 0
    for tmp in puzzle_input:
        elements = tmp["elements"]
        result = tmp["result"]
        if check_equation(elements, operators, result):
            accumulator += result
    return accumulator

def check_equation(elements, operators, result):
    return check_equation_iter(elements, operators, result, 1, elements[0])


def check_equation_iter(elements, operators, result, i, carry):
    if i == len(elements):
        return carry == result
    for op in operators:
        if check_equation_iter(elements, operators, result, i+1, op(carry, elements[i])):
            return True
    return False


FILE = "input.txt"
#FILE = "test.txt"

INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 7")
print("Solution for Part 1:", solver1(INPUT))
print("Solution for Part 2:", solver2(INPUT))
