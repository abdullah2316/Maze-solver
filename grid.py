
class Grid:
    def __init__(self, grid_info, gridsize, agent: tuple[int, int], parent=None, cost=0, heuristic: tuple = 0):
        self.grid_info = grid_info
        self.agentPosition = agent
        self.gridSize = gridsize
        self.children = []
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def print_grid(self):
        for r in self.grid_info:
            for c in r:

                if c == 0:
                    print("empty", end=" ")
                elif c == 1:
                    print("block", end=" ")
                elif c == 2:
                    print("agent", end=" ")
                elif c == 3:
                    print("start", end=" ")
                else:
                    print("goal", end=" ")
            print()
        print("agentPosition: ", self.agentPosition)

    def get_List(self) -> list:
        return self.grid_info

    def add(self, child):

        self.children.append(child)

    def get_agentposition(self) -> tuple[int, int]:
        return self.agentPosition

    def get_size(self) -> tuple[int, int]:
        return self.gridSize

    def get_cost(self) -> int:
        return self.cost

    def setagent(self, r: int, c: int):
        # self.grid_info[self.agentPosition[0]][self.agentPosition[1]] = 0
        # self.grid_info[r][c] = 2
        self.agentPosition = r, c

    def print_children(self):

        for c in self.children:
            c.print_grid()

    def get_children(self):
        return self.children

    def goal_check(self):
        if self.grid_info[self.agentPosition[0]][self.agentPosition[1]] == 4:
            return True
        else:
            return False
