
from collections import Counter
from random import randint
from heapq import heappop, heappush
from math import sqrt


def build_maze(m, n, swag):
    """ Build maze, build paths and add swag in maze, call A* algorithm to find shortest path,
        reconstruct path, output data on swag collected, and return maze graphic.
        parameters: m: rows (height) of maze
                    n: columns (width) of maze
                    swag: list of swag item types to be distributed in maze
        returns: grid: maze graphic (with path indicated)
    """
    grid = [['wall' for col in range(n)] for row in range(m)]
    start_i, start_j = randint(0, m - 1), randint(0, n - 1)
    grid[start_i][start_j] = "Start"
    mow(grid, start_i, start_j)
    end_i, end_j = explore_maze(grid, start_i, start_j, swag)
    came_from = a_star(grid, (start_i, start_j), (end_i, end_j))
    reconstruct_path(grid, came_from, (end_i, end_j), swag)
    return grid


def print_maze(grid):
    """ Output maze (including embedded swag and shortest path) to console.
        parameters: grid: maze
        returns: nothing (prints to console)
    """
    for row in grid:
        printable_row = ''
        for cell in row:
            if cell == "wall":
                char = '#'
            elif cell == "empty":
                char = ' '
            else:
                char = cell[0]
            printable_row += char
        print(printable_row)


def mow(grid, i, j):
    """ Clear out paths by removing walls within maze.
        parameters: grid: maze
                    i: grid location index
                    j: grid location index
        returns: nothing
    """
    directions = ["U", "D", "L", "R"]
    while len(directions) > 0:
        directions_index = randint(0, len(directions) - 1)
        direction = directions.pop(directions_index)
        if direction == 'U':
            if i - 2 < 0:
                continue
            elif grid[i - 2][j] == 'wall':
                grid[i - 1][j] = 'empty'
                grid[i - 2][j] = 'empty'
                mow(grid, i - 2, j)
        elif direction == 'D':
            if i + 2 >= len(grid):
                continue
            elif grid[i + 2][j] == 'wall':
                grid[i + 1][j] = 'empty'
                grid[i + 2][j] = 'empty'
                mow(grid, i + 2, j)
        elif direction == 'L':
            if j - 2 < 0:
                continue
            elif grid[i][j - 2] == 'wall':
                grid[i][j - 1] = 'empty'
                grid[i][j - 2] = 'empty'
                mow(grid, i, j - 2)
        else:
            if j + 2 >= len(grid[0]):
                continue
            elif grid[i][j + 2] == 'wall':
                grid[i][j + 1] = 'empty'
                grid[i][j + 2] = 'empty'
                mow(grid, i, j + 2)


def explore_maze(grid, start_i, start_j, swag):
    """ Use breadth-first search to drop swag items in random locations and find and return the location
        indices of the end point.
        parameters: grid: maze
                    start_i: starting cell location index
                    start_j: starting cell location index
                    swag: list of swag items provided by user
        returns: i, j: ending cell location indices
    """
    grid_copy = [row[:] for row in grid]
    bfs_queue = [[start_i, start_j]]
    directions = ['U', 'D', 'L', 'R']
    while bfs_queue:
        i, j = bfs_queue.pop(0)
        if randint(1, 10) == 1 and grid[i][j] != "Start":
            grid[i][j] = swag[randint(0, len(swag) - 1)]
        grid_copy[i][j] = "visited"
        for direction in directions:
            explore_i = i
            explore_j = j
            if direction == 'U':
                explore_i = i - 1
            elif direction == 'D':
                explore_i = i + 1
            elif direction == 'L':
                explore_j = j - 1
            else:
                explore_j = j + 1
            if explore_i < 0 or explore_j < 0 or explore_i >= len(grid) or explore_j >= len(grid[0]):
                continue
            elif grid_copy[explore_i][explore_j] != 'visited' and grid_copy[explore_i][explore_j] != 'wall':
                bfs_queue.append([explore_i, explore_j])
    grid[i][j] = "End"
    return i, j


def maze_dimensions():
    """ Obtain user input for maze dimensions.
        parameters: none
        returns: row, column: integer values for maze row (y) and column (x) dimensions
    """
    while True:
        try:
            row = int(input("Enter maze height (an integer): "))
            break
        except ValueError:
            print("Error: you must enter an integer. Try again.")
    while True:
        try:
            column = int(input("Enter maze width (an integer): "))
            break
        except ValueError:
            print("Error: you must enter an integer. Try again.")
    return row, column


