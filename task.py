import  sys
sys.path.append( "./mapf" )

from typing import Tuple


class Task:
    def __init__(self,
                 pickup_loc: Tuple[int, int],
                 delivery_loc: Tuple[int, int]):
        self.pickup_loc = pickup_loc
        self.delivery_loc = delivery_loc
    
    def add_start_chain_task(self, chain_task):
        self.start_chain_task = chain_task
    
    def add_finish_chain_task(self, chain_task):
        self.finish_chain_task = chain_task

    def __str__(self):
        return str(f'task:pickup{self.pickup_loc}_delivery{self.delivery_loc}')

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    task = Task((2, 5), (10, 3))
    next_task = Task((2, 5), (5, 2))
    task.add_start_chain_task(next_task)
    print(task)
