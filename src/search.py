import sys
import uniform_cost_search as ucs
import heuristic_search as hs
import weighted_heuristic_search as whs
import heuristics as hrsts

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

def flat(tuple):
    return "\""+",".join(map(str,tuple))+"\""
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
        print "2 arguments required: search.py [file] [search type] [heuristic type] [weight]"
        exit()

    # Get file name, search type (also heuristic type and weight, if given)
    file_name = sys.argv[1]
    search_type = sys.argv[2]  # u = uniform-cost search, a = A* search, w = weighted A* search
    heuristic_type = -1
    if len(sys.argv) > 3:
        heuristic_type = sys.argv[3]  # 1:linear, 2:manhatan,3:diagonal,4:eucliden,5:sample in instruction
    else:
        heuristic_type = "5"

    weight = 1
    if len(sys.argv) > 4:
        weight = sys.argv[4] # Weight to be used in weighted A* search

    # Read from file
    (start, goal, grid) = read_from_file(file_name)

    # Select heuristic function
    heuristic = None
    if heuristic_type == "1":
        heuristic = hrsts.heu_linear
    elif heuristic_type == "2":
        heuristic = hrsts.heu_manhatan
    elif heuristic_type == "3":
        heuristic = hrsts.heu_diagonal_brkingties
    elif heuristic_type == "4":
        heuristic = hrsts.heu_eucliden_powtwo
    elif heuristic_type == "5":
        heuristic = hrsts.heu_sample
    else:
        raise ValueError('Please pick a valid heuristic from 1 to 5')

    # Use chosen search to find path
    path = None
    num_nodes_expanded = -1

    if search_type == "u":
        uniform_cost_search = ucs.UniformCostSearch(grid)
        path, num_nodes_expanded = uniform_cost_search.search(start, goal)
    elif search_type == "a":
        heuristic_search = hs.HeuristicSearch(grid, heuristic)
        path, num_nodes_expanded = heuristic_search.search(start, goal)
    elif search_type == "w":
        weighted_heuristic_search = whs.WeightedHeuristicSearch(grid, heuristic, weight)
        path, num_nodes_expanded = weighted_heuristic_search.search(start, goal)
    else:
        raise ValueError('Please use a valid search type: u = uniform-cost search, a = A* search, w = weighted A* search')

    # Output result
    if path is None:
        print 'No path found'
    else:
        print 'Path: {}'.format(path)
        print 'Time (# nodes expanded): {}'.format(num_nodes_expanded)
        f = open('path.txt','w')
        f.write("["+','.join(map(flat,path))+"]")
        f.close()