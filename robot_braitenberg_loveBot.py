from robot import *

nb_robots = 0
debug = False

class Robot_player(Robot):
    team_name = "BraitenbergLoveBot"
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
        # Rotation : poids attractifs
        weights = [-2.0, -1.0, -1.0, 0.0, 0.0, 1.0, 0.6, 1.0]
        rotation = sum(a*w for a,w in zip(activation, weights))
        # Translation : ralentit si robot devant
        front_act = (activation[sensor_front_left]
                     + activation[sensor_front]
                     + activation[sensor_front_right]) / 3.0
        translation = max(0.2, 1.0 - 0.8 * front_act)

        if debug and self.iteration % 100 == 0:
            print(f"[LoveBot] iter={self.iteration}, trans={translation:.2f}, rot={rotation:.2f}")

        self.iteration += 1
        return translation, rotation, False
