# config.py - Configurations de la  represation du jeu et de l'IA  Stockfish

import os


LARGEUR_FENETRE = 900
HAUTEUR_FENETRE = 700
TAILLE_PLATEAU = 560
TAILLE_CASE = TAILLE_PLATEAU // 8
DECALAGE_X = 50
DECALAGE_Y = 70
# Reglages de la fenetre du jeu  

CASE_BLANCHE = (240, 217, 181)
CASE_NOIRE = (181, 136, 99)
COULEUR_SURBRILLANCE = (186, 202, 68, 180)
COULEUR_SELECTION = (246, 246, 105, 200)
COULEUR_DERNIER_COUP = (205, 210, 106, 150)
COULEUR_ECHEC = (235, 97, 80, 180)
COULEUR_COUP_VALIDE = (100, 100, 100, 80)
# Couleurs des cases des cases et surbrillances des coups 

COULEUR_FOND = (32, 32, 35)
COULEUR_PANNEAU = (45, 45, 48)
COULEUR_TEXTE = (220, 220, 220)
COULEUR_ACCENT = (76, 175, 80)
# Couleurs de l'interface du  jeu

CHEMIN_STOCKFISH = os.environ.get("STOCKFISH_PATH", r"C:\Users\augus\Downloads\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe")
# mise en  relation avec le moteur  de calcul Stockfish pour les coups et les analyses crucial

PROFONDEUR_DEFAUT = 15  # calcul du nombre de coups calculer par stockfish 15 dans ce cas
LIMITE_TEMPS_DEFAUT = 1.0  # Limite de temps par coup en secondes


NIVEAUX_DIFFICULTE = {
    "Débutant": {"competence": 1, "profondeur": 5},
    "Facile": {"competence": 5, "profondeur": 8},
    "Moyen": {"competence": 10, "profondeur": 12},
    "Difficile": {"competence": 15, "profondeur": 15},
    "Expert": {"competence": 20, "profondeur": 20},
}
#tout les niveaux de difficulte pour le moteur de calcul


NOM_POLICE = "Segoe UI"
TAILLE_POLICE_PETIT = 14
TAILLE_POLICE_MOYEN = 18
TAILLE_POLICE_GRAND = 24
TAILLE_POLICE_TITRE = 32
# Polices et tailles du texte
