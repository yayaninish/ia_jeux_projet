# robot_braitenberg_hateWall.py
from robot import *

nb_robots = 0

class Robot_player(Robot):
    team_name = "BraitenbergHateWall"
    robot_id = -1

    def __init__(self, x0, y0, theta0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x0, y0, theta0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Activation des murs (1 = proche, 0 = loin ou pas un mur)
        activation = [(1.0 - sensors[i]) * float(sensor_view[i] == 1) 
                      for i in range(8)]
        # Poids répulsifs pour s’éloigner des murs
        w = [ -0.5, -0.8, -0.2, -0.1, 0.0,  0.1,  0.2,  0.8]
        # Rotation = somme pondérée des activations
        rotation = sum(activation[i] * w[i] for i in range(8))
        # Translation = diminue si mur frontal
        front = (activation[0] + activation[1] + activation[7]) / 3.0
        translation = max(0.2, 1.0 - 0.8 * front)
        return translation, rotation, False
