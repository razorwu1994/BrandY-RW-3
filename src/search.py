import sys
import heapq as hq
import math

# Constants for terrain type
BLOCKED = 0
UNBLOCKED = 1
ROUGH = 2 # aka hard-to-traverse

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
                tempCell = Cell((y, x), int(char), False)
            elif char == 'a':
                tempCell = Cell((y, x), 1, True)
            elif char == 'b':
                tempCell = Cell((y, x), 2, True)

            row.append(tempCell)
        grid.append(row)

    return (start, goal, grid)

class Cell:
    """
    Represents a cell in the 160x120 grid

    Attr:
        pos: coordinates for this cell in the form of 2-tuple: (x, y)
        parent: previously visited Cell before reaching current one, None by default
        terrain_type: 0 for blocked, 1 for unblocked, 2 for hard-to-traverse
        has_highway: 0 if it has no highway, 1 if it does
        f: function value
        g: distance from start
        h: heuristic value

    Only unblocked (1) and hard-to-traverse (2) terrains can have highways.
    """

    def __init__(self, pos, terrain_type, has_highway):
        """
        By default, set f = 0, g = 20000, h = 0
        """
        self.pos = pos
        self.parent = None
        self.terrain_type = terrain_type
        self.has_highway = has_highway
        self.g = 20000 # 20000 represents infinity
        self.h = 0
        self.f = self.g + self.h

    def convert_to_char(self):
        """
        Converts cell to '0', '1', '2', 'a' or 'b' depending on its characteristics
        """
        if self.terrain_type == 1 and self.has_highway == True:
            return 'a'
        elif self.terrain_type == 2 and self.has_highway == True:
            return 'b'
        else:
            return str(self.terrain_type)

    def __eq__(self, other):
        """
        Compare two cells based on their positions
        """
        if not isinstance(other, Cell):
            return False

        if self.pos == other.pos:
            return True
        return False
    
    def __str__(self):
        """
        Prints out the Cell in format ((x, y), f, g, h)
        """
        t_type = self.convert_to_char()
        return "(({0}, {1}), {2}, f={3}, g={4}, h={5})".format(self.pos[0], self.pos[1], t_type, self.f, self.g, self.h)

def retrieve_path(start, goal, grid):
    """
    Find the path leading from start to goal by working backwards from the goal

    Parameters:
    start: (x, y) coordinates of the start position
    goal: (x, y) coordinates of goal position
    grid: 160x120 array of Cells

    Returns:
    1D array of (x, y) coordinates to follow from start to goal
    """
    curr_cell = grid[goal[0]][goal[1]]
    path = [curr_cell.pos] # Start at goal
    
    while curr_cell.pos != start:
        parent = curr_cell.parent
        path.append(parent.pos)
        curr_cell = parent
        
    path.reverse() # Reverse path so it starts at start and ends at goal
    return path

def get_neighbors(cell, grid):
    """
    Find the valid neighbors for the given cell.
    Check 8-neighbors around the cell, ignore blocked cells and cells outside of the boundary.

    Parameters:
    cell = target Cell
    grid = 160x120 grid of Cells

    Returns: 1D array of Cells
    """
    # Find 8 neighboring positions
    pos = cell.pos
    
    top_left_pos = (pos[0] - 1, pos[1] + 1)
    top_pos = (pos[0], pos[1] + 1)
    top_right_pos = (pos[0] + 1, pos[1] + 1)
    right_pos = (pos[0] + 1, pos[1])
    bottom_right_pos = (pos[0] + 1, pos[1] - 1)
    bottom_pos = (pos[0], pos[1] - 1)
    bottom_left_pos = (pos[0] - 1, pos[1] - 1)
    left_pos = (pos[0] - 1, pos[1])
    
    possible_neighbors = [top_left_pos, top_pos, top_right_pos, right_pos, bottom_right_pos, bottom_pos, bottom_left_pos, left_pos]

    # Filter out invalid neighbors (out of bounds or blocked cell)
    possible_neighbors = [pos for pos in possible_neighbors if pos[0] >= 0 and pos[0] < 120 and pos[1] >= 0 and pos[1] < 160]
    
    for neighbor in possible_neighbors:
        if grid[neighbor[0]][neighbor[1]].terrain_type == BLOCKED:
            possible_neighbors.remove(neighbor)

    """ Testing
    print "Neighbors:"
    for neighbor in possible_neighbors:
        print neighbor
    print ""
    """

    valid_neighbors = [grid[pos[0]][pos[1]] for pos in possible_neighbors]
    return valid_neighbors

