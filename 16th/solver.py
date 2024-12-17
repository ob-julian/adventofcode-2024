import os
import heapq
import numpy as np
#pylint: disable=missing-function-docstring

def file_reader(file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'r') as f:
        return f.read().splitlines()

def parser(lines):
    result = []
    for line in lines:
        result.append(list(line))
    return result

# up left down right
# N, W, S, E
# 0, 1, 2, 3
DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
DIRECTION_TO_NAME = ['North', 'West', 'South', 'East']

class Deer :
    def __init__(self, pos, direction, points, maze, local_maze):
        self.x, self.y = pos
        self.direction = direction
        self.points = points
        self.maze = maze
        # part 2 change: have copy of the maze for local path
        self.local_maze = np.copy(local_maze)
        self.local_maze[self.y][self.x] = 1 # 1 = used

    def move(self):
        new_x = self.x + DIRECTIONS[self.direction][0]
        new_y = self.y + DIRECTIONS[self.direction][1]
        # wall or loop
        if self.maze[new_y][new_x] == '#' or self.local_maze[new_y][new_x] == 1:
            print("Wall or loop")
            return None
        self.local_maze[self.y][self.x] = 1
        self.points += 1
        self.x = new_x
        self.y = new_y
        return self

    def next_moves(self):
        right = (self.direction + 1) % 4
        left = (self.direction - 1) % 4
        left_deer = create_new_deer(self.x, self.y, right, self.points+1000, self.maze, self.local_maze)
        right_deer = create_new_deer(self.x, self.y, left, self.points+1000, self.maze, self.local_maze)
        return [self.move(), left_deer, right_deer]

    def imprint_path(self, local_maze):
        for i, row in enumerate(local_maze):
            for j, _ in enumerate(row):
                if self.local_maze[i][j] == 1:
                    local_maze[i][j] = 1


    #override priority queue
    def __lt__(self, other):
        return self.points < other.points

    def __str__(self):
        return f"Deer at ({self.x}, {self.y}) facing {DIRECTION_TO_NAME[self.direction]} with {self.points} points"


def create_new_deer(x, y, direction, points, maze, local_maze):
    new_x = x + DIRECTIONS[direction][0]
    new_y = y + DIRECTIONS[direction][1]
    if maze[new_y][new_x] == '#' or local_maze[new_y][new_x] == 1:
        return None
    return Deer((new_x, new_y), direction, points + 1, maze, local_maze)

def find_deers(maze, letter):
    # nest time use x and y instead of i and j, maybe you noticed beforehand that you tried to run from the finish to the start...
    # somehow all test cases passed, but the real input failed
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == letter:
                return (x, y)
    return None

def find_winning_deers(maze):
    start = find_deers(maze, 'S')
    end = find_deers(maze, 'E')

    queue = []
    # staritng deer facing east
    heapq.heappush(queue, Deer(start, 3, 0, maze, np.zeros((len(maze), len(maze[0])))))
    winning_deers = []
    while len(queue) > 0:
        local_mazee = np.zeros((len(maze), len(maze[0])), dtype=int)
        for deer in queue:
            deer.imprint_path(local_mazee)
        for deer in queue:
            if local_mazee[deer.y][deer.x] >= 0:
                local_mazee[deer.y][deer.x] = -1
            else:
                local_mazee[deer.y][deer.x] -= 1
        print_maze(local_mazee)
        deer = heapq.heappop(queue)
        print(len(queue) + 1)
        if (deer.x, deer.y) == end:
            print("Found deer with", deer.points, "points")
            if len(winning_deers) > 0:
                if deer.points == winning_deers[0].points:
                    winning_deers.append(deer)
                else:
                    break
            winning_deers.append(deer)
        for next_deer in deer.next_moves():
            if next_deer is not None:
                heapq.heappush(queue, next_deer)
    return winning_deers

def solver1(deers):
    return deers[0].points

def solver2(deers):
    for i in range(1, len(deers)):
        print_maze(deers[i].local_maze)
        print()
        deers[i].imprint_path(deers[0].local_maze)
    return sum(line.count(1) for line in deers[0].local_maze)

def print_maze(maze):
    max_len = max(len(str(cell)) for row in maze for cell in row)
    for line in maze:
        print(" ".join(str(cell).rjust(max_len) for cell in line))

#FILE = "input.txt"
FILE = "test_1.txt"
#FILE = "test_2.txt"

INPUT = parser(file_reader(FILE))

WINNING_DEERS = find_winning_deers(INPUT)

print("Advent of Code: Day 13")
print("Solution for Part 1:", solver1(WINNING_DEERS))
print("Solution for Part 2:", solver2(WINNING_DEERS))
