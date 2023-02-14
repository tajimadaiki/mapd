import  sys
sys.path.append( "./mapf" )

from centralized import CentralizedAlgorithm
from config_mapd import ConfigMAPD
from agent_mapd import AgentMAPD
from task import Task
from typing import List, Tuple, Dict
import numpy as np


class Simulation:
    def __init__(self,
                 config: ConfigMAPD,
                 max_timestep: int):
        self.config = config
        self.agents: List[AgentMAPD] = config.agents_mapd
        endpoints = list(config.endpoints.values())
        self.centralized = CentralizedAlgorithm(self.agents, config.map, endpoints)
        self.tasks: Dict[int: List[Task]] = config.tasks  # {timestep: [task]}
        self.max_timestep = max_timestep
        self.path_log: Dict[AgentMAPD: np.ndarray] = dict()
        self._path_log: Dict[AgentMAPD: List[Tuple[int, int]]] = dict()
        self.state_log: Dict[AgentMAPD: List[str]] = dict()
        self.task_assign_log: List[int] = []
        self.task_deliver_log: List[int] = []

    def run(self):
        for timestep in range(self.max_timestep):
            print(timestep)
            print(f'remain_tasks: {self.centralized.remain_tasks}, '
                  f'in_delivery_tasks: {self.centralized.in_delivery_tasks}')
            self.centralized.plan()
            self.update(timestep)
            if len(self.centralized.remain_tasks) == 0 \
                  and len(self.centralized.in_delivery_tasks) == 0:
                print(f'finish all task at {timestep}')
                break
        self.path_log = self.agent_path()
        # print(self.path_log)

    def update(self, timestep: int):
        # recode hold
        hold: Dict[Tuple[int, int]: bool] = dict()
        for task in self.centralized.in_delivery_tasks:
            hold[task.delivery_loc] = True
        # add new tasks
        self.centralized.remain_tasks.extend(self.tasks.setdefault(timestep, []))

        for agent in self.agents:
            # update agent and task status
            # when agent finish assigned task
            if agent.delivering and agent.task.delivery_loc == agent.pos:
                print(f'finish {agent.task} by {agent}!')
                # add chain task
                if len(agent.task.finish_chain_task) != 0:
                    new_tasks = agent.task.finish_chain_task
                    self.centralized.remain_tasks.extend(new_tasks)
                    print('add finish chain tasks')
                # update
                self.centralized.in_delivery_tasks.remove(agent.task)
                agent.task = None
                agent.delivering = False
                agent.next_destination = agent.pos

            # when agent start assigned task
            if not agent.delivering \
                    and agent.task is not None \
                    and agent.task.pickup_loc == agent.pos \
                    and not hold.setdefault(agent.task.delivery_loc, False):
                print(f'{agent} starts {agent.task}!')
                # add chain task
                if len(agent.task.start_chain_task) != 0:
                    new_tasks = agent.task.start_chain_task
                    self.centralized.remain_tasks.extend(new_tasks)
                    print('add start chain tasks')
                # update
                agent.delivering = True
                ###########################################
                print(f'agent task: {agent.task}')
                ###########################################
                self.centralized.remain_tasks.remove(agent.task)
                self.centralized.in_delivery_tasks.append(agent.task)
                agent.next_destination = agent.task.delivery_loc

            # update agent pos
            agent.pos = tuple(agent.path[1]) if len(agent.path) > 1 else tuple(agent.path[0])

            # record log
            self._path_log.setdefault(agent, []).append(agent.pos)
            state = 'free'
            if agent.delivering:
                state = "delivering"
            self.state_log.setdefault(agent, []).append(state)
        self.task_assign_log.append(len(self.centralized.remain_tasks))
        self.task_deliver_log.append(len(self.centralized.in_delivery_tasks))

    def load_tasks(self, task_file_path):
        file = open(task_file_path, "r")
        if not file.mode == 'r':
            print("Could not open " + task_file_path)
        else:
            print("Loading task file")
            task_data = file.readlines()
            for line in task_data:
                timestep, xp, yp, xd, yd = map(int, line.split())
                task = Task((xp, yp), (xd, yd))
                self.tasks.setdefault(timestep, []).append(task)
        file.close()

    def agent_path(self):
        path_log: Dict[AgentMAPD: np.ndarray] = dict()
        for agent, path in self._path_log.items():
            path_np = np.array(path)
            path_log[agent] = path_np
        return path_log


if __name__ == "__main__":
    max_timestep = 20
    config_file = "./config/config_test.xlsx"
    config = ConfigMAPD(config_file)
    sim = Simulation(config, max_timestep)
    sim.run()
    print(sim.task_assign_log)
    print(sim.task_deliver_log)
