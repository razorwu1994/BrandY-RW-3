INFINITY = 20000

class Cell2:
    """
    Represents a cell in the 160x120 grid for sequential search

    Attr:
        pos: coordinates for this cell in the form of 2-tuple: (x, y)
        parent: previously visited Cell before reaching current one, None by default
        terrain_type: 0 for blocked, 1 for unblocked, 2 for hard-to-traverse
        has_highway: 0 if it has no highway, 1 if it does
        g: list of distances from start
        h: list of heuristic values

    Only unblocked (1) and hard-to-traverse (2) terrains can have highways.
    """

    def __init__(self, pos, terrain_type, has_highway, num_heuristics):
        """
        By default, set all f's = 0, g's = 20000, h's = 0
        """
        self.pos = pos
        self.terrain_type = terrain_type
        self.has_highway = has_highway

        # For sequential search, have list of parents, g's, h's and (maybe) f's
        self.parent = []
        self.g = []
        self.h = []
        for i in range(num_heuristics):
            parent = None
            g = INFINITY
            h = 0
            self.parent.append(parent)
            self.g.append(g)  # 20000 represents infinity
            self.h.append(h)

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
        g_temp = self.g[:]
        h_temp = self.h[:]

        for i in range(len(f_temp)):
            g_temp[i] = round(g_temp[i], 2)
            h_temp[i] = round(h_temp[i], 2)

        return "(({0}, {1}), {2}, g={4}, h={5})".format(self.pos[0], self.pos[1], t_type, f_temp, g_temp, h_temp)

    def __hash__(self):
        """
        Hash this cell

        :return: for cell (x,y), hash((x, y))
        """
        return hash(self.pos)