from robot import *

nb_robots = 0

class Robot_player(Robot):
    team_name = "Subsumption"
    
    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Behavior 1: Go straight (lowest priority)
        translation = 1.0
        rotation = 0.0
        
        # Behavior 2: Avoid walls (medium priority)
        wall_sensors = [sensors[i] if sensor_view[i] == 1 else 0 for i in range(8)]
        if max(wall_sensors) > 0.3:  # If wall detected
            sensor_to_wall = []
            for i in range(8):
                view = sensor_view[i]
                # Plus la valeur est petite, plus le mur est proche
                sensor_to_wall.append(sensors[i] if view == 1 else 1.0)

            # Activation: plus la valeur est grande, plus le mur est proche (1.0 = mur en contact)
            activation_wall = [1.0 - s for s in sensor_to_wall]

            # Pondération des directions pour éloigner des murs
            # Les poids sont inversés par rapport à LoveWall
            w = [0, -0.8, -0.2, -0.1, 0, 0.1, 0.2, 0.8]

            # Rotation : somme pondérée des activations
            front = float(sensor_view[sensor_front] < 0.3)
            frontleftright = float(sensor_view[sensor_front_right] < sensor_view[sensor_front_left]) #1 si obstacle droit plus proche que gauche
            rotation = sum([activation_wall[i] * w[i] for i in range(8)])

            # Translation : ralentit quand mur détecté devant
            # On utilise une moyenne des capteurs avant (0,7,1)
            sidewall = float(activation_wall[sensor_left] > 0.6 or activation_wall[sensor_right] > 0.6)
            front_activation = (activation_wall[0] + activation_wall[7] + activation_wall[1]) / 3
            translation = (1.0 - 0.8 * front_activation) * (1-sidewall) + (0.2) * sidewall  # minimum 0.2, maximum 1.0
        
        # Behavior 3: Follow robots (highest priority)
        robot_sensors = [sensors[i] if sensor_view[i] == 2 else 0 for i in range(8)]
        if max(robot_sensors) > 0.3:  # If robot detected
                  
            # Activation: plus la valeur est grande, plus le robot est proche
            activation = [1.0 - s if s > 0 else 0 for s in robot_sensors]
            
            # Configuration des poids pour l'attraction
            weights = [-2.0, -1.0, -1.0, 0, 0, 1.0, 0.6, 1.0]  # Poids asymétriques pour un comportement plus fluide


            
            # Calcul de la rotation (somme pondérée)
            rotation = (sum([activation[i] * weights[i] for i in range(8)]))
            
            # Gestion de la translation:
            # - Avance normalement si pas de robot devant
            # - Ralentit proportionnellement à la proximité des robots devant
            front_activation = (activation[sensor_front] + 
                            activation[sensor_front_left] * 0.5 + 
                            activation[sensor_front_right] * 0.5) / 2

            translation = (max(0.2, 1.0 - front_activation * 0.8))  # Limite à 0.2 pour garder une vitesse minimale
            
        
        return translation, rotation, False