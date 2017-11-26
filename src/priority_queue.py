import itertools
import heapq as hq
from cell import Cell

REMOVED = '<removed-cell>'  # placeholder for a removed cell

class PriorityQueue:
    """
    Priority queue using heapq as a min binary heap.

    Attributes:
    heap = list of entries arranged in a heap
    entry_finder = mapping of cells to entries
    counter = unique sequence count
    size = # of non-removed entries in the queue
    """

    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.size = 0
        self.counter = itertools.count()

    def add_cell(self, cell, priority=0):
        """
        Add a new cell or update the priority of an existing cell

        :param cell: cell to add to the pq
        :param priority: priority of the given cell, default is 0
        :return: None
        """
        if cell in self.entry_finder:
            self.remove_cell(cell)
        count = next(self.counter)
        entry = [priority, count, cell]
        self.entry_finder[cell] = entry
        hq.heappush(self.pq, entry)
        self.size += 1

    def remove_cell(self, cell):
        """
        Mark an existing cell as REMOVED.  Raise KeyError if not found.

        :param cell: cell to remove from the heap
        :return: None
        """
        entry = self.entry_finder.pop(cell)
        entry[-1] = REMOVED
        self.size -= 1

    def pop_cell(self):
        """
        Remove and return the lowest priority cell. Raise KeyError if empty.

        :return: cell with the lowest priority
        """
        while self.pq:
            priority, count, cell = hq.heappop(self.pq)
            if cell is not REMOVED:
                self.size -= 1
                del self.entry_finder[cell]
                return cell
        raise KeyError('pop from an empty priority queue')

    def min_key(self):
        """
        Peek at the priority (KEY) of the lowest priority cell

        :return: priority of the lowest priority cell
        """
        if self.size == 0:
            raise KeyError('peek into empty priority queue')

        priority, count, cell = self.pq[0]
        return priority

    def __len__(self):
        return self.size

    def __contains__(self, cell):
        return True if cell in self.entry_finder else False