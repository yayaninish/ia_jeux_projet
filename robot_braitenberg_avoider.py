from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "BraitenbergAvoider"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range(8):
            view = sensor_view[i]
            sensor_to_wall.append(sensors[i] * (float(view == 1)) + 1.0 * float(view != 1) )
            sensor_to_robot.append(sensors[i] * (float(view == 2)) + 1.0 * float(view != 2) )

        # On inverse les valeurs pour avoir une "activation" (1 = danger, 0 = libre)
        activation_wall = [1.0 - s for s in sensor_to_wall]
        activation_robot = [1.0 - s for s in sensor_to_robot]

        # Fusion des activations pour éviter à la fois murs et robots
        activation_total = [max(a, b) for a, b in zip(activation_wall, activation_robot)]

        # Pondération des directions pour tourner loin des obstacles
        w = [-1, -0.5, 0, 0, -1, 0, 0, 0.5]  # Poids de rotation (ex: gauche négatif, droite positif)

        # Rotation : somme pondérée des activations
        rotation = sum([activation_total[i] * w[i] for i in range(8)])

        # Translation : avance plus quand peu d'obstacles devant
        front = (activation_total[0] + activation_total[7] + activation_total[1]) / 3
        translation = 1.0 - front  # diminue si obstacle en face

        if debug and self.iteration % 100 == 0:
            print("Robot", self.robot_id, "(team " + str(self.team_name) + ")", "at step", self.iteration, ":")
            print("\tsensors =", sensors)
            print("\tsensor_view =", sensor_view)
            print("\tactivation_wall =", activation_wall)
            print("\tactivation_robot =", activation_robot)
            print("\tactivation_total =", activation_total)

        self.iteration += 1        
        return translation, rotation, False
