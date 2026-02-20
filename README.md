## WARNING !
- Download Stockfish from https://stockfishchess.org/download/
- Then update CHEMIN_STOCKFISH variable in config.py with your own Stockfish file path.

# Que fait mon projet ? 
Il met à disposition un jeu d'échecs éducatif permettant de s'entraîner/s'amuser. 
Il intègre le moteur de calcul stockfish qui permet de :
  - De jouer contre des adversaires avec plusieurs difficultés pour des niveaux d'utilisateurs variés.
  - De mettre à disposition de l'utilisateur des indices afin de comprendre les théories fondamentales des échecs.
  - Optimiser toutes les lignes de play possibles à jouer et expliquer pourquoi c'est un bon/mauvais coup.

# Comment marche le moteur d'échecs
Programmation d'un jeu d'échecs en deux parties :
   - Utilisation du moteur de calcul stockfish pour avoir les meilleurs coups possibles sans les calculer sur la machine utilisée
   - Effectuer les calculs minimax sur la machine utilisée à l'aide de propriétés mathématiques 


## Options mises en place (Touches)
- Possibilité de recommencer une partie pendant ta partie ou à la fin de ta partie (R)
- Annuler un coup afin de rectifier une erreur ou de chercher le coup optimal (U)
- Demander un indice sur la position actuelle te permettant de minimiser l'erreur (H)
- Changer de difficulté en fonction de ton niveau (change le niveau de l'ia en face) (←,→)
- Quitter l'application pygame (esc/échap)

## Structure du projet
- main.py          L'assemblage de tous les programmes python afin de faire fonctionner le jeu
- config.py        Met en place les dimensions de l'interface, les couleurs, l'aspect visuel mais aussi la connexion avec le moteur stockfish et les différents niveaux de jeu
- plateau.py       La logique du plateau, l'interface visuelle, placement des pièces mais aussi la logique du jeu
- MoteurEchecs.py  Gère l'intégration de stockfish, les analyses de la position et tactique
- explainer.py     Il explique la logique du jeu donc dans notre cas le coup joué, la position et la tactique/stratégie
- pieces.py        Crée le rendu des pièces et les fonctions utilitaires de celles-ci

## Librairies utilisées et moteur 
Librairies
- pygame :  permet l'interface de jeu pour python
- chess : gère toute la logique des échecs 
- chess.engine : sous module de chess qui permet de communiquer avec stockfish 
- os : permet d'interagir avec le système de fichiers de mon ordinateur
- random : permet uniquement dans ce cas d'assurer un coup légal si stockfish plante

Moteur
- Stockfish : Moteur d'échecs le plus puissant du monde qui permet de calculer jusqu'à 20 coups à l'avance pour prendre la meilleure décision
- Minimax : fonction codée par moi qui permet de calculer 4/5 coups à l'avance (soit entre 1 et 50 millions de calculs effectués) il est bien evidemment possible de faire plus de coup mais cela peut prendre beaucoup de temps

## Comment j'ai coder mon minimax alpha-beta ?
J'ai en premiers temps reflechie à un comptage de point minimaliste (comparé à Stockfish) qui permet d'evaluer chaque coup en fonction de 2 parametres.
- Le premier critère est la valeur des pièces. Chaque pièce a une valeur en fonction de son importance (le nombre de cases qu'elle peut couvrir, sauf le roi qui vaut l'infini).
- Le deuxième critère est le placement de la pièce en fonction du moment de la partie. En effet, une même pièce n'a pas la même valeur selon l'endroit où elle se trouve sur l'échiquier. Un cavalier placé au centre, par exemple, contrôle jusqu'à 8 cases, tandis qu'un cavalier coincé dans un coin n'en contrôle que 2. Il est donc bien moins utile. De même, un pion vaut davantage en fin de partie lorsqu'il est proche de la promotion, qu'en début de partie où il n'est qu'un simple bloqueur.

Pour cela j'ai effectuer 3*6 matrices. 3 représente le nombre de phase de la partie (début/milieu/fin) et 6 le nomnre de piece(Tour, Fou, Cavalier, Reine, Roi et pion).
Cela permet donc d'evaluer en fonction d'une piece donnée, du moment de la partie et de sa case, une valeur de la piece. Exemple un pion proche de la promotion peut valoir plus qu'une reine clouer.

Maintenant je vais expliquer mon système phasique de la partie très simplement.
- Première phase, l'échiquier possède plus de 28 pièces (vivantes) alors on est encore dans la phase de début dite ouverture.
- Deuxième phase, l'échiquier possède plus de 14 pièces (vivantes) mais moins de 28 alors on est dans le milieu de partie.
- Dernière phase, l'échiquier possède moins de 14 pièces (vivantes) alors on est dans la fin de partie.
Il aurait été aussi possible de compter en centipions au lieu du nombre de pièces, ce qui est moins cohérent dans mon cas, mais je préfère être le plus simple possible pour les gens qui ne comprennent pas trop le jeu.

Enfin le plus important la fonction en elle meme.
- Après avoir regarder plusieurs vidéos pour comprendre le concept mathématiques du minimax j'ai décider de coder la fonction meme si celle ci était souvent representé dans les vidéos.
- Pour les explications, je vous donne le lien de la vidéo qui m'a permis de mieux comprendre. 
- Link : https://youtu.be/l-hh51ncgDI?si=IizlpFgzucJQLukf 
Si vous ne voulez pas regarder j'explique la fonction ici :
- L'algorithme met en place deux agents dans notre cas les noirs et les blancs. La fonction explore récursivement l'arbre de toutes les parties possibles jusqu'à une certaine profondeur. Le joueur "Blanc" cherche à maximiser son score, tandis que "Noir" (l'adversaire) cherche à le minimiser. À chaque nœud, on alterne entre choisir le meilleur coup (max) et le pire pour nous (min).Quand on atteint la profondeur limite, une fonction d'évaluation attribue un score à la position, et ces scores remontent dans l'arbre pour déterminer le meilleur coup à jouer.

