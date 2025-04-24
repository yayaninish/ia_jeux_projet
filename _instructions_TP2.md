# TP 2 - optimisation de comportements

## Exercice 1: recherche aléatoire 

Etudiez la fonction _step_ du fichier _robot_optimize.py_. 

Cette fonction montre comment faire une recherche aléatoire dans l'espace des paramètres d'un réseau de neurones artificiels simple (un Perceptron sans couche cachée utilisant une fonction tangente hyperbolique pour le calcul d'activation).

On considère que chaque paramètre peut prendre une valeur parmi trois: -1 (inhibition), +1 (excitation) ou 0 (pas de connexion).

Calculez le score d'un individu pour maximiser à chaque pas de temps la vitesse de translation et minimiser la vitesse de rotation, c'est à dire:
* score = somme_sur_toutes_les_iterations ( vitesse_de_translation * ( 1 - abs(vitesse_de_rotation) ) ) 

Créez le fichier _robot_randomsearch.py_ (en copiant _robot_optimize.py_), puis modifiez le comme suit:
* en utilisant les variables existantes, fixer le nombre de comportements à générer aléatoirement qui devront être évalués.
* à chaque fois qu'un comportement est meilleur que les précédents, sauvegardez-le (score, valeur des paramètres et le numéro d'évaluation ou il a été trouvé).
* fixer le nombre de stratégies testées à 500 avant d'arrêter (i.e. 500 comportements différents seront testés, chacun pendant 400 itérations).

Après avoir épuisé le budget d'évaluations, rejouez le meilleur comportement trouvé pendant _1000_ itérations, puis recommencez (i.e. le meilleur comportement est montré à l'infini, il est remis à sa position initiale toutes les 1000 itérations).

Remarques:
* la variable _display_mode_ permet de régler la vitesse de la simulation au démarrage. Pratique pour faire une recherche rapide (valeur 1, voire 2).
* n'oubliez pas de sauvegarder votre meilleur individu quelque part (p.ex. en affichant ses paramètres dans le terminal à la fin de la recherche).

## Exercice 2: effet des conditions initiales

Un inconvénient du programme précédent vient du fait que la condition initiale (position et orientation initiale) est toujours la même. Cela ne permet pas de garantir que le comportement obtenu sera efficace dans une autre situation. 

En partant du programme précédent (créez un fichier _randomsearch2.py_), modifier le code afin que chaque comportement soit évalué _3_ fois, en tirant aléatoirement l'orientation initiale à chaque fois. Le score d'un comportement sera la somme de ces 3 évaluations.

Remarque: 
* vous pouvez aussi, si vous le souhaitez, faire varier la position de départ (éviter de positionner votre robot dans un mur).

## Exercice 3: algorithme génétique

Créez le fichier _genetic_algorithms.py_ (en copiant le précédent) et implémentez un algorithme génétique à la place de la recherche aléatoire, comme vu en cours:
* opérateur de sélection: _( mu=1 + lambda=1 )_
* opérateur de mutation: sélection d'un paramètre au hasard, et remplacement de sa valeur au hasard sans retirage (c'est à dire que la nouvelle valeur est forcément différente de la précédente)

A chaque génération un seul enfant est donc créé, à partir du parent et en modifiant la valeur d'un seul paramètre. Si l'enfant est meilleur que le parent, alors il remplace le parent. Sinon, le parent est conservé (et l'enfant effacé).

## Exercice 4: affichage et comparaison des résultats 

Pour un nombre d'_itérations_ identique, comparez les résultats obtenus par la recherche aléatoire et la recherche par algorithme génétique. Pour chaque méthode, vous tracerez un graphe compilant les résultats de 10 essais indépendants. Pour cela, modifiez les codes que vous venez d'écrire pour les questions 2 et 3 afin de sauvegarder dans un fichier les informations suivantes pour chaque évaluation:

* numéro de l'évaluation à partir duquel le comportement actuel est testé 
* score du comportement actuel
* meilleur score obtenu depuis le début

Cela donnera par exemple:
* 0, 225.3660952, 225.3660952
* 1, 199.618627164, 225.3660952
* 2, 80.8005718674, 225.3660952
* 3, 642.2593266, 642.2593266 
* _etc._

Vous devez maintenant générer des graphes de vos résultats:
* tracer le résultat d'une recherche (axe X: evaluations, axe Y: score), en traçant pour chaque itération le meilleur individu trouvé jusqu'ici. (cf. premier exemple du fichier _aide.txt_)
* tracer la performance moyenne d'une recherche aléatoire en compilant 10 essais indépendants. (cf. second exemple du fichier _aide.txt_)
Pour cela, vous pouvez utiliser un tableur (p.ex. Libroffice) ou un script Python (ex.: [multiplot](https://github.com/nekonaute/SU-LU3IN025-robots/tree/main/multiplotCSV)).

Remarques:
* Plutôt que de sauvegarder directement les informations demandées dans un fichier, vous pouvez aussi simplement les afficher dans le terminal, et les copier manuellement dans un fichier.
* en plus des infos demandées, vous pouvez ajouter sur chaque ligne les valeurs des meilleurs paramètres trouvés jusqu'ici. Cela permet ensuite de pouvoir les rejouer si besoin.

## Quelques idées pour le projet

* implémentez une fonction score calculant la couverture de l'environnement, par exemple en le découpant en cases (cf. projet)
* implémentez un opérateur de sélection (mu=5,lambda=20)
* modifiez l'opérateur de mutation afin d'explorer un taux de mutation plus élevé

L'algorithme génétique peut vous permettre de trouver une solution exploitable pour votre projet, à condition de bien définir la fonction score (pour guider la recherche) et les conditions d'expérience (pour garantir l'aspect générique de la solution).
