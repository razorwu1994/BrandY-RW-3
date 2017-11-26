class Cell:
    """
    Represents a cell in the 160x120 grid for sequential search

    Attr:
        pos: coordinates for this cell in the form of 2-tuple: (x, y)
        parent: previously visited Cell before reaching current one, None by default
        terrain_type: 0 for blocked, 1 for unblocked, 2 for hard-to-traverse
        has_highway: 0 if it has no highway, 1 if it does
        f: function value
        g: distance from start
        h: heuristic value

    Only unblocked (1) and hard-to-traverse (2) terrains can have highways.
    """

    def __init__(self, pos, terrain_type, has_highway):
        """
        By default, set f = 0, g = 20000, h = 0
        """
        self.pos = pos
        self.parent = None
        self.terrain_type = terrain_type
        self.has_highway = has_highway
        self.g = 20000  # 20000 represents infinity
        self.h = 0
        self.f = self.g + self.h

    def convert_to_char(self):
        """
        Converts cell to '0', '1', '2', 'a' or 'b' depending on its characteristics
        """
        if self.terrain_type == 1 and self.has_highway == True:
            return 'a'
        elif self.terrain_type == 2 and self.has_highway == True:
            return 'b'
        else:
            return str(self.terrain_type)

    def __eq__(self, other):
        """
        Compare two cells based on their positions
        """
        if not isinstance(other, Cell):
            return False

        if self.pos == other.pos:
            return True
        return False

    def __str__(self):
        """
        Prints out the Cell in format ((x, y), f, g, h)
        """
        t_type = self.convert_to_char()
        return "(({0}, {1}), {2}, f={3}, g={4}, h={5})".format(self.pos[0], self.pos[1], t_type, self.f, self.g, self.h)

    def __hash__(self):
        """
        Hash this cell

        :return: for cell (x,y), hash((x, y))
        """
        return hash(self.pos)