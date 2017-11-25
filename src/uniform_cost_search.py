import math
from priority_queue import PriorityQueue
from cell import Cell

# Constants for terrain type
BLOCKED = 0
UNBLOCKED = 1
ROUGH = 2  # aka hard-to-traverse

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
        s = Cell chosen for exansion
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

    def update_vertex(self, s, neighbor, fringe, goal):
        """
        Update values for a neighbor based on s

        Parameters:
        s = a Cell
        neighbor = a Cell next to s
        fringe = priority queue that stores nodes to be considered for expansion
        goal = coordinates of goal node

        Returns: None
        """
        total_cost = s.g + self.get_cost(s, neighbor)
        if total_cost < neighbor.g:
            neighbor.g = total_cost
            neighbor.parent = s
            if (neighbor.f, neighbor) in fringe:
                fringe.remove_cell(neighbor)

            self.apply_heuristic(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.h  # Update neighbor's f-value
            fringe.add_cell(neighbor, neighbor.f)  # Insert neighbor back into fringe

    def get_hash_key(self, pos):
        """
        Get the hash key for given (x,y) position

        :param pos: 2-tuple (x,y) that represents the position of a cell on the grid
        :return: hash key to use in the closed list dictionary
        """
        hash_code = 91
        return pos[0] * hash_code + pos[1]

    def contained_in_closed(self, pos, closed):
        """
        Check if cell at given position is contained in the cell or not

        :param pos: position of the cell
        :param closed: closed dictionary
        :return: True if position is contained in the dictionary, False otherwise
        """
        key = self.get_hash_key(pos)

        if key in closed:
            if pos in closed[key]:
                return True
        return False

    def search(self, start, goal):
        """
        Do uniform cost search on the grid, find a path from start to goal

        Parameters:
        start = coordinates of the start position
        goal = coordinates of the goal position

        Returns: path, a 1D array of coordinates ((x, y) tuples), None if path does not exist
        """
        # Run search
        start_cell = self.grid[start[0]][start[1]]
        start_cell.g = 0
        self.apply_heuristic(start_cell, goal)
        start_cell.f = start_cell.g + start_cell.h
        start_cell.parent = start

        fringe = PriorityQueue()
        fringe.add_cell(start_cell, start_cell.f)

        closed = {}  # closed := empty dictionary
        num_nodes_expanded = 0

        while len(fringe) != 0:  # Checking that fringe is nonempty
            s = fringe.pop_cell()
            if s.pos == goal:
                path = self.retrieve_path(start, goal)  # Get path from start to goal
                path_length = round(self.grid[goal[0]][goal[1]].g, 2)
                return path, path_length, num_nodes_expanded

            # Store in closed list
            key = self.get_hash_key(s.pos)
            if key in closed: # Uses hash to determine if key is in closed, still O(1)
                closed[key].append(s.pos)
            else:
                closed[key] = [s.pos]
            num_nodes_expanded += 1

            # For each neighbor
            neighbors = self.get_neighbors(s)
            for neighbor in neighbors:
                if not self.contained_in_closed(neighbor.pos, closed):
                    if neighbor not in fringe:
                        neighbor.g = 20000  # 20,000 = infinity
                        neighbor.parent = None
                    self.update_vertex(s, neighbor, fringe, goal)

        return None, -1, -1  # No path found, no nodes expanded
