import  sys
sys.path.append( "./mapf" )

from agent import Agent
from task import Task
from typing import Tuple
import numpy as np

class AgentMAPD(Agent):
    def __init__(self, 
                 agent_id: str,
                 init_pos: Tuple[int, int]):
        super().__init__(agent_id)
        self.pos = init_pos
        self.path = np.array(init_pos)
        self.next_destination = init_pos
        self.delivering = False
        self.task: Task = None
        

if __name__ == "__main__":
    agent = AgentMAPD('001', (0, 3))
    print(agent, agent.pos)