import sys
import uniform_cost_search as ucs
import heuristics as hrst

def read_from_file(file_name):
    """
    Extract grid data from given file.
    File follows format given in Assignment 3 Instructions.
    """
    # Split by lines
    lines = [line.rstrip('\n') for line in open(file_name)]

    # First line provides coordinates of the starting cell
    start_str = lines[0][3:].split(',')  # Start at index 3 because of weird char in front
    start = tuple([int(c) for c in start_str])

    # Second line provides coordinates of the goal cell
    goal_str = lines[1].split(',')
    goal = tuple([int(c) for c in goal_str])

    # Next eight lines provide the coordinates of the centers of hard to traverse regions
    htt_centers = []
    for i in range(8):
        htt_center_str = lines[2 + i].split(',')
        htt_center = tuple([int(c) for c in htt_center_str])
        htt_centers.append(htt_center)

    """
    Remaining 120 lines represent the map where
        '0' = blocked cell
        '1' = regular unblocked cell
        '2' = hard-to-traverse cell
        'a' = regular unblocked cell with highway
        'b' = hard-to-traverse cell with highway
    """

    grid = [] # For storing data on each cell in the 160x120
    x = -1
    y = -1
    for i in range(10, len(lines)):
        y += 1
        x = -1
        row = []
        line = lines[i]
        for char in line:
            x +=1
            tempCell = None
            if char=='0' or char=='1' or char=='2':
                tempCell = ucs.Cell((y, x), int(char), False)
            elif char == 'a':
                tempCell = ucs.Cell((y, x), 1, True)
            elif char == 'b':
                tempCell = ucs.Cell((y, x), 2, True)

            row.append(tempCell)
        grid.append(row)

    return (start, goal, grid)

def heuristic_search(start, goal, grid):
    # Get data
    # Run search
    # Return the path (1D array)
    print("A* Search")
    return None


def weighted_heuristic_search(start, goal, grid):
    # Get data
    # Run search
    # Return the path (1D array)
    print("Weighted A* Search")
    return None

if __name__ == "__main__":
    """ For testing
    (start, goal, grid) = read_from_file("map1.txt")
    path = ucs.uniform_cost_search(start, goal, grid)
    print path
    """

    # Make sure there are enough argument given
    if (len(sys.argv) < 3):
        print "2 arguments required: search.py [file] [search type]"
        print "search types: u = uniform-cost search, a = A* search, w = weighted A* search"
        exit()

    # Get file name and search type
    file_name = sys.argv[1]
    search_type = sys.argv[2]  # u = uniform-cost search, a = A* search, w = weighted A* search
    if len(sys.argv) > 3:
        heuristic_type = sys.argv[3]  # 1:linear, 2:manhatan,3:diagonal,4:eucliden,5:sample in instruction
    else:
        heuristic_type = "5"
    # Read from file
    (start, goal, grid) = read_from_file(file_name)

    # print heuristic_type
    # heu_linear
    # heu_manhatan
    # heu_diagonal
    # heu_eucliden
    # heu_sample
    # print start, goal

    testGrid = grid
    if heuristic_type.__eq__("1"):
        testGrid = hrst.heu_linear(start, goal, grid)
    if heuristic_type.__eq__("2"):
        testGrid = hrst.heu_manhatan(start, goal, grid)
    if heuristic_type.__eq__("3"):
        testGrid = hrst.heu_diagonal_brkingties(start, goal, grid)
    if heuristic_type.__eq__("4"):
        testGrid = hrst.heu_eucliden_powtwo(start, goal, grid)
    if heuristic_type.__eq__("5"):
        testGrid = hrst.heu_sample(start, goal, grid)

    # print testGrid[50][75]

    # In grid, x = y coordinate and y = x coordiante on actual grid
    # print grid[4][0]

    if search_type == "u":
        path = ucs.uniform_cost_search(start, goal, grid)
    elif search_type == "a":
        path = heuristic_search(start, goal, grid)
    else:
        path = weighted_heuristic_search(start, goal, grid)

    if path is None:
        print "No path found"
    else:
        print "Path: {}".format(path)