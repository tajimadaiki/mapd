import  sys
sys.path.append( "./mapf" )

from config import Config
from agent_mapd import AgentMAPD
from task import Task
from typing import List, Dict

class ConfigMAPD(Config):
    def __init__(self, config_file: str):
        super().__init__(config_file)
        self.agents_mapd: List[AgentMAPD] = []
        self.tasks: Dict[int: List[Task]] = dict()
        self._load_agent_mapd()
        self._load_tasks()
    
    def _load_agent_mapd(self):
        for id in self.agents_id:
            init_pos = self.init_pos[id]
            agent_mapd = AgentMAPD(id, init_pos)
            self.agents_mapd.append(agent_mapd)
    
    def _load_tasks(self):
        task_ws = self._wb['task']
        task_dict: Dict[int: Task] = dict() # id: task
        keys = dict()
        self.tasks_num = task_ws.max_row - 1
        for row in range(1, task_ws.max_row + 1):
            time = int()
            pickup_loc = tuple()
            delivery_loc = tuple()
            chain_task_id = -1
            chain_task_type = 'none'
            for col in range(1, task_ws.max_column + 1):
                if row == 1:
                    key = str(task_ws.cell(row, col).value)
                    keys[col] = key
                else:
                    value = str(task_ws.cell(row, col).value)
                    if keys[col] == 'id': 
                        id = int(value)
                    if keys[col] == 'time': 
                        time = int(value)
                    if keys[col] == 'chain_task_id': 
                        if value != 'none':
                            chain_task_id = int(value)
                    if keys[col] == 'chain_type': 
                        if value != 'none':
                            chain_task_type = value
                    if keys[col] == 'pickup_loc':
                        pickup_loc = self.endpoints[value]
                    if keys[col] == 'delivery_loc':
                        delivery_loc = self.endpoints[value]
            if row != 1:
                # create task
                task = Task(id, pickup_loc, delivery_loc)
                # record task
                if time != -1:
                    self.tasks.setdefault(time, []).append(task)
                task_dict[id] = task
                # if this task chain other task
                if chain_task_id != -1:
                    if chain_task_type == 'start':
                        task_dict[chain_task_id].add_start_chain_task(task)
                    if chain_task_type == 'finish':
                        task_dict[chain_task_id].add_finish_chain_task(task)


if __name__ == "__main__":
    config_file = "./config/config_test.xlsx"
    config = ConfigMAPD(config_file)
    print(config.agents)
    print(config.agents_id)
    print(config.endpoints)
    print(config.tasks)
    print(config.tasks[0][0].start_chain_task)