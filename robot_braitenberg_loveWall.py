from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "BraitenbergLoveWall"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        for i in range(8):
            view = sensor_view[i]
            # Plus la valeur est petite, plus le mur est proche
            sensor_to_wall.append(sensors[i] if view == 1 else 1.0)

        # Activation: plus la valeur est grande, plus le mur est proche (1.0 = mur en contact)
        activation_wall = [1.0 - s for s in sensor_to_wall]

        # Pondération des directions pour attirer vers les murs
        # Les poids positifs attirent vers les murs de ce côté
        w = [-0.8, -0.4, 0, 0, 0.4, 0.6, 0.6, 0.8]
        

        # Rotation : somme pondérée des activations
        near_right = float(activation_wall[sensor_right] < 0.3 and activation_wall[sensor_front_right] > 0.5 or activation_wall[sensor_rear_right] < 0.6)
        near_left = float(activation_wall[sensor_left] < 0.3 and activation_wall[sensor_front_left] > 0.5 or activation_wall[sensor_rear_left] < 0.6)
        no_r_l = float(near_left == 0 and near_right == 0 )
        front = float(sensors[sensor_front] < 0.5)
        frontleftright = float(sensors[sensor_front_right] < sensors[sensor_front_left]) #1 si obstacle droit plus proche que gauche
        rotation = ((near_right)* (0.5) + (near_left) * (-0.5) + (no_r_l) * sum([activation_wall[i] * w[i] for i in range(8)])) * (1-front) + ((frontleftright * (0.8) + (1 - frontleftright) * (-0.8))) * front

        # Translation : avance plus quand mur détecté devant
        # On utilise une moyenne des capteurs avant (0,7,1)
        sidewall = float(activation_wall[2] > 0.5 or activation_wall[6] > 0.5)
        front_activation = (activation_wall[0] + activation_wall[7] + activation_wall[1]) / 3
        translation = (0.4 + 0.6 * front_activation) * (1-sidewall) + (0.9) * sidewall  # minimum 0.2, maximum 1.0

        if debug and self.iteration % 100 == 0:
            print("Robot", self.robot_id, "(team " + str(self.team_name) + ")", "at step", self.iteration, ":")
            print("\tsensors =", sensors)
            print("\tsensor_view =", sensor_view)
            print("\tsensor_to_wall =", sensor_to_wall)
            print("\tactivation_wall =", activation_wall)
            print("\trotation weights =", w)
            print("\tresulting rotation =", rotation)
            print("\tresulting translation =", translation)

        self.iteration += 1        
        return translation, rotation, False