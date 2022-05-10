import copy
from queue import Queue, LifoQueue

from scipy.spatial.distance import cityblock

from GUI import UI_init
from priorityQ import *


def m_heuristic(node, goal_node) -> int:
    return int(cityblock(node, goal_node))


def remove_costs(explored: list[tuple]):
    return explored[::2]


def greedy(root: Grid, explored, goal_node: Grid):
    q = priorityQ('h')
    t = tuple()
    t = copy.deepcopy(m_heuristic(root.get_agentposition(), goal_node.get_agentposition()))
    root.heuristic = t
    q.insert(root)
    while not q.empty():
        node = q.get()
        explored.append(node.get_agentposition())
        explored.append(node.heuristic)
        if node.goal_check():
            return node
        c = get_children(node, 'left')
        if c is not None:
            t = tuple()
            t = copy.deepcopy(m_heuristic(c.get_agentposition(), goal_node.get_agentposition()))
            c.heuristic = t
            if duplicate_state3(c, explored, q):
                node.add(c)

        c = get_children(node, 'right')
        if c is not None:
            c.heuristic = m_heuristic(c.get_agentposition(), goal_node.get_agentposition())
            if duplicate_state3(c, explored, q):
                c.heuristic = m_heuristic(c.get_agentposition(), goal_node.get_agentposition())
                node.add(c)

        c = get_children(node, 'up')
        if c is not None:
            c.heuristic = m_heuristic(c.get_agentposition(), goal_node.get_agentposition())
            if duplicate_state3(c, explored, q):
                c.heuristic = m_heuristic(c.get_agentposition(), goal_node.get_agentposition())
                node.add(c)

        c = get_children(node, 'down')
        if c is not None:
            c.heuristic = m_heuristic(c.get_agentposition(), goal_node.get_agentposition())
            if duplicate_state3(c, explored, q):
                c.heuristic = m_heuristic(c.get_agentposition(), goal_node.get_agentposition())
                node.add(c)

    return None


# add to GitHub
def UCS(root: Grid, explored):
    q = priorityQ('c')
    q.insert(root)
    while not q.empty():
        node = q.get()
        explored.append(node.get_agentposition())
        explored.append(node.cost)
        if node.goal_check():
            return node
        c = get_children(node, 'left')
        if c is not None:
            if duplicate_state2(c, explored, q):
                node.add(c)

        c = get_children(node, 'right')
        if c is not None:
            if duplicate_state2(c, explored, q):
                node.add(c)

        c = get_children(node, 'up')
        if c is not None:
            if duplicate_state2(c, explored, q):
                node.add(c)

        c = get_children(node, 'down')
        if c is not None:
            if duplicate_state2(c, explored, q):
                node.add(c)

    return None


def DFS(root, explored):
    frontier = []
    q = LifoQueue(maxsize=0)
    q.put(root)
    frontier.append(root.get_agentposition())
    while not q.empty():
        node = q.get()
        explored.append(node.get_agentposition())
        if node.goal_check():
            return node
        c = get_children(node, 'left')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
        c = get_children(node, 'right')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
        c = get_children(node, 'up')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
        c = get_children(node, 'down')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
    return None


# change in DFS
def BFS(root, explored):
    # Read start/root state from file
    # initialize
    frontier = []
    q = Queue(maxsize=0)
    q.put(root)
    frontier.append(root.get_agentposition())
    while not q.empty():
        node = q.get()
        explored.append(node.get_agentposition())
        if node.goal_check():
            return node
        c = get_children(node, 'left')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
        c = get_children(node, 'right')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
        c = get_children(node, 'up')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
        c = get_children(node, 'down')
        if c is not None:
            if duplicate_state(c.get_agentposition(), frontier):
                node.add(c)
                q.put(c)
    return None


def populate_grid():
    with open('input.txt') as f:
        grid_data = []
        for line in f:
            line = line.split()
            if line:
                line = [int(i) for i in line]
                grid_data.append(line)
    return grid_data


def duplicate_state(agent: tuple[int, int], frontier: list[tuple]) -> bool:
    if agent not in frontier:
        frontier.append(agent)
        return True

    return False


