import sys
import heapq
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
    start_str = lines[0][3:].split(',') # Start at index 3 because of weird char in front
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
        prev: coordinate for the previously visited cell to reach the current one, None by default
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
        self.prev = None
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

    def __cmp__(self, other):
        """
        Compare two cells based on their f (priority) values
        """
        return cmp(self.f, other.f)
    
    def __str__(self):
        """
        Prints out the card with the format: <value> of <suit>
        Jokers are just printed out as 'joker'
        """
        t_type = self.convert_to_char()
        return "({}, f={}, g={}, h={})".format(t_type, self.f, self.g, self.h)

def retrieve_path(start, goal, grid):
    """
    Find the path leading from start to goal by working backwards from the goal

    Parameters:
    start: (x, y) coordinates of the start position
    goal: (x, y) coordaintes of goal position
    grid: 160x120 array of Cells
    """
    curr_cell = grid[goal[0], goal[1]]
    path = [curr_cell.pos] # Start at goal
    
    while curr_cell.coord != start:
        prev = curr_cell.prev
        path.insert(0, prev.pos) # Insert at front
        curr_cell = prev

    path.insert(0, curr_cell.pos) # End at start (at front of list)
    return path

def get_neighbors(cell, grid):
    """
    Find the valid neighbors for the given cell.
    Check 8-neighbors around the cell, ignore blocked cells and cells outside of the boundary

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
    possible_neighbors = [pos for pos in possible_neighbors if pos[0] >= 0 and pos[0] <= 160 and pos[1] >= 0 and pos[1] <= 120]
    
    for neighbor in possible_neighbors:
        if grid[neighbor[0]][neighbor[1]].terrain_type == BLOCKED:
            possible_neighbors.remove(neighbor)

    print "Neighbors:"
    for neighbor in possible_neighbors:
        print neighbor

    print "" 

    valid_neighbors = [grid[pos[0]][pos[1]] for pos in possible_neighbors]
    return valid_neighbors

def get_distance(s, neighbor):
    """
    Calculate the distance from s to its neighboring cell.
        - Unblocked cells cost 1 to traverse along an edge
        - Hard-to-traverse cells cost 2 to traverse along an edge
        - Moving from highway to highway cuts overall cost by a factor of 4  
    Parameter:
    s = Cell for the furthest cell on the optimal path
    neighbor = Cell for a neighbor of s

    Returns: distance to move from s to neighbor
    """
    # Find Euclidean distance
    (x1, y1) = s.coord
    (x2, y2) = neighbor.coord
    euclid_distance = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))

    # Factor in terrain types
    temp_dict = {s:euclid_distance/2, neigbor:euclid_distance/2}

    for cell in temp_dict.keys:
        if cell.terrain_type == ROUGH:
            temp_dict[cell] *= 2 # Rough terrain costs 2x to move across

    distance = sum(temp_dict.values())

    # Check if highway cuts cost further (4x)
    if s.hasHighway is True and neighbor.hasHighway is True:
        distance /= 4

    return distance

def update_vertex(s, neighbor):
    return None

def uniform_cost_search(start, goal, grid):
    """
    Do uniform cost search on the given grid, start and goal

    Parameters:
    start = coordinates of the start position
    goal = coordinates of the goal position
    grid = entire 160x120 grid map

    Returns: path, a 1D array of coordinates ((x, y) tuples)
    """
    print("UCS")
            
    # Run search
    start_cell = grid[start[0]][start[1]] # -------------------May have swapped x and y coord
    start_cell.g = 0
    start_cell.prev = start
    fringe = [] 
    heappush(fringe, start_cell) # Insert to fringe
    closed = [] # closed := empty set

    while len(fringe) != 0: # Checking that fringe is nonempty
        s = heappop(fringe)
        if s.coord == goal:
            # Retrieve path
            path = retrieve_path(start, goal, grid)
            return path
        closed.append(s)
        neighbors = get_neighbors(s)
        for neighbor in neighbors:
            if neighbor not in closed:
                if neighbor not in fringe:
                    neighbor.g = 20000
                    neighbor.parent = None
                update_vertex(s, neighbor)
    return None # No path found

    # Done with search, retrieve path or no path found

    # Return the path (1D array)
    return (None, None)

def heuristic_search():
    # Get data
    # Run search
    # Return the path (1D array)
    print("A* Search")
    return (None, None)

def weighted_heuristic_search():
    # Get data
    # Run search
    # Return the path (1D array)
    print("Weighted A* Search")
    return (None, None)

if __name__ == "__main__":
    (start, goal, grid) = read_from_file("map1.txt")
    """ Testing
    # Make sure there are enough argument given
    if(len(sys.argv) < 3):
        print "2 arguments required: search.py [file] [search type]"
        print "search types: u = uniform-cost search, a = A* search, w = weighted A* search"
        exit()

    # Get file name and search type
    file_name = sys.argv[1]
    search_type = sys.argv[2] # u = uniform-cost search, a = A* search, w = weighted A* search

    # Read from file
    (start, goal, grid) = read_from_file(file_name)

    # In grid, x = y coordinate and y = x coordiante on actual grid
    print grid[4][0]

    if search_type == "u":
        path = uniform_cost_search(start, goal, grid)
    elif search_type == "a":
        path = heuristic_search(start, goal, grid)
    else:
        path = weighted_heuristic_search(start, goal, grid)
    """
