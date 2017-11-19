def heu_linear(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = math.sqrt(math.pow(r - xcor, 2) + math.pow(c - ycor, 2))
            col.h = h
            c += 1
        r += 1
    return grid

def heu_manhatan(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = abs(r - xcor) + abs(c - ycor)
            col.h = h
            c += 1
        r += 1
    return grid


def heu_diagonal_brkingties(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = abs(r - xcor) + abs(c - ycor) + (math.sqrt(2) - 2) * min(abs(r - xcor), abs(c - ycor))
            h = h * (1 + 0.01)  # 0.01 is the p to break tie
            col.h = h
            c += 1
        r += 1
    return grid


def heu_eucliden_powtwo(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            h = math.pow(abs(r - xcor), 2) + math.pow(abs(c - ycor), 2)
            col.h = h
            c += 1
        r += 1
    return grid


def heu_sample(start, goal, grid):
    xcor = goal[0]
    ycor = goal[1]
    r = 0
    c = 0
    for row in grid:
        for col in row:
            manhaX = abs(r - xcor)
            manhaY = abs(c - ycor)
            h = math.sqrt(2) * min(manhaX, manhaY) + max(manhaX, manhaY) - min(manhaX, manhaY)
            col.h = h
            c += 1
        r += 1
    return grid