from robot import * 
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
    robot_id = -1
    iteration = 0

    param = []
    best_param = []
    best_score = -1
    best_evaluation = 0
    current_score = 0
    
    evaluations = 500  # nombre total de stratégies à tester
    it_per_evaluation = 400  # nombre d'itérations par stratégie
    trial = 0  # compteur de stratégies testées

    x_0 = 0
    y_0 = 0
    theta_0 = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=0, it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()
        self.current_score = 0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Toutes les X itérations: évaluer la stratégie et en essayer une nouvelle
        if self.iteration % self.it_per_evaluation == 0:
            if self.iteration > 0:
                # Fin d'une évaluation - calcul du score
                #self.current_score /= self.it_per_evaluation  # score moyen
                
                # Si c'est le meilleur score, on le sauvegarde
                if self.current_score > self.best_score:
                    self.best_score = self.current_score
                    self.best_param = self.param.copy()
                    self.best_evaluation = self.trial
                    print(f"New best strategy found at evaluation {self.trial} with score {self.best_score:.4f}")
                    print("\tparameters =", self.best_param)
                
            
            # Si on a testé toutes les stratégies, on passe en mode "meilleur comportement"
            if self.trial >= self.evaluations:
                if self.best_param:  # Si on a trouvé un bon comportement
                    print("\n=== Best strategy ===")
                    print(f"Found at evaluation {self.best_evaluation}")
                    print(f"Score: {self.best_score:.4f}")
                    print("Parameters:", self.best_param)
                    self.param = self.best_param.copy()
                    
                    # On rejoue le meilleur comportement toutes les 1000 itérations
                    if self.iteration % 1000 == 0:
                        return 0, 0, True  # reset
                    else:
                        translation, rotation = self.compute_movement(sensors)
                        return translation, rotation, False
                else:  # Au cas où aucune stratégie n'a été trouvée (ne devrait pas arriver)
                    self.param = [random.randint(-1, 1) for i in range(8)]
            
            # Génération d'une nouvelle stratégie aléatoire
            else:
                self.param = [random.randint(-1, 1) for i in range(8)]
                self.trial += 1
                print(f"Testing strategy {self.trial}/{self.evaluations}")
            
            self.iteration += 1
            return 0, 0, True  # ask for reset
        
        # Calcul du mouvement
        translation = math.tanh(self.param[0] + 
                       self.param[1] * sensors[sensor_front_left] + 
                       self.param[2] * sensors[sensor_front] + 
                       self.param[3] * sensors[sensor_front_right])
        
        rotation = math.tanh(self.param[4] + 
                     self.param[5] * sensors[sensor_front_left] + 
                     self.param[6] * sensors[sensor_front] + 
                     self.param[7] * sensors[sensor_front_right])
        # Calcul du score (vitesse_translation * (1 - abs(vitesse_rotation)))
        self.current_score += abs(translation * (1 - abs(rotation)))
        
        self.iteration += 1
        return translation, rotation, False
    