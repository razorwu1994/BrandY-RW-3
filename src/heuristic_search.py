from uniform_cost_search import UniformCostSearch

class HeuristicSearch(UniformCostSearch):
    """
    Class that performs heuristic search on a 160x120 grid.
    Use search to find a path of coordinates to follow from start to finish.

    Attributes:
    grid = 160x120 grid of cells that represent the map
    """

    def __init__(self, grid, heuristic):
        UniformCostSearch.__init__(self, grid)
        self.heuristic = heuristic

    def apply_heuristic(self, cell, goal):
        """
        Calculate and set the heuristic for a cell

        Parameters:
        cell = target cell
        goal = coordinates of goal cell

        Returns: h value for the cell
        """
        cell.h = self.heuristic(cell, goal)
        return cell.h