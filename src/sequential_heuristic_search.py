import math
from priority_queue import PriorityQueue
import heuristics as hrsts
from cell2 import Cell2

# Constants for terrain type
BLOCKED = 0
UNBLOCKED = 1
ROUGH = 2  # aka hard-to-traverse

class SequentialHeuristicSearch:
    """
    Class that performs sequential heuristic search on a 160x120 grid.
    Use search to find a path of coordinates to follow from start to finish.

    Attributes:
    grid = 160x120 grid of cells that represent the map
    w1 = weight used to inflate heuristic values like in weighted A*
    w2 = weight used to prioritize inadmissible search processes over the admissible one (the anchor)
    """

    def __init__(self, grid, w1, w2):
        self.grid = grid
        self.w1 = w1
        self.w2 = w2

    def key(self, s, i):
        """

        :param s: cell with
        :param i:
        :return:
        """

    def search(self, start, goal):
        """
        Do sequential heuristic search on the grid, find a path from start to goal

        Parameters:
        start = coordinates of the start position
        goal = coordinates of the goal position

        Returns: path, a 1D array of coordinates ((x, y) tuples), None if path does not exist
        """


        return None, -1, -1  # No path found, no nodes expanded