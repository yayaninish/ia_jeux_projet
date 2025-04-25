from robot import *
import math
import random

# Algorithme génétique (mu=1 + lambda=1)
nb_robots = 0
debug = False

class Robot_player(Robot):
    team_name = "GeneticAlgorithm"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=500, it_per_evaluation=400):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        # positions/orientations initiales
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        # paramètres du parent et meilleur
        self.param = [random.randint(-1, 1) for _ in range(8)]
        self.parent_param = self.param.copy()
        self.best_param = self.param.copy()
        self.best_score = float('-inf')
        # budget et durée d'évaluation
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        # compteurs
        self.generation = 0  # enfants générés
        self.iteration = 0   # itérations simulées
        self.current_score = 0
        # flag pour replay
        self.replay_started = False
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()
        # remets le score courant à zéro
        self.current_score = 0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # --- MODE REPLAY DU MEILLEUR ---
        if self.generation >= self.evaluations:
            if not self.replay_started:
                print("\n=== Replaying best strategy ===")
                print(f"Found at strategy {self.generation}")
                print(f"BestScore: {self.best_score:.4f}")
                print("Parameters:", self.best_param)
                print("BestTheta:", self.best_theta)
                print("Theta:", self.theta0)
                self.param = self.best_param.copy()
                self.current_score = 0
                self.replay_started = True
            # exécution normale du meilleur
            translation = math.tanh(
                self.param[0] + self.param[1] * sensors[sensor_front_left] +
                self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right]
            )
            rotation = math.tanh(
                self.param[4] + self.param[5] * sensors[sensor_front_left] +
                self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right]
            )
            # accumulation du score en replay
            self.current_score += abs(translation) * (1 - abs(rotation))
            self.iteration += 1
            # reset périodique tous les 1000 pas
            if self.iteration % 1000 == 0:
                print("\n=== Replaying best strategy ===")
                print(f"Found at strategy {self.generation}")
                print(f"BestScore: {self.best_score:.4f}")
                print(f"Score: {self.current_score:.4f}")
                print("Parameters:", self.best_param)
                print("BestTheta:", self.best_theta)
                print("Theta:", self.theta0)
                return 0, 0, True
            return translation, rotation, False

        # --- PHASE D'OPTIMISATION ---
        # fin d'une évaluation courante ? (sauf à l'itération 0)
        if self.iteration > 0 and self.iteration % self.it_per_evaluation == 0:
            # sélection (mu+lambda)
            if self.current_score > self.best_score:
                self.best_score = self.current_score
                self.parent_param = self.param.copy()
                self.best_param = self.param.copy()
                self.best_theta = self.theta0
                print(f"Gen {self.generation}: nouveau parent score {self.best_score:.4f} --------------------------------------")
                print("Parameters:", self.best_param)
                print("Theta:", self.best_theta)
            
            with open(f"genetic_run{1}.csv", "a") as f:
                    f.write(f"{self.generation},{self.current_score},{self.best_score}\n")
            # next generation
            self.generation += 1
            # mutation pour créer l'enfant
            if self.generation < self.evaluations:
                self.param = self.parent_param.copy()
                idx = random.randrange(8)
                choices = [-1, 0, 1]
                choices.remove(self.param[idx])
                self.param[idx] = random.choice(choices)
                print(f"Création gen {self.generation}: mutation idx {idx}")
                print("Parameters Parent:", self.parent_param)
                print("Parameters Enfant:", self.param)
                print("Theta:", self.theta0)
                self.current_score = 0
            # ask for reset pour le prochain test
            self.iteration += 1
            return 0, 0, True

        # calcul du mouvement
        translation = math.tanh(
            self.param[0] + self.param[1] * sensors[sensor_front_left] +
            self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right]
        )
        rotation = math.tanh(
            self.param[4] + self.param[5] * sensors[sensor_front_left] +
            self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right]
        )
        # accumulation du score
        self.current_score += abs(translation) * (1 - abs(rotation))
        self.iteration += 1
        return translation, rotation, False
