from robot import * 
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):
    team_name = "RandomSearch"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0,
                 name="n/a", team="n/a",
                 evaluations=500, it_per_evaluation=400):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        # positions/orientation initiale
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        # paramètres courants et meilleur
        self.param = [random.randint(-1, 1) for _ in range(8)]
        self.best_param = []
        self.best_score = float('-inf')
        self.best_evaluation = None
        # score et compteurs
        self.current_score = 0
        self.iteration = 0       # itérations totales
        self.trial = 0           # stratégies testées
        # configuration
        self.evaluations = evaluations
        self.it_per_evaluation = it_per_evaluation
        # flag replay
        self.replay_started = False
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        # reset de position/orientation et remise à zéro du score
        super().reset()
        self.current_score = 0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        # --- Mode replay du meilleur comportement ---
        if self.trial >= self.evaluations:
            if not self.replay_started:
                print("\n=== Replaying best strategy ===")
                print(f"Found at strategy {self.trial}")
                print(f"BestScore: {self.best_score:.4f}")
                print("Parameters:", self.best_param)
                self.param = self.best_param.copy()
                self.current_score = 0
                self.replay_started = True
            # exécution normale du meilleur
            translation, rotation = self._compute_move(sensors)
            # recalcul du score
            self.current_score += abs(translation) * (1 - abs(rotation))
            self.iteration += 1
            # reset périodique
            if self.iteration % 1000 == 0:
                print("\n=== Replaying best strategy ===")
                print(f"Found at strategy {self.trial}")
                print(f"BestScore: {self.best_score:.4f}")
                print(f"Score: {self.current_score:.4f}")
                print("Parameters:", self.best_param)

                return 0, 0, True
            return translation, rotation, False

        # --- Phase d'optimisation ---
        # fin d'une évaluation ?
        if self.iteration > 0 and self.iteration % self.it_per_evaluation == 0:
            # vérification du meilleur
            if self.current_score > self.best_score:
                self.best_score = self.current_score
                self.best_param = self.param.copy()
                self.best_evaluation = self.trial
                print(f"New best strategy at eval {self.trial} with score {self.best_score:.4f}")
                print("Parameters:", self.best_param)
            # passe à la stratégie suivante
            self.trial += 1
            # tirage d'une nouvelle stratégie
            if self.trial < self.evaluations:
                self.param = [random.randint(-1, 1) for _ in range(8)]
                print(f"Testing strategy {self.trial}/{self.evaluations}")
            # reset pour la prochaine évaluation
            self.iteration += 1
            return 0, 0, True

        # --- Calcul du mouvement en cours d'évaluation ---
        translation, rotation = self._compute_move(sensors)
        self.current_score += abs(translation) * (1 - abs(rotation))
        self.iteration += 1
        return translation, rotation, False

    def _compute_move(self, sensors):
        # perceptron sans couche cachée
        t = math.tanh(
            self.param[0]
            + self.param[1] * sensors[sensor_front_left]
            + self.param[2] * sensors[sensor_front]
            + self.param[3] * sensors[sensor_front_right]
        )
        r = math.tanh(
            self.param[4]
            + self.param[5] * sensors[sensor_front_left]
            + self.param[6] * sensors[sensor_front]
            + self.param[7] * sensors[sensor_front_right]
        )
        return t, r
