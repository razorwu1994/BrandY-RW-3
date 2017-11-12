import heapq

class Cell:
    """
    Represents a cell in the 160x120 grid

    Attr:
        terrain_type: 0 for blocked, 1 for unblocked, 2 for hard-to-traverse
        has_highway: 0 if it has no highway, 1 if it does
        f: function value
        g: distance from start
        h: heuristic value

    Only unblocked (1) and hard-to-traverse (2) terrains can have highways.
    """

    def __init__(self, terrain_type, has_highway):
        """
        By default, set f = 0, g = 0, h = 0
        """
        self.terrain_type = terrain_type
        self.has_highway = has_highway
        f = 0
        g = 0
        h = 0    
    
    def __str__(self):
        """
        Prints out the card with the format: <value> of <suit>
        Jokers are just printed out as 'joker'
        """
        t_type = str(self.terrain_type)

        if self.terrain_type == 1 && self.has_highway == True:
            t_type = 'a'
        elif self.terrain_type == 2 && self.has_highway == True:
            t_type = 'b'
            
        return "({0}, {2}, {3}, {4))".format(t_type, self.f, self.g, self.h)

def read_from_file(file_name):
    """
    Extract grid data from given file.
    File follows format given in Assignment 3 Instructions.
    """
    # Split by lines
    lines = [line.rstrip('\n') for line in open(filename)]

    # Test, for printing out lines
    for line in range(len(lines)):
        print "{}\n".format(line)
        
    # First line provides coordinates of the starting cell
    start = lines[0].split(',')

    # Second line provides coordinates of the goal cell
    goal = lines[1].split(',')
    
    # Next eight lines provide the coordinates of the centers of hard to traverse regions
    htt_centers = []
    for i in range(8):
        htt_centers.append(lines[2 + i].split(','))
        
    """
    Remaining 120 lines represent the map where
        '0' = blocked cell
        '1' = regular unblocked cell
        '2' = hard-to-traverse cell
        'a' = regular unblocked cell with highway
        'b' = hard-to-traverse cell with highway
    """

    grid = [] # For storing data on each cell in the 160x120 grid

    for i in range(10, len(lines)):
        row = []
        for [c in c in lines[i + 10]]:
            tempCell = None
            if c=='0' || c=='1' || c=='2':
                tempCell = Cell(int(c), False)
            elif c == 'a':
                tempCell = Cell(1, True)
            elif c == 'b':
                tempCell = Cell(2, True)

            row.append(tempCell)
        grid.append(row)

    return (start, goal, grid)

def uniform_cost_search(start, goal, grid):
    """
    Do uniform cost search on the given grid, start and goal

    Parameters:
    start = coordinates of the start position
    goal = coordinates of the goal position
    grid = entire 160x120 grid map
    """

    
    # Run search
    # Return the path (1D array)
}

def heuristic_search(){
    # Get data
    # Run search
    # Return the path (1D array)
}

def weighted_heuristic_search(){
    # Get data
    # Run search
    # Return the path (1D array)
}

if __name__ == "__main__":
    # Make sure there are enough argument given
    if(len(sys.argv) < 3):
        print "2 arguments required: search.py [file] [search type]"
        print "search types: u = uniform-cost search, a = A* search, w = weighted A* search"
        exit()

    # Get file name and search type
    file_name = sys.argv[1]
    search_type = sys.argv[2] # u = uniform-cost search, a = A* search, w = weighted A* search

    # Read from file
    [start, goal, grid] = read_from_file(file_name)

    if search_type == "u":
        [path, grid] = uniform_cost_search(start, goal, grid)
    elif search_type == "a":
        [path, grid] = heuristic_search(start, goal, grid)
    else:
        [path, grid] = weighted_heuristic_search(start, goal, grid)
