import os
import numpy as np
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    result = []
    for line in lines:
        result.append(np.array([int(x) for x in line.replace("p=", "").replace(" v=", ",").split(",")]))
    return result

def move_robot(position, velocity, steps):
    return position + velocity * steps

def teleport_robot(position, room_width, room_height):
    return [position[0] % room_width, position[1] % room_height]

def get_quadrant(position, room_width, room_height):
    if position[0] < room_width//2:
        if position[1] < room_height//2:
            return 0
        if position[1] > room_height//2:
            return 1
    if position[0] > room_width//2:
        if position[1] < room_height//2:
            return 2
        if position[1] > room_height//2:
            return 3
    return -1

def move_robots(robots, steps):
    width = 101
    height = 103
    for robot in robots:
        postion = np.array(robot[0:2])
        velocity = np.array(robot[2:4])
        new_position = teleport_robot(move_robot(postion, velocity, steps), width, height)
        robot[0] = new_position[0]
        robot[1] = new_position[1]


def solver1(puzzle_input):
    quadrants = [0,0,0,0]
    move_robots(puzzle_input, 100)
    for robot in puzzle_input:
        quadrant = get_quadrant(robot[:2], 101, 103)
        if quadrant != -1:
            quadrants[quadrant] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def find_all_neighbours(room, position):
    neighbours = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            #if position[0] + x < 0 or position[0] + x >= 101 or position[1] + y < 0 or position[1] + y >= 103:
            if not (0 <= position[0] + x < room.shape[1] and 0 <= position[1] + y < room.shape[0]):
                continue
            if room[position[1] + y, position[0] + x] > 0:
                # found neighbour
                neighbours.append([position[0] + x, position[1] + y])
                # remove neighbour from room
                room[position[1] + y, position[0] + x] = -1
    return neighbours

def count_neighbour_lines(room, position):
    queue = [position]
    count = 0
    while len(queue) > 0:
        count += 1
        current = queue.pop(0)
        neighbours = find_all_neighbours(room, current)
        for neighbour in neighbours:
            queue.append(neighbour)
    return count

def solver2(puzzle_input):
    i = 0
    while i < 10000:
        #print(i)
        move_robots(puzzle_input, 1)
        room = np.zeros((103, 101), dtype=int)
        for robot in puzzle_input:
            room[robot[1], robot[0]] += 1
        max_neighbours_count = 0
        for robot in puzzle_input:
            position = robot[:2]
            local_neighbours = count_neighbour_lines(room, position)
            max_neighbours_count = max(max_neighbours_count, local_neighbours)
        if max_neighbours_count / len(puzzle_input) > 0.2:
            print("Found Christmas Tree wich" , max_neighbours_count / len(robot) * 100, "% of the robots are neighbours")
            for row in room:
                print("".join(["#" if x > 0 else "." for x in row]))
            return i
        i += 1

FILE = "input.txt"
#FILE = "test.txt"

testgrid = np.zeros((11, 7), dtype=int)
for i in range(len(testgrid[0])):
    testgrid[0, i] = 1
    testgrid[len(testgrid)-1, i] = 1

print(testgrid)

print(count_neighbour_lines(testgrid, [0, 0]))

print(testgrid)

INPUT = parser(file_reader(FILE))

print("Advent of Code: Day 13")
print("Solution for Part 1:", solver1(INPUT[:]))
print("Solution for Part 2:", solver2(INPUT))
