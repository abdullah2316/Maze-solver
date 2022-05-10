from grid import Grid


class priorityQ:
    def __init__(self, priority):
        self.data: list[Grid] = []
        self.priority = priority

    def insert(self, element: Grid):
        self.data.append(element)
        if self.priority == 'c':
            self.data.sort(key=lambda x: x.cost)
        elif self.priority == 'h':
            self.data.sort(key=lambda x: x.heuristic)

    def is_in(self, element: Grid) -> int:
        for i in range(0, len(self.data)):
            if self.data[i].get_agentposition() == element.get_agentposition():
                return i
        return -1

    def printQ(self):
        for g in self.data:
            print(g.get_cost(), end=" ")
        print()

    def replace(self, element: Grid, index: int):
        del self.data[index]
        self.insert(element)


    def empty(self):
        if len(self.data) == 0:
            return True
        return False

    def get(self):
        node = self.data.pop(0)
        if self.priority == 'c':
            self.data.sort(key=lambda x: x.cost)
        elif self.priority == 'h':
            self.data.sort(key=lambda x: x.heuristic)
        return node
