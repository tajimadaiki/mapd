import  sys
sys.path.append( "./mapf" )

from typing import Tuple, List


class Task:
    def __init__(self,
                 id: int,
                 pickup_loc: Tuple[int, int],
                 delivery_loc: Tuple[int, int]):
        self.pickup_loc = pickup_loc
        self.delivery_loc = delivery_loc
        self.start_chain_task: List[Task] = []
        self.finish_chain_task: List[Task] = []
    
    def add_start_chain_task(self, chain_task):
        self.start_chain_task.append(chain_task)
    
    def add_finish_chain_task(self, chain_task):
        self.finish_chain_task.append(chain_task)

    def __str__(self):
        return str(f'task:pickup{self.pickup_loc}_delivery{self.delivery_loc}')

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    task = Task(0, (2, 5), (10, 3))
    if task.start_chain_task is not None:
        print('ctart chain task 1')
    next_task = Task(1, (2, 5), (5, 2))
    task.add_start_chain_task(next_task)
    if task.start_chain_task is not None:
        print('ctart chain task 2')
    print(task)