def swag():
    """ Obtain user input for swag items to be randomly distributed in maze.
        parameters: none
        returns: swag_list: list of swag items
    """
    swag_list = ['candy corn', 'werewolf', 'pumpkin']
    answer = None
    while answer not in ("y", "n"):
        answer = input("Use default swag list [candy corn, werewolf, pumpkin], y/n? ")
        if answer == "y":
            break
        elif answer == "n":
            swag_list.clear()
            swag_entry = input("Enter swag items, separated by commas: ")
            swag_list = swag_entry.split(", ")
        else:
            print("Error: Please enter y or n.")
    return swag_list


def heuristic(start, end):
    """ Obtain Euclidean heuristic for A* algorithm.
        parameters: start: start vertex
                    end: end vertex
        returns: Euclidean distance
    """
    x_distance = abs(start[0] - end[0])
    y_distance = abs(start[1] - end[1])
    return sqrt(x_distance ** 2 + y_distance ** 2)


def a_star(grid, start, end):
    """ Perform A* algorithm on grid-shaped maze to find shortest path between starting point and
        end point.
        parameters: grid: maze
                    start: start vertex
                    end: end vertex
        returns: came_from: shortest path from start vertex to end vertex
    """
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, end)}
    oheap = []
    heappush(oheap, (fscore[start], start))
    while oheap:
        current = heappop(oheap)[1]
        if current == end:
            break
        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < len(grid):
                if 0 <= neighbor[1] < len(grid[0]):
                    if grid[neighbor[0]][neighbor[1]] == "wall":
                        continue
                else:
                    continue
            else:
                continue
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heappush(oheap, (fscore[neighbor], neighbor))
    return came_from


def reconstruct_path(grid, came_from, end, swag):
    """ Add path markers to designate shortest path from end point to start point in maze, create and
        display list of swag items collected along path.
        parameters: grid: maze
                    came_from: shortest path
                    end: end vertex
                    swag: list of user-defined swag (for comparison)
        returns: data: path
    """
    current = end
    swag_list = []
    data = []
    while current in came_from:
        i, j = current
        if grid[i][j] != "End":
            if grid[i][j] in swag:
                swag_list.append(grid[i][j])
            grid[i][j] = "."
        data.insert(0, current)
        current = came_from[current]
    print_swag(swag_list)
    return data


def radix_sort(swag_list):
    """ Perform radix sort on list of swag items (strings) collected along shortest path in maze.
        parameters: swag_list: unsorted list of swag items
        returns: swag_list: alphabetically sorted list of swag items
    """
    max_length = -1
    for string in swag_list:  # Find longest string
        string_length = len(string)
        if string_length > max_length:
            max_length = string_length
    oa = ord('a') - 1;  # First character code
    oz = ord('z') - 1;  # Last character code
    n = oz - oa + 2;  # Number of buckets (+empty character)
    buckets = [[] for i in range(0, n)]  # The buckets
    for position in reversed(range(0, max_length)):
        for string in swag_list:
            index = 0  # Assume "empty" character
            if position < len(string):  # Might be within length
                index = ord(string[position]) - oa
            buckets[index].append(string)  # Add to bucket
        del swag_list[:]
        for bucket in buckets:  # Reassemble swag_list in new order
            swag_list.extend(bucket)
            del bucket[:]
    return swag_list


def print_swag(swag_list):
    """ Prints swag collection, calls radix sort and displays sorted collection, shows totals
        listed by swag item.
        parameters: swag_list: list of swag collected
        returns: nothing
    """
    print("\n\nSwag items in the order they were collected in the maze:\n{0}".format(swag_list))
    swag_list2 = [x.replace(' ', '') for x in swag_list]
    radix_sort(swag_list2)          
    swag_list3 = []
    for word2 in swag_list2:
        found = False
        for word in swag:
            if word2 == word.replace(' ', ''):
                found = True
                swag_list3.append(word)
                break
        if not found:
            swag_list3.append(word2)
    print("\nSwag items, sorted:\n{0}".format(swag_list3))
    swag_list4 = Counter(swag_list3)
    print("\nTabulated collection of swag items:")
    for k, v in list(reversed(swag_list4.most_common())):
        print("\t{0}: {1}".format(k, v))
    print("\n")


print("Codecademy Computer Science Basics: Algorithms",
      "Convoluted Kernel Maze Capstone Project",
      "Author: Patrick Wrinn\n", "Please provide maze parameters:\n", sep="\n")
row, col = maze_dimensions()
swag = swag()
print_maze(build_maze(row, col, swag))