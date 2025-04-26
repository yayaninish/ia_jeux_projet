from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):
    team_name = "BraitenbergHateBot"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        self.iteration = 0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Filtrer uniquement capteurs détectant des robots
        robot_sensors = [sensors[i] if sensor_view[i] == 2 else 1.0 for i in range(8)]
        # Activation (1=fortement proche, 0=pas de robot)
        activation = [1.0 - s for s in robot_sensors]

        # Poids pour répulsion (Braitenberg type)
        weights = [0.8, 0.6, 0.2, 0.0, 0.0, -0.2, -0.6, -0.8]

        # Calcul rotation : somme pondérée des activations
        rotation = sum(a * w for a, w in zip(activation, weights))

        # Translation : moins rapide quand robot proche devant
        # moyenne des capteurs avant (0: front, 1: front-left, 7: front-right)
        front_activation = (activation[sensor_front] + activation[sensor_front_left] + activation[sensor_front_right]) / 3.0
        translation = max(0.0, 1.0 - front_activation)

        if debug and self.iteration % 100 == 0:
            print("Robot", self.robot_id, "(team " + str(self.team_name) + ")", "at step", self.iteration, ":")
            print("\tsensors =", sensors)
            print("\tsensor_view =", sensor_view)
            print("\tresulting rotation =", rotation)
            print("\tresulting translation =", translation)

        self.iteration += 1
        return translation, rotation, False
