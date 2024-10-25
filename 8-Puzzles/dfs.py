import time

class DfsAgent:
    def __init__(self, initial_State):
        self.explored = set()
        self.path = []
        self.parent = {}
        self.goal = 12345678
        self.initial_State = self.prepare_initial_state(initial_State)

    def dfs(self):
        start_time = time.time()
        stack = [(self.initial_State, 0)]
        max_depth = 0
        while stack:
            current, level = stack.pop()
            max_depth = max(max_depth, level)
            self.explored.add(current)
            if current == self.goal:
                self.get_path(current)
                end_time = time.time()
                return self.path, len(self.path), len(self.explored), max_depth, end_time - start_time
            for child in self.get_children(current):
                if (child[0] not in self.explored) and (self.not_in_stack(child[0], stack)):
                    stack.append((child[0], level + 1))
                    self.parent[child[0]] = (current, child[1])
        end_time = time.time()
        return None, None, len(self.explored), max_depth, end_time - start_time

    def not_in_stack(self, state: int, stack: list) -> bool:
        for s in stack:
            if s[0] == state:
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

ids = DfsAgent([[8,6,7], [2,5,4], [3,0,1]])
print(ids.dfs())


