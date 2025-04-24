from robot import *

nb_robots = 0
debug = True  # Active l'affichage des informations de débogage

class Robot_player(Robot):
    team_name = "HateBot"
    
    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.iteration = 0  # Compteur d'itérations pour le débogage
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # 1. Filtrage: ne considère que les capteurs détectant d'autres robots (type 2)
        robot_sensors = [sensors[i] if sensor_view[i] == 2 else 0 for i in range(8)]
        
        # 2. Conversion en activation (1.0 = robot très proche, 0.0 = pas de robot)
        activation = [1.0 - s if s > 0 else 0 for s in robot_sensors]
        
        # 3. Configuration des poids pour la répulsion (inversés par rapport à LoveBot)
        weights = [0.8, 0.6, 0.2, 0, 0, -0.2, -0.6, -0.8]  # Poids asymétriques
        
        # 4. Calcul de la rotation (somme pondérée des activations)
        rotation = sum([activation[i] * weights[i] for i in range(8)])
        
        # 5. Gestion de la translation:
        #    - Recule si robot très proche devant
        #    - Avance normalement sinon
        front_threat = (activation[sensor_front] + 
                      activation[sensor_front_left] * 0.3 + 
                      activation[sensor_front_right] * 0.3)
        
        if front_threat > 0.7:  # Danger immédiat devant
            translation = -0.5  # Recule
        elif front_threat > 0.3:  # Robot proche devant
            translation = 0.3  # Ralentit fortement
        else:
            translation = 1.0  # Avance normalement

        # 6. Affichage des informations de débogage
        if debug and self.iteration % 100 == 0:
            print(f"\nRobot {self.robot_id} (HateBot) - step {self.iteration}:")
            print("Raw sensors:", sensors)
            print("Robot sensors:", robot_sensors)
            print("Activation:", [round(a, 2) for a in activation])
            print("Weights:", weights)
            print(f"Front threat: {front_threat:.2f}")
            print(f"Final command: t={translation:.2f}, r={rotation:.2f}")

        self.iteration += 1
        return translation, rotation, False