# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : LABIADH Yanis 21202800
#  Prénom Nom No_étudiant/e : SI MOHAMMED Yaniss
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import *
import math
import random

# Best GA parameters obtained précédemment (exemple)
GA_PARAMS = [-1, -1, -1, -1, -1, 1, -1, 1]

nb_robots = 0

class Robot_player(Robot):
    team_name = "YY"

    def __init__(self, x_0, y_0, theta_0,
                 name="n/a", team="A"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        # Mémoire unique: 0=GA roam, 1=repulse robot, 2=avoid wall
        self.memory = 0
        # paramètres de perceptron GA pour le comportement par défaut
        self.ga_params = GA_PARAMS.copy()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # --- 1. Priorité haute: répulsion vis-à-vis des robots adverses ---
        # capteurs détectant un robot ennemi
        rob_sens = [sensors[i] if sensor_view[i] == 2 and sensor_team[i] != self.team else 0
                    for i in range(len(sensors))]
        if max(rob_sens) > 0.0:
            # activation (1=proche)
            activation = [1.0 - s for s in rob_sens]
            # poids braitenberg pour répulsion
            weights = [0.8, 0.6, 0.2, 0.0, 0.0, -0.2, -0.6, -0.8]
            rotation = sum(a * w for a, w in zip(activation, weights))
            # translation: recule si menace frontale
            front_threat = (activation[sensor_front] +
                            activation[sensor_front_left] * 0.3 +
                            activation[sensor_front_right] * 0.3)
            translation = max(0.0, 1.0 - front_threat)
            self.memory = 1
            return translation, rotation, False

        # --- 2. Moyenne priorité: éviter les murs ---
        wall_sens = [sensors[i] if sensor_view[i] == 1 else 0
                     for i in range(len(sensors))]
        if max(wall_sens) > 0.0:
            activation_wall = [1.0 - s for s in wall_sens]
            # poids pour éviter les murs
            weights_w = [0.0, -0.8, -0.2, -0.1, 0.0, 0.1, 0.2, 0.8]
            rotation = sum(a * w for a, w in zip(activation_wall, weights_w))
            # translation: ralentit si obstacle devant
            front_act = (activation_wall[sensor_front] +
                         activation_wall[sensor_front_left] +
                         activation_wall[sensor_front_right]) / 3.0
            translation = max(0.2, 1.0 - 0.8 * front_act)
            self.memory = 2
            return translation, rotation, False

        # --- 3. Comportement par défaut: GA-based roam ---
        # perceptron sans couche cachée, tanh activation
        t = math.tanh(
            self.ga_params[0]
            + self.ga_params[1] * sensors[sensor_front_left]
            + self.ga_params[2] * sensors[sensor_front]
            + self.ga_params[3] * sensors[sensor_front_right]
        )
        r = math.tanh(
            self.ga_params[4]
            + self.ga_params[5] * sensors[sensor_front_left]
            + self.ga_params[6] * sensors[sensor_front]
            + self.ga_params[7] * sensors[sensor_front_right]
        )
        self.memory = 0
        return t, r, False
