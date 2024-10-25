import time


class IdsAgent:

    def __init__(self, initial_State):

        self.explored = set()
        self.path = []
        self.parent = {}
        self.level ={}
        self.goal = 12345678
        self.initial_State = self.prepare_initial_state(initial_State)

    def iterative_dfs(self):
        limit = 0
        start_time = time.time()
        while limit <= 32:

            self.explored = set()
            self.path = []
            self.parent = {}
            path, path_length, expand_length, max_depth = self.dfs(limit)
            if path:
                end_time = time.time()
                return path, path_length, expand_length, max_depth, end_time - start_time
            limit += 1
        end_time = time.time()
        return None, None, None, 32, end_time - start_time

    def dfs(self, limit: int):
        stack = [(self.initial_State, 0)]
        max_depth = 0
        while stack:
            current, level = stack.pop()
            max_depth = max(max_depth, level)
            self.explored.add(current)
            self.level[current] = level
            if current == self.goal:
                self.get_path(current)
                return self.path, len(self.path), len(self.explored), max_depth
            if level < limit:
                for child in self.get_children(current):
                    if (child[0] not in self.explored or (child[0]  in self.explored and self.level[child[0]] > level + 1 )) and (self.not_in_stack(child[0], stack, level)):
                        stack.append((child[0], level + 1))
                        self.parent[child[0]] = (current, child[1])
        return None, None, len(self.explored), max_depth

    def not_in_stack(self, state: int, stack: list , level) -> bool:
        for s in stack:
            if s[0] == state and s[1] < level + 1 :
                return False
        return True

    def prepare_initial_state(self, initial_State: list[list[int]]) -> int:
        k = 8
        intial = 0
        for i in range(3):
            for j in range(3):
                intial += initial_State[i][j] * (10 ** k)
                k -= 1

        return intial

    def get_children(self, state: int) -> list[(int, str)]:
        children = []
        state = str(state)
        if len(state) != 9:
            state = '0' + state
        zero_index = state.index('0')

        if zero_index % 3 != 2:
            children.append((int(self.swap(state, zero_index, zero_index + 1)), "right"))
        if zero_index + 3 < 9:
            children.append((int(self.swap(state, zero_index, zero_index + 3)), "down"))
        if zero_index % 3 != 0:
            children.append((int(self.swap(state, zero_index, zero_index - 1)), "left"))
        if zero_index - 3 >= 0:
            children.append((int(self.swap(state, zero_index, zero_index - 3)), "up"))




        return children

    def swap(self, state: str, i: int, j: int) -> str:
        state = list(state)
        state[i], state[j] = state[j], state[i]
        return ''.join(state)

    def get_path(self, state: int):
        while state != self.initial_State:
            self.path.append((state, self.parent[state][1]))
            state = self.parent[state][0]
        self.path.reverse()
        return

#
# ids = IdsAgent([[8,6,7], [2,5,4], [3,0,1]])
# print(ids.iterative_dfs())
#
#
# # [[0,3,5], [4,2,8], [6,1,7]] 10
# # [[3,2,8], [4,5,1], [6,7,0]] 12
# #[[3,2,8], [4,5,1], [6,0,7]]
#
# # ([(305428617, 'right'), (325408617, 'down'), (325418607, 'down'), (325418670, 'right'), (325410678, 'up'), (320415678, 'up'), (302415678, 'left'), (312405678, 'down'), (312045678, 'left'), (12345678, 'up')],
# # ([(305428617, 'right'), (325408617, 'down'), (325418607, 'down'), (325418670, 'right'), (325410678, 'up'), (320415678, 'up'), (302415678, 'left'), (312405678, 'down'), (312045678, 'left'), (12345678, 'up')], 10, 242, 10, 0.001993417739868164)