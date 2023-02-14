import  sys
sys.path.append( "./mapf" )
from typing import Dict, List
from agent import Agent
from simulation import Simulation
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches


class Visualizer:

    def __init__(self,
                 simulation: Simulation,
                 speed: float = 1.0,
                 step_div=5):
        self.grid_size_x = simulation.config.grid_size_x
        self.grid_size_y = simulation.config.grid_size_y
        self.static_obstacles = simulation.config.static_obstacles
        self.endpoints = list(simulation.config.endpoints.values())
        self.solution = simulation.path_log
        self.state_log = simulation.state_log
        self.task_assign_log = simulation.task_assign_log
        self.task_deliver_log = simulation.task_deliver_log
        self.traject: Dict[Agent, np.ndarray] = dict()
        self.state_traject: Dict[Agent, List[str]] = dict()
        self.step_div = step_div
        self.speed = speed
        self.path_steps = 0
        self.traj_steps = 0
        self._set_steps()
        self._make_traject()

    def _set_steps(self):
        for path in self.solution.values():
            self.path_steps = max(self.path_steps, len(path))
        self.traj_steps = int(self.path_steps * self.step_div + 1)

    def _make_traject(self):
        for agent, path in self.solution.items():
            traj_x = np.array([path[0][0]])
            traj_y = np.array([path[0][1]])
            self.state_traject[agent] = ['free']
            for timestep in range(len(path)-1):
                now_pos = path[timestep]
                next_pos = path[timestep+1]
                for i in range(self.step_div):
                    i_pos = now_pos + (next_pos-now_pos)/self.step_div*(i+1)
                    traj_x = np.append(traj_x, i_pos[0])
                    traj_y = np.append(traj_y, i_pos[1])
                    if self.state_log is not None:
                        self.state_traject[agent].append(self.state_log[agent][timestep])
                    else:
                        self.state_traject[agent].append('free')
            self.traject[agent] = np.stack([traj_x, traj_y], 1)

    def plot(self, save=False, name='anim', display_tasks=False, figure_size=(6, 4)):
        fig = plt.figure(figsize=figure_size)
        if display_tasks:
            ax1 = fig.add_subplot(1, 2, 1, aspect=1)
            ax2 = fig.add_subplot(1, 2, 2, aspect=0.5)
        else:
            ax1 = fig.add_subplot(1, 1, 1, aspect=1)

        def plot_one_step(f):
            # clear pre step artists
            ax1.cla()
            if display_tasks: ax2.cla()
            # set lim
            ax1.set_xlim(-1, self.grid_size_x)
            ax1.set_ylim(-1, self.grid_size_y)
            # set grid
            for x in range(self.grid_size_x + 1):
                ax1.plot([x - 0.5, x - 0.5], [0 - 0.5, self.grid_size_y - 0.5], color="black")
            for y in range(self.grid_size_y + 1):
                ax1.plot([0 - 0.5, self.grid_size_x - 0.5], [y - 0.5, y - 0.5], color="black")
            # plot static obstacle
            for obstacle in self.static_obstacles:
                x = obstacle[0] - 0.5
                y = obstacle[1] - 0.5
                r = patches.Rectangle(xy=(x, y), width=1, height=1, color="black")
                ax1.add_patch(r)
            # plot static obstacle
            for endpoint in self.endpoints:
                x = endpoint[0] - 0.5
                y = endpoint[1] - 0.5
                r = patches.Rectangle(xy=(x, y), width=1, height=1, color="skyblue")
                ax1.add_patch(r)
            # plot agents
            for agent, pos in self.traject.items():
                if f < len(pos):
                    # plot agents
                    c = patches.Circle(xy=(pos[f][0], pos[f][1]), radius=0.3, color="blue", ec="k")
                    ax1.text(pos[f][0], pos[f][1], str(agent.id), va="center", ha="center", fontsize=8, color="white")
                    ax1.add_patch(c)
                    # when agent deliver
                    if self.state_traject[agent][f] == "delivering":
                        r = patches.Rectangle(xy=(pos[f][0] + 0.1, pos[f][1] + 0.1), width=0.25, height=0.3, ec='k',
                                              fc='orange')
                        ax1.add_patch(r)
                else:
                    c = patches.Circle(xy=(pos[-1][0], pos[-1][1]), radius=0.3, color="blue", ec="k")
                    ax1.text(pos[-1][0], pos[-1][1], str(agent.id), va="center", ha="center", fontsize=8, color="white")
                    ax1.add_patch(c)
            # plot task log
            timestep = max(0, f-1)//self.step_div
            label = ["stock\ntasks", "delivering\ntasks"]
            value = [self.task_assign_log[timestep], self.task_deliver_log[timestep]]
            y_lim_max = int(max(max(self.task_assign_log), max(self.task_deliver_log))*1.2)
            if display_tasks:
                ax2.set_ylabel("number of tasks")
                ax2.set_ylim(-1, y_lim_max)
                ax2.bar(label, value, color="blue", ec="k")

        interval_time = 1000 / self.step_div / self.speed
        anim = FuncAnimation(fig, plot_one_step, frames=self.traj_steps, interval=interval_time)
        if save:
            fail_path = './anim/' + name + '.mp4'
            anim.save(fail_path, writer="imagemagick")
        plt.show()


if __name__ == '__main__':
    from config_mapd import ConfigMAPD
    config_file = "./config/config_test.xlsx"
    config = ConfigMAPD(config_file)

    sim = Simulation(config, 100)

    # set log
    agent_1 = Agent(1)
    agent_2 = Agent(2)
    path_1 = np.array([[1, 3], [1, 4], [1, 5]])
    path_2 = np.array([[4, 2], [3, 2], [3, 3]])
    path_log = {agent_1: path_1, agent_2: path_2}
    task_assign_log = [1, 2, 3]
    task_deliver_log = [0, 0, 0]
    state1 = ['free', 'free', 'free']
    state2 = ['free', 'delivering', 'delivering']
    state_log = {agent_1: state1, agent_2: state2}

    sim.path_log = path_log
    sim.task_assign_log = task_assign_log
    sim.task_deliver_log = task_deliver_log
    sim.state_log = state_log

    visualizer = Visualizer(sim)
    visualizer.plot()
