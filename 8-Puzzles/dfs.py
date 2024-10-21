class dfsAgent:
    def __init__(self, initial_State):
        self.explored = set()
        self.path = []
        self.parent = {}
        self.goal = 12345678
        self.initial_State = self.prepare_initial_state(initial_State)
    def dfs(self):
        stack = []
        stack.append(self.initial_State)
        while stack:
            current = stack.pop()
            if current == self.goal:
                print(current)
                # self.get_path(current)
                return self.path
            if current not in self.explored:
                self.explored.add(current)
                for child in self.get_children(current):
                    stack.append(child)
                    self.parent[child] = current

        return None

    def prepare_initial_state(self ,initial_State : list[list[int]]) -> int:
        k = 8
        intial = 0
        for i in range(3):
            for j in range(3):
                intial += initial_State[i][j] * (10 ** k)
                k -= 1

        return intial
    def get_children(self, state: int) -> list[int]:
        children = []
        state = str(state)
        if len(state) != 9:
            state = '0' + state
        zero_index = state.index('0')
        if zero_index != 0 and zero_index != 1 and zero_index != 2:
            children.append(int(self.swap(state, zero_index, zero_index - 3)))
        if zero_index != 0 and zero_index != 3 and zero_index != 6:
            children.append(int(self.swap(state, zero_index, zero_index - 1)))
        if zero_index != 6 and zero_index != 7 and zero_index != 8:
            children.append(int(self.swap(state, zero_index, zero_index + 3)))
        if zero_index != 2 and zero_index != 5 and zero_index != 8:
            children.append(int(self.swap(state, zero_index, zero_index + 1)))
        return children
    def swap(self, state: str, i: int, j: int) -> str:
        state = list(state)
        state[i], state[j] = state[j], state[i]
        return ''.join(state)
    def get_path(self, state: int):
        if state == self.initial_State:
            return
        self.path.append(state)
        print(state)
        self.get_path(self.parent[state])
l = dfsAgent([[1,0,2], [3,4,5], [6, 7, 8]])

print(l.dfs())