## Commentaires
J'ai pris l'habitude de commenter un maximum mon code pour qu'il soit lisible et compréhensible par n'importe qui, même quelqu'un qui découvre le projet. C'est aussi une bonne pratique que j'ai apprise en regardant des projets open source sur GitHub, où le code est toujours bien documenté pour faciliter la collaboration.
Pour certaines parties comme l'interface Pygame que je ne connaissais pas bien, je me suis aidé de la documentation, de tutoriels et aussi d'outils d'IA pour comprendre comment fonctionnent certaines fonctions.Les commentaires me servaient justement à mémoriser certaines fonctions quand je relierais mon code plus tard.

## English Version

# What does my project do? 
It provides an educational chess game for training and having fun. 
It integrates the Stockfish calculation engine which allows:
 - Playing against opponents with multiple difficulty levels for various user skill levels.
 - Providing the user with hints to understand fundamental chess theories.
 - Optimizing all possible lines of play and explaining why a move is good or bad.

# How the chess engine works
Programming a chess game in two parts:
   - Using the Stockfish calculation engine to get the best possible moves without computing them on the user's machine
   - Performing minimax calculations on the user's machine using mathematical properties


## Features implemented (Keys)
- Ability to restart a game during your game or at the end of your game (R)
- Undo a move to correct a mistake or find the optimal move (U)
- Request a hint on the current position to minimize errors (H)
- Change difficulty based on your level (changes the opposing AI's level) (←,→)
- Quit the pygame application (esc)

## Project structure
- main.py         The assembly of all Python programs to run the game
- config.py       Sets up interface dimensions, colors, visual appearance, as well as the connection with the Stockfish engine and the different game levels
- plateau.py      Board logic, visual interface, piece placement, and game logic
- MoteurEchecs.py Handles Stockfish integration, position analysis, and tactics
- explainer.py    Explains the game logic, in this case the move played, the position, and the tactics/strategy
- pieces.py       Creates piece rendering and their utility functions

## Libraries used and engine 
Libraries
- pygame: provides the game interface for Python
- chess: handles all chess logic
- chess.engine: submodule of chess that allows communication with Stockfish
- os: allows interaction with my computer's file system
- random: only used in this case to ensure a legal move if Stockfish crashes

Engine
- Stockfish: The most powerful chess engine in the world, capable of calculating up to 20 moves ahead to make the best decision
- Minimax: A function coded by me that can calculate 4/5 moves ahead (between 1 and 50 million calculations performed). It is of course possible to go deeper, but it can take a very long time

## How did I code my minimax alpha-beta?
First, I thought of a minimalist scoring system (compared to Stockfish) that evaluates each move based on 2 parameters.
- The first criterion is piece value. Each piece has a value based on its importance (the number of squares it can cover, except the king which is worth infinity).
- The second criterion is the piece's placement depending on the stage of the game. Indeed, the same piece does not have the same value depending on where it is on the chessboard. A knight placed in the center, for example, controls up to 8 squares, while a knight stuck in a corner only controls 2. It is therefore far less useful. Similarly, a pawn is worth more in the endgame when it is close to promotion than in the opening where it is merely a blocker.
To achieve this, I created 3×6 matrices. 3 represents the number of game phases (opening/middlegame/endgame) and 6 the number of piece types (Rook, Bishop, Knight, Queen, King, and Pawn).

This allows evaluating, for a given piece, the stage of the game, and its square, a value for the piece. For example, a pawn close to promotion can be worth more than a pinned queen.

Now I will explain my game phase system very simply.
- First phase, the chessboard has more than 28 pieces (alive) so we are still in the opening phase.
- Second phase, the chessboard has more than 14 pieces (alive) but fewer than 28 so we are in the middlegame.
- Last phase, the chessboard has fewer than 14 pieces (alive) so we are in the endgame.
It would also have been possible to count in centipawns instead of the number of pieces, which is less consistent in my case, but I prefer to keep things as simple as possible for people who don't fully understand the game.

Finally the most important part, the function itself.
- After watching several videos to understand the mathematical concept of minimax, I decided to code the function even though it was often demonstrated in the videos.
For the explanations, here is the link to the video that helped me understand better. 
- Link: https://youtu.be/l-hh51ncgDI?si=IizlpFgzucJQLukf 
If you don't want to watch, I explain the function here:
- The algorithm sets up two agents, in our case Black and White. The function recursively explores the tree of all possible games up to a certain depth. The "White" player seeks to maximize their score, while "Black" (the opponent) seeks to minimize it. At each node, we alternate between choosing the best move (max) and the worst for us (min). When the depth limit is reached, an evaluation function assigns a score to the position, and these scores propagate back up the tree to determine the best move to play.

## Comments
I made it a habit to comment my code as much as possible so that it is readable and understandable by anyone, even someone discovering the project. It is also a good practice I learned from looking at open source projects on GitHub, where code is always well documented to facilitate collaboration.
For some parts like the Pygame interface that I wasn't very familiar with, I used documentation, tutorials and also AI tools to understand how certain functions work. The comments were also useful for me to memorize certain functions when I would re-read my code later.






