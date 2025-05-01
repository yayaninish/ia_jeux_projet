from robot import *
import math

nb_robots = 0

class Robot_player(Robot):
    team_name = "BraitenbergLoveWall"
    robot_id = -1
    memory = 0  # compteur pour détecter l'état de "bloqué"

    def __init__(self, x0, y0, theta0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x0, y0, theta0, name=name, team=team)
        self.memory = 0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Vecteur distance au mur (1.0 si pas un mur)
        sensor_to_wall = [sensors[i] if sensor_view[i] == 1 else 1.0 for i in range(8)]

        # Seuils et indicateurs
        WALL_TH = 0.65
        STUCK1 = 30
        STUCK2 = 60
        blocked_front = sensors[sensor_front] < WALL_TH
        blocked_fl = sensors[sensor_front_left] < WALL_TH
        blocked_fr = sensors[sensor_front_right] < WALL_TH
        stuck = blocked_front and (blocked_fl or blocked_fr)

        # Mise à jour du compteur de blocage
        if stuck:
            self.memory += 1
        else:
            self.memory = 0

        # 1) Bloqué: reculer et tourner
        if self.memory > STUCK1:
            trans = -0.05
            rot = 0.4 if self.memory <= STUCK2 else 0.1
            return trans, rot, False

        # 2) Coin concave: manœuvre locale
        if blocked_front and (blocked_fl or blocked_fr):
            trans = sensors[sensor_front] * 0.3
            rot = (0.6 * sensors[sensor_front_left]
                   - 0.6 * sensors[sensor_front_right]
                   + 0.6 * sensors[sensor_left]
                   - 0.6 * sensors[sensor_right])
            return trans, rot, False

        # 3) Comportement Braitenberg: attirer vers les murs
        activation_wall = [1.0 - s for s in sensor_to_wall]
        # Poids attirants vers le mur
        weights = [-0.8, -0.4, 0.0, 0.0, 0.4, 0.6, 0.6, 0.8]
        rotation = sum(a * w for a, w in zip(activation_wall, weights))
        front = (activation_wall[sensor_front_left]
                 + activation_wall[sensor_front]
                 + activation_wall[sensor_front_right]) / 3.0
        translation = 0.4 + 0.6 * front
        return translation, rotation, False
