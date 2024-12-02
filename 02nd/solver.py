import os
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    result = []
    for line in lines:
        result.append([int(x) for x in line.strip().split()])
    return result

def solver1(input):
    counter = 0
    for report in input:
        if check_report(report):
            counter += 1
    return counter

def solver2(input):
    counter = 0
    for report in input:
        if check_report(report):
            counter += 1
        else:
            for i in range(len(report)):
                if check_report(report[:i] + report[i+1:]):
                    counter += 1
                    break

                
    return counter


def check_report(report):
    if len(report) < 2:
        return False
    if report[0] > report[1]:
        return check_report_desc(report)
    if report[0] < report[1]:
        return check_report_asc(report)

    return False

def check_report_desc(report):
    return check_report_wrapper(report, report[0]+1, lambda x, y: x < y)

def check_report_asc(report):
    return check_report_wrapper(report, report[0]-1, lambda x, y: x > y)

def check_report_wrapper(report, start, check):
    i = start
    for level in report:
        if not check(level, i):
            return False
        if abs(level - i) > 3:
            return False
        i = level
    return True
FILE = "input.txt"
#FILE = "test.txt"

INPUT = parser(file_reader(FILE))
print("Advent of Code: Day 2")
print("Solution for Part 1:", solver1(INPUT))
print("Solution for Part 2:", solver2(INPUT))
