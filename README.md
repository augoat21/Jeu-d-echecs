# Que fait mon projet ? 
Il met à disposition un jeu d'échecs éducatif permettant de s'entraîner/s'amuser. 
Il intègre le moteur de calcul stockfish qui permet de :
    - De jouer contre des adversaires avec plusieurs difficultés pour des niveaux d'utilisateurs variés.
    - De mettre à disposition de l'utilisateur des indices afin de comprendre les théories fondamentales des échecs.
    - Optimiser toutes les lignes de play possibles à jouer et expliquer pourquoi c'est un bon/mauvais coup.

# Comment marche le moteur d'échecs
Programmation d'un jeu d'échecs en deux parties :
   - 1) Utilisation du moteur de calcul stockfish pour avoir les meilleurs coups possibles sans les calculer sur la machine utilisée
   - 2) Effectuer les calculs minimax sur la machine utilisée à l'aide de propriétés mathématiques 


## Options mises en place (Touches)
-Possibilité de recommencer une partie pendant ta partie ou à la fin de ta partie (R)
-Annuler un coup afin de rectifier une erreur ou de chercher le coup optimal (U)
-Demander un indice sur la position actuelle te permettant de minimiser l'erreur (H)
-Changer de difficulté en fonction de ton niveau (change le niveau de l'ia en face) (←,→)
-Quitter l'application pygame (esc/échap)

## Structure du projet
main.py         # L'assemblage de tous les programmes python afin de faire fonctionner le jeu
config.py       # Met en place les dimensions de l'interface, les couleurs, l'aspect visuel mais aussi la connexion directe avec le moteur stockfish et les différents niveaux de jeu
plateau.py      # La logique du plateau, l'interface visuelle, placement des pièces mais aussi la logique du jeu
MoteurEchecs.py # Gère l'intégration de stockfish, les analyses de la position et tactique
explainer.py    # Il explique la logique du jeu donc dans notre cas le coup joué, la position et la tactique/stratégie
pieces.py       # Crée le rendu des pièces et les fonctions utilitaires de celles-ci
README.md

## Librairies utilisées et moteur 
Librairies
-pygame :  permet l'interface de jeu pour python
-chess : gère toute la logique des échecs 
-chess.engine : sous module de chess qui permet de communiquer avec stockfish 
-os : permet d'interagir avec le système de fichiers de mon ordinateur
-random : permet uniquement dans ce cas d'assurer un coup légal si stockfish plante

Moteur
Stockfish : Moteur d'échecs le plus puissant du monde qui permet de calculer jusqu'à 20 coups à l'avance pour prendre la meilleure décision
Minimax : fonction codée par moi qui permet de calculer 4/5 coups à l'avance (soit entre 1 et 50 millions de calculs effectués)


