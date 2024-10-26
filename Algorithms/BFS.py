from queue import Queue
import queue
import time
from typing import List, Set

class BFSAgent:
    def __init__(self, initial_State):
        self.explored = set()
        self.path = [] 
        self.parent = {}
        self.goal = 12345678
        self.initial_State = self.prepare_initial_State(initial_State)

    def get_children(self, state: int) -> list[tuple[int, str]]:
        children = []
        state = str(state)
        if len(state) != 9:
            state = '0' + state
        zero_index = state.index('0')
        if zero_index != 0 and zero_index != 1 and zero_index != 2:
            children.append((int(self.swap(state, zero_index, zero_index - 3)),'UP'))
        if zero_index != 6 and zero_index != 7 and zero_index != 8:
            children.append((int(self.swap(state, zero_index, zero_index + 3)),'DOWN'))
        if zero_index != 0 and zero_index != 3 and zero_index != 6:
            children.append((int(self.swap(state, zero_index, zero_index - 1)),"LEFT"))
        if zero_index != 2 and zero_index != 5 and zero_index != 8:
            children.append((int(self.swap(state, zero_index, zero_index + 1)),"RIGHT"))
        return children
    
    def swap(self, state: str, i: int, j: int) -> str:
        state = list(state)
        state[i], state[j] = state[j], state[i]
        return ''.join(state)
    
 
    def get_path(self, state: int):
        if state not in self.parent:
            return
        self.get_path(self.parent[state][0])  
        self.path.append((state, self.parent[state][1])) 

    def prepare_initial_State(self ,initial_State : list[list[int]]) -> int:
        k = 8
        intial = 0
        for i in range(3):
            for j in range(3):
                intial += initial_State[i][j] * (10 ** k)
                k -= 1
        return intial
    
    def BFS (self):
        res = self.BFS_()
        if res[0]==None :
           # print("#####UNSOLVABLE!#####")
           # print("expanded nodes : " ,res[2])
            pass
        else:
        #     print("#####SOLVABLE#####")
        #     print("path : " ,res[0])
        #     print("cost : ",res[1])
        #     print("expanded nodes : " ,res[2])
        #     print("search depth : " ,res[3])
        # print("time elapsed : ",res[4])
            pass
     

            
    def BFS_ (self):
        start_time = time.time()
        frontier_set = set()
        frontier = Queue()
        frontier.put(self.initial_State)
        frontier_set.add(self.initial_State)
        parent ={}
        while(not frontier.empty()):
            state = frontier.get()
            self.explored.add(state)
            if state== self.goal:
                self.get_path(state)
                end_time = time.time()
                formated_path = [(self.initial_State, self.path[0][1])] + [(self.path[i - 1][0], self.path[i][1]) for i in range(1, len(self.path))]
                formated_path.append((12345678, ''))
                return formated_path, len(self.path), len(self.explored), len(self.path) - 1, end_time-start_time
            
            children = self.get_children(state)
            for child in children:
                if child[0] not in self.explored and child[0] not in frontier_set:
                    frontier.put(child[0])
                    frontier_set.add(child[0])
                    self.parent[child[0]] = (state,child[1])
        end_time = time.time()
       
        return None , None, len(self.explored),None,end_time-start_time




#
# l = BFSAgent(
# [[1, 8, 2],
#  [0, 4, 3],
#  [7, 6, 5]]
# )
# res =l.BFS_()
#
# print(res)