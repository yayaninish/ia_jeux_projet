from robot import *
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch2"
    robot_id = -1
    
    # Variables pour la gestion des évaluations
    global_iteration = 0      # Compte toutes les itérations
    strategy_iteration = 0    # Compte les itérations dans l'évaluation actuelle
    current_strategy = 0      # Numéro de la stratégie en cours
    current_eval = 0          # Numéro de l'évaluation en cours (0-2)
    
    # Paramètres et scores
    param = []
    best_param = []
    best_score = -1
    current_score = 0
    strategy_scores = [0, 0, 0]  # Scores des 3 évaluations
    
    # Configuration
    evaluations = 500         # Nombre total de stratégies à tester
    it_per_evaluation = 400   # Itérations par évaluation
    evaluations_per_strategy = 3  # Nombre d'évaluations par stratégie

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=0, it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for _ in range(8)]
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        """Réinitialise le robot avec une orientation aléatoire"""
        super().reset()
        # Nouvelle orientation aléatoire pour chaque évaluation
        self.theta0 = self.theta = random.uniform(0, 360)
        self.current_score = 0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # Vérifie si on doit terminer l'évaluation en cours
        if self.strategy_iteration >= self.it_per_evaluation:
            # Enregistre le score de l'évaluation
            self.strategy_scores[self.current_eval] = self.current_score
            self.current_eval += 1
            
            # Si on a fait les 3 évaluations, on passe à la stratégie suivante
            if self.current_eval >= self.evaluations_per_strategy:
                # Calcule le score total de la stratégie
                total_score = sum(self.strategy_scores)
                
                # Vérifie si c'est la meilleure stratégie
                if total_score > self.best_score:
                    self.best_score = total_score
                    self.best_param = self.param.copy()
                    print(f"New best strategy {self.current_strategy} with score {self.best_score:.4f}")
                    print("\tparameters =", self.best_param)
                
                # Passe à la stratégie suivante ou au mode best strategy
                self.current_strategy += 1
                if self.current_strategy >= self.evaluations:
                    print("\n=== Best strategy ===")
                    print(f"Score: {self.best_score:.4f}")
                    print("Parameters:", self.best_param)
                    self.param = self.best_param.copy()
                    # Reset périodique pour le meilleur comportement
                    if self.global_iteration % 1000 == 0:
                        return 0, 0, True
                    else:
                        translation, rotation = self.compute_movement(sensors)
                        return translation, rotation, False
                else:
                    # Nouvelle stratégie aléatoire
                    self.param = [random.randint(-1, 1) for _ in range(8)]
                    print(f"Testing strategy {self.current_strategy}/{self.evaluations}")
                
                self.current_eval = 0
                self.strategy_scores = [0, 0, 0]
            
            # Réinitialise pour la prochaine évaluation
            self.strategy_iteration = 0
            return 0, 0, True  # Demande un reset
        
        # Calcul du mouvement et du score
        translation, rotation = self.compute_movement(sensors)
        self.current_score += translation * (1 - abs(rotation))
        
        self.strategy_iteration += 1
        self.global_iteration += 1
        return translation, rotation, False
    
    def compute_movement(self, sensors):
        """Calcule le mouvement selon les paramètres actuels"""
        translation = math.tanh(
            self.param[0] + 
            self.param[1] * sensors[sensor_front_left] + 
            self.param[2] * sensors[sensor_front] + 
            self.param[3] * sensors[sensor_front_right]
        )
        
        rotation = math.tanh(
            self.param[4] + 
            self.param[5] * sensors[sensor_front_left] + 
            self.param[6] * sensors[sensor_front] + 
            self.param[7] * sensors[sensor_front_right]
        )
        
        return translation, rotation