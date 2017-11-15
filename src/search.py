import sys
import heapq
import math
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
        self.f = 0
        self.g = 0
        self.h = 0

    def convert_to_char(self):
        if self.terrain_type == 1 and self.has_highway == True:
            return 'a'
        elif self.terrain_type == 2 and self.has_highway == True:
            return 'b'
        else:
            return str(self.terrain_type)
    
    def __str__(self):
        """
        Prints out the card with the format: <value> of <suit>
        Jokers are just printed out as 'joker'
        """
        t_type = self.convert_to_char()
        return "({0}, {1}, {2}, {3})".format(t_type, self.f, self.g, self.h)

    def set_h(self,h):
        self.h = h

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
    print htt_centers
        
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
        line = lines[i]
        for char in line:
            tempCell = None
            if char=='0' or char=='1' or char=='2':
                tempCell = Cell(int(char), False)
            elif char == 'a':
                tempCell = Cell(1, True)
            elif char == 'b':
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
    print("UCS")
    # Run search
    # Return the path (1D array)
    return (None, None)

def heuristic_search(start, goal, grid):
    # Get data
    # Run search
    # Return the path (1D array)
    print("Hello")
    return (None, None)

def weighted_heuristic_search(start, goal, grid):
    # Get data
    # Run search
    # Return the path (1D array)
    print("Hello")
    return (None, None)


def heu_linear(start, goal, grid):
    xcor =goal[0]
    ycor =goal[1]
    r=0
    c=0
    for row in grid:
        for col in row:
            h = math.sqrt(math.pow(r-xcor,2)+math.pow(c-ycor,2))
            col.set_h(h)
            c+=1
        r+=1
    return grid
def heu_manhatan(start, goal, grid):
    xcor =goal[0]
    ycor =goal[1]
    r=0
    c=0
    for row in grid:
        for col in row:
            h = abs(r-xcor)+abs(c-ycor)
            col.set_h(h)
            c+=1
        r+=1
    return grid
def heu_diagonal(start, goal, grid):
    xcor =goal[0]
    ycor =goal[1]
    r=0
    c=0
    for row in grid:
        for col in row:
            h = abs(r-xcor)+abs(c-ycor)+(math.sqrt(2)-2)*min(abs(r-xcor),abs(c-ycor))
            col.set_h(h)
            c+=1
        r+=1
    return grid
def heu_eucliden(start, goal, grid):
    xcor =goal[0]
    ycor =goal[1]
    r=0
    c=0
    for row in grid:
        for col in row:
            h = math.sqrt(math.pow(abs(r-xcor),2)+math.pow(abs(c-ycor),2))
            col.set_h(h)
            c+=1
        r+=1
    return grid
def heu_sample(start, goal, grid):
    xcor =goal[0]
    ycor =goal[1]
    r=0
    c=0
    for row in grid:
        for col in row:
            manhaX=abs(r-xcor)
            manhaY=abs(c-ycor)
            h = math.sqrt(2)*min(manhaX,manhaY)+max(manhaX,manhaY)-min(manhaX,manhaY)
            col.set_h(h)
            c+=1
        r+=1
    return grid


if __name__ == "__main__":
    # Make sure there are enough argument given
    if(len(sys.argv) < 3):
        print "2 arguments required: search.py [file] [search type]"
        print "search types: u = uniform-cost search, a = A* search, w = weighted A* search"
        exit()

    # Get file name and search type
    file_name = sys.argv[1]
    search_type = sys.argv[2] # u = uniform-cost search, a = A* search, w = weighted A* search
    if len(sys.argv) >3:
        heuristic_type = sys.argv[3] # 1:linear, 2:manhatan,3:diagonal,4:eucliden,5:sample in instruction
    else:
        heuristic_type=5
    # Read from file
    [start, goal, grid] = read_from_file(file_name)

    print heuristic_type
    # heu_linear
    # heu_manhatan
    # heu_diagonal
    # heu_eucliden
    # heu_sample
    print start, goal

    testGrid = grid
    if heuristic_type.__eq__("1"):
        testGrid = heu_linear(start, goal, grid)
    if heuristic_type.__eq__("2"):
        testGrid = heu_manhatan(start, goal, grid)
    if heuristic_type.__eq__("3"):
        testGrid = heu_diagonal(start, goal, grid)
    if heuristic_type.__eq__("4"):
        testGrid = heu_eucliden(start, goal, grid)
    if heuristic_type.__eq__("5"):
        testGrid = heu_sample(start, goal, grid)

    print testGrid[50][75]

    # In grid, x = y coordinate and y = x coordiante on actual grid
    # print grid[4][0]

    if search_type == "u":
        [path, grid] = uniform_cost_search(start, goal, grid)
    elif search_type == "a":
        [path, grid] = heuristic_search(start, goal, grid)
    else:
        [path, grid] = weighted_heuristic_search(start, goal, grid)
