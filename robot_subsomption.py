from robot import *

nb_robots = 0

class Robot_player(Robot):
    team_name = "Subsumption"
    robot_id = -1

    def __init__(self, x0, y0, theta0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots; nb_robots += 1
        super().__init__(x0, y0, theta0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # 1) Si robot ennemi détecté -> suivre (loveBot)
        rob = [1.0 - s if view==2 and sensor_team[i]!=self.team else 0.0
               for i,(s,view) in enumerate(zip(sensors, sensor_view))]
        if max(rob) > 0:
            weights = [-2.0, -1.0, -1.0, 0.0, 0.0, 1.0, 0.6, 1.0]
            rotation = sum(a*w for a,w in zip(rob, weights))
            front = (rob[sensor_front_left] + rob[sensor_front] + rob[sensor_front_right]) / 3.0
            translation = max(0.2, 1.0 - 0.8 * front)
            return translation, rotation, False

        # 2) Sinon si mur détecté -> éviter (hateWall)
        wall = [1.0 - s if view==1 else 0.0
                for s,view in zip(sensors, sensor_view)]
        if max(wall) > 0:
            # Poids répulsifs pour s’éloigner des murs
            w = [ -0.5, -0.8, -0.2, -0.1, 0.0,  0.1,  0.2,  0.8]
            # Rotation = somme pondérée des activations
            rotation = sum(wall[i] * w[i] for i in range(8))
            # Translation = diminue si mur frontal
            front = (wall[0] + wall[1] + wall[7]) / 3.0
            translation = max(0.2, 1.0 - 0.8 * front)
            return translation, rotation, False

        # 3) Sinon -> tout droit
        return 1.0, 0.0, False
