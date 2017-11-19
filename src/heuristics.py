
import math

def heu_linear(cell,goal):
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    h = math.sqrt(math.pow(cellXcor - xcor, 2) + math.pow(cellYcor - ycor, 2))
    cell.h = h
    return h

def heu_manhatan(cell,goal):
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    h = abs(cellXcor - xcor) + abs(cellYcor - ycor)
    cell.h = h
    return h


def heu_diagonal_brkingties(cell,goal):
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    h = abs(cellXcor - xcor) + abs(cellYcor - ycor) + (math.sqrt(2) - 2) * min(abs(cellXcor - xcor), abs(cellYcor - ycor))
    cell.h = h
    return h



def heu_eucliden_powtwo(cell,goal):
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    h = math.pow(abs(cellXcor - xcor), 2) + math.pow(abs(cellYcor - ycor), 2)
    cell.h = h
    return h


def heu_sample(cell,goal):
    xcor = goal[0]
    ycor = goal[1]
    cellXcor = cell[0]
    cellYcor = cell[1]
    manhaX = abs(cellXcor - xcor)
    manhaY = abs(cellYcor - ycor)
    h = math.sqrt(2) * min(manhaX, manhaY) + max(manhaX, manhaY) - min(manhaX, manhaY)
    cell.h = h
    return h
