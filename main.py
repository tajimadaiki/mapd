from config_mapd import ConfigMAPD
from simulation import Simulation
from visualizer import Visualizer


def main():
    max_timestep = 600
    config_file = "./config/map_KVC.xlsx"
    config = ConfigMAPD(config_file)
    sim = Simulation(config, max_timestep)
    sim.run()

    visualizer = Visualizer(sim, speed=2.5)
    visualizer.plot(save=False, name='task5_agent5_15m_1msec', figure_size=(6, 12))


if __name__ == "__main__":
    main()
