import math

def heu_linear(cell,goal):
    """
    Euclidean distance heuristic

    :param cell: a cell on the grid
    :param goal: coordinates of the goal
    :return: heuristic value for the cell
    """
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    h = math.sqrt(math.pow(cellXcor - xcor, 2) + math.pow(cellYcor - ycor, 2))
    return h

def heu_manhatan(cell,goal):
    """
    Manhattan distance heuristic (allow only vertical and horizontal movements)

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
    h = dx + dy
    return h


def heu_diagonal(cell,goal):
    """
    Similar to Manhattan distance, but allow diagonal movements

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
    h = dx + dy + (math.sqrt(2) - 2) * min(dx, dy)
    return h



def heu_eucliden_squared(cell,goal):
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
    h = math.pow(abs(cellXcor - xcor), 2) + math.pow(abs(cellYcor - ycor), 2)
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
    manhaX = abs(cellXcor - xcor)
    manhaY = abs(cellYcor - ycor)
    h = math.sqrt(2) * min(manhaX, manhaY) + max(manhaX, manhaY) - min(manhaX, manhaY)
    return h
