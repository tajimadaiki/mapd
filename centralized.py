import  sys
sys.path.append( "./mapf" )

from conflict_based_search import ConflictBasedSearch
from agent_mapd import AgentMAPD
from task import Task
from munkres import Munkres
import numpy as np
from typing import List, Tuple, Dict


class CentralizedAlgorithm:
    def __init__(self,
                 agents: AgentMAPD,
                 map: List[List[str]],
                 endpoints: List[Tuple[int, int]]):
        self.agents: List[AgentMAPD] = agents
        self.cbs = ConflictBasedSearch(self.agents, map)
        self.endpoints = endpoints
        self.remain_tasks: List[Task] = []
        self.in_delivery_tasks: List[Task] = []
        self.heuristic = self.cbs.low_level_planner.heuristic.single_shortest_path

    def plan(self):
        # update state
        self.update_agent_state()
        self.get_new_tasks()

        # chose free agents
        free_agents: List[AgentMAPD] = []
        for agent in self.agents:
            if not agent.delivering:
                free_agents.append(agent)

        # assign tasks
        self.assign_tasks(free_agents)

        # find path
        starts: Dict[AgentMAPD: Tuple[int, int]] = dict()
        goals: Dict[AgentMAPD: Tuple[int, int]] = dict()
        for agent in self.agents:
            starts[agent] = agent.pos
            goals[agent] = agent.next_destination
        path = self.cbs.plan(starts, goals)
        for agent in self.agents:
            agent.path = path[agent]
        return path

    def update_agent_state(self):
        # simulation 上でやる
        # agent の場所
        # agent のタスク実行状況
        # next_distination の変更
        pass

    def get_new_tasks(self):
        # simulation 上でやる
        # chainタスクの生成
        pass

    def assign_tasks(self, free_agents: List[AgentMAPD]):
        # no free agents
        if len(free_agents) == 0:
            return 0
        # hold: Record unusable location
        hold: Dict[Tuple[int, int]: bool] = dict()
        for task in self.in_delivery_tasks:
            hold[task.delivery_loc] = True
        tasks: List[Task] = []
        starts: List[Tuple[int, int]] = []
        # pick off tasks that start points are not held and different with each other
        for task in self.remain_tasks:
            if not hold.setdefault(task.pickup_loc, False):
                tasks.append(task)
                starts.append(task.pickup_loc)
                hold[task.pickup_loc] = True
        # if tasks are less than agents, add non-holding endpoints for each agent
        if len(starts) < len(free_agents):
            # choose the nearest endpoint ep for each agent
            for agent in free_agents:
                inf = 1001001001
                dist = inf
                nearest_ep = tuple()
                for ep in self.endpoints:
                    if hold.setdefault(ep, False):
                        continue
                    dist_ep = self.heuristic(agent.pos, ep)
                    if dist_ep < dist:
                        dist = dist_ep
                        nearest_ep = ep
                    hold[nearest_ep] = True
                    starts.append(nearest_ep)
        # compute cost matrix
        cost_mat = []
        inf = 1001001001
        large_c = 1000
        for i in range(len(free_agents)):  # i: free_agents index
            i_cost = []
            for j in range(len(starts)):  # j: starts index
                cost = inf
                if j < len(tasks):  # pickup loc
                    num = len(free_agents)
                    dist = self.heuristic(free_agents[i].pos, tasks[j].pickup_loc)
                    cost = num*large_c*dist
                else:  # parking loc
                    num = len(free_agents)
                    dist = self.heuristic(free_agents[i].pos, starts[j])
                    cost = num*large_c**2 + dist
                i_cost.append(cost)
            cost_mat.append(i_cost)
        cost_mat_np = np.array(cost_mat)
        ans_mat = Munkres().compute(cost_mat_np)

        # recode ans
        for ans in ans_mat:
            i = ans[0]
            j = ans[1]
            agent = free_agents[i]
            if j < len(tasks):
                task = tasks[j]
                agent.task = task
                agent.next_destination = task.pickup_loc
            else:
                agent.next_destination = starts[j]


if __name__ == "__main__":
    from config_mapd import ConfigMAPD
    config_file = "./config/config_test.xlsx"
    config = ConfigMAPD(config_file)
    print(config.init_pos)

    agents: List[AgentMAPD] = config.agents_mapd

    ca = CentralizedAlgorithm(agents, config.map, list(config.endpoints.values()))

    task0 = Task((0, 6), (4, 3))
    task1 = Task((4, 0), (4, 6))
    task2 = Task((4, 6), (4, 3))
    ca.remain_tasks = [task0, task1, task2]
    ca.assign_tasks(ca.agents)
    for agent in ca.agents:
        print(agent, agent.task)
    path = ca.plan()
    print(path)
