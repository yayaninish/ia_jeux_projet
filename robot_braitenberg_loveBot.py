from robot import *

nb_robots = 0
debug = True  # Ajout du mode debug pour visualiser les calculs

class Robot_player(Robot):
    team_name = "LoveBot"
    
    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.iteration = 0  # Ajout d'un compteur d'itérations
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Seulement les capteurs détectant d'autres robots (type 2)
        robot_sensors = [sensors[i] if sensor_view[i] == 2 else 0 for i in range(8)]
        
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

        if debug and self.iteration % 100 == 0:
            print(f"\nRobot {self.robot_id} (step {self.iteration}):")
            print("Raw sensors:", sensors)
            print("Robot sensors:", robot_sensors)
            print("Activation:", activation)
            print("Weights:", weights)
            print(f"Front activation: {front_activation:.2f}")
            print(f"Result - translation: {translation:.2f}, rotation: {rotation:.2f}")

        self.iteration += 1
        return translation, rotation, False