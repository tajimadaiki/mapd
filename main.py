from config_mapd import ConfigMAPD
from simulation import Simulation
from visualizer import Visualizer


def main():
    max_timestep = 80
    config_file = "./config/map_KVC.xlsx"
    config = ConfigMAPD(config_file)
    sim = Simulation(config, max_timestep)
    sim.run()

    visualizer = Visualizer(sim, speed=1.5)
    visualizer.plot(save=False)


if __name__ == "__main__":
    main()
