import math
from priority_queue import PriorityQueue
import heuristics as hrsts
from cell import Cell

# Constants for terrain type
BLOCKED = 0
UNBLOCKED = 1
ROUGH = 2  # aka hard-to-traverse

class SequentialHeuristicSearch:
    """
    Class that performs uniform cost search on a 160x120 grid.
    Use search to find a path of coordinates to follow from start to finish.

    Attributes:
    grid = 160x120 grid of cells that represent the map

    """

    def __init__(self, grid):
        self.grid = grid

    def search(self, start, goal):
        """
        Do uniform cost search on the grid, find a path from start to goal

        Parameters:
        start = coordinates of the start position
        goal = coordinates of the goal position

        Returns: path, a 1D array of coordinates ((x, y) tuples), None if path does not exist
        """


        return None, -1, -1  # No path found, no nodes expanded