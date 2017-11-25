import math

def heu_euclidean(cell,goal):
    """
    Euclidean distance heuristic. Assume on "highway" (cut distance by 4)

    :param cell: a cell on the grid
    :param goal: coordinates of the goal
    :return: heuristic value for the cell
    """
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    dx = cellXcor - xcor
    dy = cellYcor - ycor
    h = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))/4
    return h

def heu_manhattan(cell,goal):
    """
    Manhattan distance heuristic (allow only vertical and horizontal movements).
    Assume movement is along highways (divide movement costs by 4)

    :param cell: a cell on the grid
    :param goal: coordinates of the goal
    :return: heuristic value for the cell
    """
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    dx = abs(cellXcor - xcor)/4
    dy = abs(cellYcor - ycor)/4
    h = dx + dy
    return h


def heu_diagonal(cell,goal):
    """
    Similar to Manhattan distance, but allow diagonal movements.
    Assume you travel on a highway the entire distance (cut movement cost by 4)

    :param cell: a cell on the grid
    :param goal: coordinates of the goal
    :return: heuristic value for the cell
    """
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    dx = abs(cellXcor - xcor) # x distance for manhattan distance
    dy = abs(cellYcor - ycor) # y distance for manhattan heuristic
    D = 0.25 # cost to move horizontally or vertically between cells (along highway)
    D2 = math.sqrt(2)/4.0 # cost to move diagonally (along highway)
    h = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    return h

def heu_euclidean_squared(cell,goal):
    """
    Similar to Euclidean distance, but saves on square root computation time

    :param cell: a cell on the grid
    :param goal: coordinates of the goal
    :return: heuristic value for the cell
    """
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    h = (math.pow(abs(cellXcor - xcor), 2) + math.pow(abs(cellYcor - ycor), 2))/16.0
    return h


def heu_sample(cell,goal):
    """
    Heuristic given in the assignment instructions.

    :param cell: a cell on the grid
    :param goal: coordinates of the goal
    :return: heuristic value for the cell
    """
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    dx = abs(cellXcor - xcor)
    dy = abs(cellYcor - ycor)
    h = math.sqrt(2) * min(dx, dy) + max(dx, dy) - min(dx, dy)
    return h
