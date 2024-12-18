import os
import heapq
#pylint: disable=missing-function-docstring

# felt like js today but no priority queue in js, so we use heapq and Python AGAIN

TESTING = False

if TESTING:
    INPUT_FILE = "test.txt"
    WIDTH = 7
    HEIGHT = 7
    STEPS = 12
else:
    INPUT_FILE = "input.txt"
    WIDTH = 71
    HEIGHT = 71
    STEPS = 1024

def read_file(file):
    with open(os.path.join(os.path.dirname(__file__), file), 'r') as f:
        return f.read().splitlines()

def parse_input(input_lines):
    corrupted = []
    for line in input_lines:
        corrupted.append(tuple(int(x) for x in line.split(",")))
    return corrupted

def get_corrupted_grid(corruption_list, start, steps):
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    update_corrupted_grid(corruption_list, start, steps, grid)
    return grid

def update_corrupted_grid(corruption_list, start, steps, grid):
    for i in range(start, start + steps):
        try:
            x = int(corruption_list[i][0])
            y = int(corruption_list[i][1])
            grid[y][x] = 1
        except IndexError as e:
            print("end of corruption list")
            print(e)
        except ValueError as e:
            print(f"Error parsing corruption list: {e}")
    return grid

def dijkstra(grid, start, end):
    # we dont care for the integrity of the grid, so we (miss)use is as our visited array
    # grid: 0 = empty, 1 = wall/corrupted, 2 = visited
    queue = [(0, start)]

    while queue:
        cost, current = heapq.heappop(queue)
        if current == end:
            return cost
        cx, cy = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and grid[ny][nx] == 0:
                heapq.heappush(queue, (cost + 1, (nx, ny)))
                grid[ny][nx] = 2
    return -1

def dijkstra_with_set_and_path(grid, start, end):
    # using det here because we want to reuse the grid for the next iteration
    # grid: 0 = empty, 1 = wall/corrupted
    path = set()
    path.add(start)
    queue = [(0, start, path)]
    visited = set()

    while queue:
        cost, current, path = heapq.heappop(queue)
        if current == end:
            return cost, path
        cx, cy = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in visited and 0 <= nx < WIDTH and 0 <= ny < HEIGHT and grid[ny][nx] == 0:
                cpath = path.copy()
                cpath.add((nx, ny))
                heapq.heappush(queue, (cost + 1, (nx, ny), cpath))
                visited.add((nx, ny))
    return -1, set()

def visualize(grid):
    for row in grid:
        print("".join(str(cell) for cell in row).replace("0", ".").replace("1", "#").replace("2", "O"))

def solve1(corruption_list):
    grid = get_corrupted_grid(corruption_list, 0, STEPS)
    start = (0, 0)
    end = (WIDTH - 1, HEIGHT - 1)
    shortest_path = dijkstra(grid, start, end)
    return shortest_path

def solve2(corruption_list):
    # we can bootstrap the grid as we know 1024 must work
    grid = get_corrupted_grid(corruption_list, 0, STEPS)
    i = STEPS
    start = (0, 0)
    end = (WIDTH - 1, HEIGHT - 1)
    shortest_path, path, reevaluate = -1, set(), True
    while True:
        if reevaluate:
            shortest_path, path = dijkstra_with_set_and_path(grid, start, end)
            reevaluate = False
        if shortest_path == -1:
            break
        i += 1
        update_corrupted_grid(corruption_list, i, 1, grid)
        new_corupted_bit = corruption_list[i]
        if new_corupted_bit in path:
            # a corrupted bit is blocking the known path, we need to reevaluate
            reevaluate = True

    return ",".join(str(x) for x in new_corupted_bit)

def solver2_binary(corruption_list):
    # we can bootstrap the grid as we know 1024 must work
    min_b = STEPS
    max_b = len(corruption_list)
    def get_mid():
        return (min_b + max_b) // 2
    mid = get_mid()
    grid = get_corrupted_grid(corruption_list, 0, get_mid())
    start = (0, 0)
    end = (WIDTH - 1, HEIGHT - 1)
    has_found = False
    while not has_found:
        shortest_path = dijkstra(grid, start, end)
        if shortest_path == -1:
            max_b = mid
        else:
            min_b = mid
        mid = get_mid()
        if max_b - min_b == 1:
            break
        grid = get_corrupted_grid(corruption_list, 0, mid)
    return ",".join(str(x) for x in corruption_list[mid])

if __name__ == "__main__":
    INPUT = parse_input(read_file(INPUT_FILE))
    print("Advent of Code 2024 - Day 18")
    print(f"Part 1: {solve1(INPUT)}")
    print(f"Part 2: {solver2_binary(INPUT)}")
    # initial runtime: 6.3 seconds for part 2
    # with saving the path and only reevaluating when necessary: 1.4 seconds
    # binary search for the last corrupted bit: 0.35 seconds
