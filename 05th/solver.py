import os
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    not_after_rules = {}
    prints = []
    part = 1
    for line in lines:
        if line == "":
            part = 2
            continue
        if part == 1:
            split_line = [int(x) for x in line.split("|")]

            if split_line[1] not in not_after_rules:
                not_after_rules[split_line[1]] = set()
            not_after_rules[split_line[1]].add(split_line[0])
        if part == 2:
            prints.append([int(x) for x in line.split(",")])
    return not_after_rules, prints

def solver1(puzzle_input):
    not_after_rules, prints = puzzle_input
    accumulator = 0
    for printable in prints:
        if check_rules(not_after_rules, printable) is True:
            # no rule was broken
            accumulator += printable[int(len(printable)/2)]

    return accumulator


def check_rules(rules, printable):
    for i, page in enumerate(printable):
        if page not in rules:
            # page has no rules
            continue
        applicable_rules = rules[page]

        # intersection must be empty, if no rules are broken
        if set(printable[i+1:]) & applicable_rules:
            return i
    return True

def solver2(puzzle_input):
    not_after_rules, prints = puzzle_input
    accumulator = 0
    for printable in prints:
        checked_rule = check_rules(not_after_rules, printable)
        if checked_rule is True:
            # no rule was broken -> nothing to fix
            continue
        push_factor = 1
        last_index= -1
        while checked_rule is not True:
            if checked_rule == last_index:
                # no progress was made
                push_factor += 1
            else:
                last_index = checked_rule
                push_factor = 1
                # index out of range test
            if checked_rule + push_factor >= len(printable):
                print("Rule", printable, "can not be fixed, with the current algorithm")
                break
            printable[checked_rule], printable[checked_rule+push_factor] = printable[checked_rule+push_factor], printable[checked_rule]
            checked_rule = check_rules(not_after_rules, printable)
        accumulator += printable[int(len(printable)/2)]
    return accumulator


FILE = "input.txt"
#FILE = "test.txt"

PUZZLE_INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 5")
print("Solution for Part 1:", solver1(PUZZLE_INPUT))
print("Solution for Part 2:", solver2(PUZZLE_INPUT))
