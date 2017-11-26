import math
from priority_queue import PriorityQueue
import heuristics as hrsts
from cell2 import Cell2
import copy

# Constants for terrain type
BLOCKED = 0
UNBLOCKED = 1
ROUGH = 2  # aka hard-to-traverse

class SequentialHeuristicSearch:
    """
    Class that performs sequential heuristic search on a 160x120 grid.
    Use search to find a path of coordinates to follow from start to finish.
    OPEN_i = fringe for heuristic i
    CLOSED_i = closed list/dictionary for heuristic i

    Attributes:
    grid = 160x120 grid of cells that represent the map
    w1 = weight used to inflate heuristic values like in weighted A*
    w2 = weight used to prioritize inadmissible search processes over the admissible one (the anchor)
    heuristics = list of heuristic functions
    num_heuristics = number of heuristics in h
    fringes = list of fringes (OPEN lists) where fringe i is for heuristic i
    closed = list of closed lists (dictionaries) where closed list i is for heuristic i
    visited = list of dictionaries (like the closed lists) that keeps tracks of nodes that were visited
    """

    def __init__(self, grid, w1, w2):
        self.grid = grid
        self.w1 = w1
        self.w2 = w2

        h0 = hrsts.heu_diagonal # Use diagonal heuristic as anchor
        h1 = hrsts.heu_euclidean
        h2 = hrsts.heu_manhattan
        h3 = hrsts.heu_euclidean_squared
        h4 = hrsts.heu_sample

        self.heuristics = [h0, h1, h2, h3, h4] # list of heuristics
        self.num_heuristics = 5

        self.fringes = []
        self.closed = []
        self.visited = []

        temp_dict = {}
        for i in range(self.num_heuristics):
            self.fringes.append(PriorityQueue())
            self.closed.append(copy.deepcopy(temp_dict))
            self.visited.append(copy.deepcopy(temp_dict))

    # Methods from UCS -------------------------------------------------------------------------------------------------
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
        temp_dists = [distance / 2, distance / 2]

        for i in range(len(temp_cells)):
            if temp_cells[i].terrain_type == ROUGH:
                temp_dists[i] *= 2  # Rough terrain costs 2x to move across

        distance = sum(temp_dists)

        # Check if highway cuts cost further (4x)
        if s.has_highway is True and neighbor.has_highway is True:
            distance /= 4

        return distance

    def get_hash_key(self, pos):
        """
        Get the hash key for given (x,y) position

        :param pos: 2-tuple (x,y) that represents the position of a cell on the grid
        :return: hash key to use in the closed list dictionary
        """
        hash_code = 91
        return pos[0] * hash_code + pos[1]

    def contained_in_dict(self, pos, closed):
        """
        Check if cell at given position is contained in the given dictionary or not

        :param pos: position of the cell
        :param closed: closed dictionary
        :return: True if position is contained in the dictionary, False otherwise
        """
        key = self.get_hash_key(pos)

        if key in closed:
            if pos in closed[key]:
                return True
        return False

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
    #-------------------------------------------------------------------------------------------------------------------

    def get_key(self, s, i, goal):
        """
        Calculate the f-value, the key, for cell s using heuristic i and weight w1

        :param s: target cell
        :param i: index of heuristic-value to pick
        :param goal: coordinates of goal cell
        :return: f-value of s for search i
        """
        s.h[i] = self.heuristics[i](s.pos, goal)
        f = s.g[i] + self.w1 * s.h[i]
        return f

    def expand_state(self, s, i, goal):
        """
        Expand
        :param s: cell to expand
        :param i: index for which fringe (OPEN) to expand s from
        :return: None
        """
        self.fringes[i].removed_cell(s)
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            if not self.contained_in_dict(neighbor.pos, self.visited[i]): # if s' was never generated (visited) in the ith search
                neighbor.g[i] = 20000
                neighbor.parent[i] = None

            cost = get_cost(s, neighbor)
            new_g = s.g[i] + cost
            if neighbor.g[i] > new_g:
                neighbor.g[i] = new_g
                neighbor.parent[i] = s
                if not self.contained_in_dict(neighbor.pos, self.closed[i]): # if neighbor has not been expanded in CLOSED_i yet
                    self.fringes[i].add_cell(neighbor, get_key(neighbor, i, goal)) # Insert/Update s' in OPEN_i with Key(s', i)

    def insert_in_closed(self, cell, closed):
        """
        Insert the given cell into the given closed dictionary

        :param cell: cell to place in closed
        :param closed: dictionary of hash keys to
        :return: None
        """
        hash_key = self.get_hash_key(cell.pos)
        if hash_key in closed:  # Uses hash to determine if key is in closed, still O(1)
            closed[hash_key].append(s.pos)
        else:
            closed[hash_key] = [s.pos]

    def search(self, start, goal):
        """
        Do sequential heuristic search on the grid, find a path from start to goal

        Parameters:
        start = coordinates of the start position
        goal = coordinates of the goal position

        Returns: path, a 1D array of coordinates ((x, y) tuples), None if path does not exist
        """

        """
        Things to do:
        - Find out where heuristics are applied
        - Keep track of visited nodes for search i
        - terminate and return path pointed by bp_i(s_goal)
        """
        start_cell = self.grid[start[0]][start[1]]
        goal_cell = self.grid[goal[0]][goal[1]]
        for i in range(self.num_heuristics):
            start_cell.g[i] = 0
            goal_cell.g[i] = 20000
            start_cell.parent[i] = None
            goal_cell.parent[i] = None
            start_cell.h[i] = self.heuristics[i](start_cell.pos, goal)
            self.fringes[i].add_cell(start_cell, self.get_key(start_cell, i, goal))

        min_key_0 = self.fringes[0].min_key
        while min_key_0 < 20000:
            for i in range(1, self.num_heuristics):
                min_key_i = self.fringes[i].min_key
                if min_key_i <= self.w2 * min_key_0:
                    if goal_cell.g[i] <= min_key_i:
                        if goal_cell.g[i] < 20000:
                            # terminate and return path pointed by bp_i(s_goal)
                        else:
                            s = self.fringes[i].pop_cell() # OPEN_i.TOP()?
                            self.expand_state(s, i, goal)
                            insert_in_closed(s, self.closed[i]) # Insert s in CLOSED_i
                else:
                    goal_g_0 = goal_cell.g[0]
                    if goal_g_0 <= self.fringes[0].min_key():
                        if goal_g_0 < 20000:
                            # terminate and return path pointed by bp_0(s_goal)
                    else:
                        s = self.fringes[0].pop()
                        self.expand_state(s, 0, goal)
                        insert_in_closed(s, self.closed[0])

        return None, -1, -1  # No path found, no nodes expanded