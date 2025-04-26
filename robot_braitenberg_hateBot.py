from robot import *

nb_robots = 0
debug = False

class Robot_player(Robot):
    team_name = "BraitenbergHateBot"
    robot_id = -1

    def __init__(self, x0, y0, theta0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots; nb_robots += 1
        super().__init__(x0, y0, theta0, name=name, team=team)
        self.iteration = 0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Activation robots uniquement (ignore murs)
        activation = [
            1.0 - s if view == 2 else 0.0
            for s, view in zip(sensors, sensor_view)
        ]
        # Rotation : poids répulsifs
        weights = [0.8, 0.6, 0.2, 0.0, 0.0, -0.2, -0.6, -0.8]
        rotation = sum(a*w for a,w in zip(activation, weights))
        # Translation : ralentit si menace frontale
        front_act = (activation[sensor_front_left]
                     + activation[sensor_front]
                     + activation[sensor_front_right]) / 3.0
        translation = max(0.0, 1.0 - front_act)

        if debug and self.iteration % 100 == 0:
            print(f"[HateBot] iter={self.iteration}, trans={translation:.2f}, rot={rotation:.2f}")

        self.iteration += 1
        return translation, rotation, False