def get_cost(s, neighbor):
    """
    Calculate cost to move from s to its neighboring cell.
        - Unblocked cells cost 1 to traverse along an edge
        - Hard-to-traverse cells cost 2 to traverse along an edge
        - Moving from highway to highway cuts overall cost by a factor of 4  
    Parameter:
    s = Cell for the furthest cell on the optimal path
    neighbor = Cell for a neighbor of s

    Returns: cost to move from s to neighbor
    """
    # Find Euclidean distance
    (x1, y1) = s.pos
    (x2, y2) = neighbor.pos
    distance = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

    # Factor in terrain types
    temp_cells = [s, neighbor]
    temp_dists = [distance/2, distance/2]

    for i in range(len(temp_cells)):
        if temp_cells[i].terrain_type == ROUGH:
            temp_dists[i] *= 2 # Rough terrain costs 2x to move across

    distance = sum(temp_dists)

    # Check if highway cuts cost further (4x)
    if s.has_highway is True and neighbor.has_highway is True:
        distance /= 4

    return distance

def get_heuristic(cell, grid):
    """
    Calculate the heursitic for a cell

    Parameters:
    cell = target cell
    grid = 160x120 grid

    Returns: h value for the cell
    """
    return 0 # For UCS use 0, replace with something else for A* and weighted A*

def update_vertex(s, neighbor, fringe):
    """
    Update values for a neighbor based on s

    Parameters:
    s = a Cell
    neighbor = a Cell next to s

    Returns: None
    """
    total_cost = s.g + get_cost(s, neighbor)
    if total_cost < neighbor.g:
        neighbor.g = total_cost
        neighbor.parent = s
        if (neighbor.f, neighbor) in fringe:
            fringe.remove((neighbor.f, neighbor)) # Possible optimization opportunity?

        neighbor.f = neighbor.g + neighbor.h # Update neighbor's f-value
        hq.heappush(fringe, (neighbor.f, neighbor)) # Insert neighbor back into fringe

def uniform_cost_search(start, goal, grid):
    """
    Do uniform cost search on the given grid, start and goal

    Parameters:
    start = coordinates of the start position
    goal = coordinates of the goal position
    grid = entire 160x120 grid map

    Returns: path, a 1D array of coordinates ((x, y) tuples), None if path does not exist
    """
    # Run search
    start_cell = grid[start[0]][start[1]]
    start_cell.g = 0
    start_cell.h = get_heuristic(start_cell, grid)
    start_cell.f = start_cell.g + start_cell.h
    start_cell.parent = start
    fringe = [] 
    hq.heappush(fringe, (start_cell.f, start_cell)) # Insert start to fringe, need to use a 2-tuple so the heapq orders based on f-value
    closed = [] # closed := empty set

    while len(fringe) != 0: # Checking that fringe is nonempty
        (f, s) = hq.heappop(fringe)
        if s.pos == goal:
            path = retrieve_path(start, goal, grid) # Get path from start to goal
            return path
        closed.append(s.pos)
        neighbors = get_neighbors(s, grid)
        for neighbor in neighbors:
            if neighbor.pos not in closed: # Possible optimization opportunity
                if (neighbor.f, neighbor) not in fringe:
                    neighbor.g = 20000 # 20,000 = infinity
                    neighbor.parent = None
                update_vertex(s, neighbor, fringe)
    return None # No path found

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


def heu_linear(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = math.sqrt(math.pow(r - xcor, 2) + math.pow(c - ycor, 2))
            col.h = h
            c += 1
        r += 1
    return grid


def heu_manhatan(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = abs(r - xcor) + abs(c - ycor)
            col.h = h
            c += 1
        r += 1
    return grid


def heu_diagonal_brkingties(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = abs(r - xcor) + abs(c - ycor) + (math.sqrt(2) - 2) * min(abs(r - xcor), abs(c - ycor))
            h = h * (1 + 0.01)  # 0.01 is the p to break tie
            col.h = h
            c += 1
        r += 1
    return grid


def heu_eucliden_powtwo(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = math.pow(abs(r - xcor), 2) + math.pow(abs(c - ycor), 2)
            col.h = h
            c += 1
        r += 1
    return grid


def heu_sample(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            manhaX = abs(r - xcor)
            manhaY = abs(c - ycor)
            h = math.sqrt(2) * min(manhaX, manhaY) + max(manhaX, manhaY) - min(manhaX, manhaY)
            col.h = h
            c += 1
        r += 1
    return grid


if __name__ == "__main__":
    """ For testing
    (start, goal, grid) = read_from_file("map1.txt")
    path = uniform_cost_search(start, goal, grid)
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
        testGrid = heu_linear(start, goal, grid)
    if heuristic_type.__eq__("2"):
        testGrid = heu_manhatan(start, goal, grid)
    if heuristic_type.__eq__("3"):
        testGrid = heu_diagonal_brkingties(start, goal, grid)
    if heuristic_type.__eq__("4"):
        testGrid = heu_eucliden_powtwo(start, goal, grid)
    if heuristic_type.__eq__("5"):
        testGrid = heu_sample(start, goal, grid)

    # print testGrid[50][75]

    # In grid, x = y coordinate and y = x coordiante on actual grid
    # print grid[4][0]

    if search_type == "u":
        path = uniform_cost_search(start, goal, grid)
    elif search_type == "a":
        path = heuristic_search(start, goal, grid)
    else:
        path = weighted_heuristic_search(start, goal, grid)

    if path is None:
        print "No path found"
    else:
        print "Path: {}".format(path)
