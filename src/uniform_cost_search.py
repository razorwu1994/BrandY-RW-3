import heapq as hq
import math

# Constants for terrain type
BLOCKED = 0
UNBLOCKED = 1
ROUGH = 2  # aka hard-to-traverse

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
        self.g = 20000  # 20000 represents infinity
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

class UniformCostSearch:
    """
    Class that performs uniform cost search on a 160x120 grid.
    Use search to find a path of coordinates to follow from start to finish.

    Attributes:
    grid = 160x120 grid of cells that represent the map
    """

    def __init__(self, grid):
        self.grid = grid

    def retrieve_path(self, start, goal):
        """
        Find the path leading from start to goal by working backwards from the goal

        Parameters:
        start: (x, y) coordinates of the start position
        goal: (x, y) coordinates of goal position

        Returns:
        1D array of (x, y) coordinates to follow from start to goal
        """
        curr_cell = self.grid[goal[0]][goal[1]]
        path = [curr_cell.pos]  # Start at goal

        while curr_cell.pos != start:
            parent = curr_cell.parent
            path.append(parent.pos)
            curr_cell = parent

        path.reverse()  # Reverse path so it starts at start and ends at goal
        return path

    def get_neighbors(self, cell):
        """
        Find the valid neighbors for the given cell.
        Check 8-neighbors around the cell, ignore blocked cells and cells outside of the boundary.

        Parameters:
        cell = target Cell

        Returns: 1D array of Cells
        """
        # Find 8 neighboring positions
        source_pos = cell.pos
        x = source_pos[0]
        y = source_pos[1]

        top_left_pos = (x - 1, y + 1)
        top_pos = (x, y + 1)
        top_right_pos = (x + 1, y + 1)
        right_pos = (x + 1, y)
        bottom_right_pos = (x + 1, y - 1)
        bottom_pos = (x, y - 1)
        bottom_left_pos = (x - 1, y - 1)
        left_pos = (x - 1, y)

        possible_neighbors = [top_left_pos, top_pos, top_right_pos, right_pos, bottom_right_pos, bottom_pos,
                              bottom_left_pos, left_pos]

        # Filter out invalid neighbors (out of bounds or blocked cell)
        possible_neighbors = [position for position in possible_neighbors if
                              position[0] >= 0 and position[0] < 120 and position[1] >= 0 and position[1] < 160]
        valid_neighbors = []

        for neighbor in possible_neighbors:
            if self.grid[neighbor[0]][neighbor[1]].terrain_type != BLOCKED:
                valid_neighbors.append(neighbor)

        valid_neighbor_cells = [self.grid[position[0]][position[1]] for position in valid_neighbors]

        return valid_neighbor_cells

    def get_cost(self, s, neighbor):
        """
        Calculate cost to move from s to its neighboring cell.
            - Unblocked cells cost 1 to traverse along an edge
            - Hard-to-traverse cells cost 2 to traverse along an edge
            - Moving from highway to highway cuts overall cost by a factor of 4

        Parameters:
        s = Cell for the furthest cell on the optimal path
        neighbor = Cell for a neighbor of s

        Returns: cost to move from s to neighbor
        """
        # Find Euclidean distance
        (x1, y1) = s.pos
        (x2, y2) = neighbor.pos
        distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

        # Factor in terrain types
        temp_cells = [s, neighbor]
        temp_dists = [distance/2, distance/2]

        for i in range(len(temp_cells)):
            if temp_cells[i].terrain_type == ROUGH:
                temp_dists[i] *= 2  # Rough terrain costs 2x to move across

        distance = sum(temp_dists)

        # Check if highway cuts cost further (4x)
        if s.has_highway is True and neighbor.has_highway is True:
            distance /= 4

        return distance

    def apply_heuristic(self, cell, goal):
        """
        Calculate and set the heuristic for a cell

        Parameters:
        cell = target cell
        goal = coordinates of goal cell

        Returns: h value for the cell
        """
        cell.h = 0
        return cell.h  # For UCS use 0, replace with something else for A* and weighted A*

    def update_vertex(self, s, neighbor, fringe):
        """
        Update values for a neighbor based on s

        Parameters:
        s = a Cell
        neighbor = a Cell next to s

        Returns: None
        """
        total_cost = s.g + self.get_cost(s, neighbor)
        if total_cost < neighbor.g:
            neighbor.g = total_cost
            neighbor.parent = s
            if (neighbor.f, neighbor) in fringe:
                fringe.remove((neighbor.f, neighbor))  # Possible optimization opportunity?

            neighbor.f = neighbor.g + neighbor.h  # Update neighbor's f-value
            hq.heappush(fringe, (neighbor.f, neighbor))  # Insert neighbor back into fringe

    def get_hash_key(self, pos):
        """
        Get the hash key for given (x,y) position

        :param pos: 2-tuple (x,y) that represents the position of a cell on the grid
        :return: hash key to use in the closed list dictionary
        """
        hash_code = 23
        return pos[0] * hash_code + pos[1]

    def search(self, start, goal):
        """
        Do uniform cost search on the grid, find a path from start to goal

        Parameters:
        start = coordinates of the start position
        goal = coordinates of the goal position

        Returns: path, a 1D array of coordinates ((x, y) tuples), None if path does not exist
        """

        # Run heuristic on every cell in the grid
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.apply_heuristic(self.grid[i][j], goal)

        # Run search
        start_cell = self.grid[start[0]][start[1]]
        start_cell.g = 0
        start_cell.f = start_cell.g + start_cell.h
        start_cell.parent = start
        fringe = []
        hq.heappush(fringe, (
        start_cell.f, start_cell))  # Insert start to fringe, need to use a 2-tuple so the heapq orders based on f-value
        closed = {}  # closed := empty dictionary
        num_nodes_expanded = 0

        while len(fringe) != 0:  # Checking that fringe is nonempty
            (f, s) = hq.heappop(fringe)
            if s.pos == goal:
                path = self.retrieve_path(start, goal)  # Get path from start to goal
                return path, num_nodes_expanded

            # Store in closed list
            key = self.get_hash_key(s.pos)
            if key in closed:
                closed[key].append(s.pos)
            else:
                closed[key] = [s.pos]
            num_nodes_expanded += 1

            # For each neighbor
            neighbors = self.get_neighbors(s)
            for neighbor in neighbors:
                neighbor_key = self.get_hash_key(neighbor.pos)
                if neighbor_key not in closed or neighbor.pos not in closed[neighbor_key]:
                    self.update_vertex(s, neighbor, fringe)

        return None, -1  # No path found, no nodes expanded