def duplicate_state2(child, explored: list[tuple], frontier: priorityQ) -> bool:
    index = frontier.is_in(child)
    if index != -1:  # in frontier
        if child.get_cost() < frontier.data[index].get_cost():  # it's a node with better cost
            frontier.replace(child, index)
    elif child.get_agentposition() not in explored:  # not in frontier not in explored
        frontier.insert(child)
    else:  # in explored
        pos = explored.index(child.get_agentposition()) + 1
        t1 = tuple()
        t1 = copy.deepcopy(explored[pos])
        if t1 > explored[pos]:  # with  better cost
            frontier.insert(child)
    return False


# for greedy
def duplicate_state3(child, explored: list[tuple], frontier: priorityQ) -> bool:
    index = frontier.is_in(child)
    if index != -1:  # in frontier
        if child.heuristic < frontier.data[index].heuristic:  # it's a node with better cost
            frontier.replace(child, index)
    elif child.get_agentposition() not in explored:  # not in frontier not in explored
        frontier.insert(child)
    else:  # in explored
        pos = explored.index(child.get_agentposition()) + 1
        t1 = tuple()
        t1 = copy.deepcopy(explored[pos])
        if t1 > explored[pos]:  # with  better cost
            frontier.insert(child)

    return False


# duplicate states
def get_children(parent_state: Grid, action: str):
    pos = parent_state.get_agentposition()
    sizeg = parent_state.get_size()
    data = copy.deepcopy(parent_state.get_List())
    child = None
    # moving agent left
    if action == 'left':
        if pos[1] - 1 >= 0 and data[pos[0]][pos[1] - 1] != 1:
            state_data = copy.deepcopy(parent_state.get_List())
            child = Grid(state_data, sizeg, pos, parent_state)
            child.setagent(pos[0], pos[1] - 1)
            child.cost = parent_state.cost + 1
            # check duplicate
            # parent_state.add(child1)

    # moving agent right
    elif action == 'right':
        if pos[1] + 1 <= sizeg[1] - 1 and data[pos[0]][pos[1] + 1] != 1:
            state_data = copy.deepcopy(parent_state.get_List())
            child = Grid(state_data, sizeg, pos, parent_state)
            child.setagent(pos[0], pos[1] + 1)
            child.cost = parent_state.cost + 1
            # parent_state.add(child2)

    # moving agent up
    elif action == 'up':
        if pos[0] - 1 >= 0 and data[pos[0] - 1][pos[1]] != 1:
            state_data = copy.deepcopy(parent_state.get_List())
            child = Grid(state_data, sizeg, pos, parent_state)
            child.setagent(pos[0] - 1, pos[1])
            child.cost = parent_state.cost + 1
            # parent_state.add(child3)

        # moving agent down
    else:
        if pos[0] + 1 <= sizeg[0] - 1 and data[pos[0] + 1][pos[1]] != 1:
            state_data = copy.deepcopy(parent_state.get_List())
            child = Grid(state_data, sizeg, pos, parent_state)
            child.setagent(pos[0] + 1, pos[1])
            child.cost = parent_state.cost + 1
            # parent_state.add(child4)
    return child


if __name__ == "__main__":
    visited = []
    T = populate_grid()
    size = T[0]
    del T[0]
    state = T[:size[0]]
    start_position = tuple((T[size[0]][0], T[size[0]][1]))
    end_position = tuple((T[size[0] + 1][0], T[size[0] + 1][1]))
    T.clear()
    start_state = Grid(state, size, start_position)
    goal_state = Grid(state, size, end_position)
    # select search

    # for BFS uncomment following line
    # goal = BFS(start_state, visited)

    # for DFS uncomment following line
    # goal = DFS(start_state, visited)

    # for UCS uncomment following 2 lines
    # goal = UCS(start_state, visited)
    # visited = remove_costs(visited)  # visited paths without costs

    # for greedy uncomment following 2 lines
    goal = greedy(start_state, visited, goal_state)
    visited = remove_costs(visited)  # visited paths without costs

    # print(visited, "\n", goal, "\n", state, "\n", size)
    if goal is not None:
        UI_init(state, size, visited, goal)

    else:
        print("goal not found")
