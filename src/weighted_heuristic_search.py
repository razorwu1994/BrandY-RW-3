from heuristic_search import HeuristicSearch

class WeightedHeuristicSearch(HeuristicSearch):
    """
    Class that performs weighted heuristic search on a 160x120 grid.
    Use search to find a path of coordinates to follow from start to finish.

    Attributes:
    grid = 160x120 grid of cells that represent the map
    """

    def __init__(self, grid, heuristic, weight):
        HeuristicSearch.__init__(self, grid, heuristic)
        self.weight = float(weight)

    def apply_heuristic(self, cell, goal):
        """
        Calculate and set the heuristic for a cell

        Parameters:
        cell = target cell
        goal = coordinates of goal cell

        Returns: h value for the cell
        """
        cell.h = self.weight * self.heuristic(cell.pos, goal)
        return cell.h