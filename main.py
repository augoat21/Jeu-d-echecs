# main.py - Point d'entree du Chess AI Explainer

import pygame
import sys
import threading
from config import *
from Plateau import Plateau
from MoteurEchecs import MoteurEchecs
from explainer import ExplicateurCoup, GenerateurIndice
from minimax_engine import meilleur_coup as minimax_meilleur_coup


class JeuEchecs:
    def __init__(self):
        pygame.init() 
        self.ecran = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
        pygame.display.set_caption("Chess AI Explainer ♟️")
        self.horloge = pygame.time.Clock() #initialisation de la fenetre de jeu et de l'horloge 

        # Initialiser les composants
        self.plateau = Plateau(self.ecran) #gerer l'affichage et la logique de jeu
        self.moteur = MoteurEchecs() #gerer les calculs de l'ia et les coups
        self.explicateur = ExplicateurCoup() #generer les explications des coups de l'ia
        self.generateur_indice = GenerateurIndice(self.explicateur) #generer les indices pour le joueur si demandé sans relever le coup exact

        # Etat du jeu
        self.case_selectionnee = None #stock la case selectionné
        self.coups_valides = [] #stock les coups valides pour la piece selectionné
        self.couleur_joueur = True  # True = Blancs, False = Noirs
        self.explication_courante = "" # stock lexplcation ducoup de l'ia pour l'affichage
        self.partie_terminee = False #indique si la partie est terminée pour interdire les interactions
        self.difficulte = "Moyen" #niveau de difficulte par defaut du moteur
        self.liste_difficultes = list(NIVEAUX_DIFFICULTE.keys()) #liste les niveaux de difficulte a changer avec les fleches
        self.moteur_ia = "Stockfish"  # "Stockfish" ou "Minimax"
        self.ia_en_cours = False      # True pendant que minimax calcule
        self.coup_ia_calcule = None   # coup retourné par le thread minimax

        # Polices
        self.police_petit = pygame.font.SysFont(NOM_POLICE, TAILLE_POLICE_PETIT)
        self.police_moyen = pygame.font.SysFont(NOM_POLICE, TAILLE_POLICE_MOYEN)
        self.police_grand = pygame.font.SysFont(NOM_POLICE, TAILLE_POLICE_GRAND)
        self.police_titre = pygame.font.SysFont(NOM_POLICE, TAILLE_POLICE_TITRE, bold=True)

    def lancer(self):
        """Boucle principale du jeu qui gere les mises a jour, affichage et evenements utilisateur"""
        while True:
            self.gerer_evenements()
            self.mettre_a_jour()
            self.afficher()
            self.horloge.tick(60)

    def gerer_evenements(self):
        """Gerer les evenements d'entree utilisateur (clique souris, touches clavier)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitter_jeu()

            elif event.type == pygame.KEYDOWN:
                self.gerer_touche(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    self.gerer_clic(event.pos)

    def gerer_touche(self, touche):
        """Gerer les entrees clavier pour les controles en bas a droite de l'ecran"""
        if touche == pygame.K_ESCAPE:
            self.quitter_jeu()
        elif touche == pygame.K_r:
            self.reinitialiser_partie()
        elif touche == pygame.K_u:
            self.annuler_coup()
        elif touche == pygame.K_h:
            self.obtenir_indice()
        elif touche == pygame.K_RIGHT or touche == pygame.K_UP:
            self.changer_difficulte(1)
        elif touche == pygame.K_LEFT or touche == pygame.K_DOWN:
            self.changer_difficulte(-1)
        elif touche == pygame.K_m:
            self.basculer_moteur()

    def gerer_clic(self, pos):
        """Gerer le clic souris sur le plateau pour le deplacement des pieces et les selections"""
        if self.partie_terminee or self.ia_en_cours:
            return

        x, y = pos
        if not (DECALAGE_X <= x < DECALAGE_X + TAILLE_PLATEAU and
                DECALAGE_Y <= y < DECALAGE_Y + TAILLE_PLATEAU):     # verifier si le clic est sur le plateau et convertir en case d'echecs
            return 

        colonne = (x - DECALAGE_X) // TAILLE_CASE
        rangee = (y - DECALAGE_Y) // TAILLE_CASE
        case = self.plateau.coords_vers_case(rangee, colonne)  # convertir en coordonnees du plateau pour les coups et les pieces

        # Gerer la selection et le deplacement des pieces
        if self.case_selectionnee is None: #verifie que aucune piece est selectionné 
            piece = self.plateau.obtenir_piece_a(case) #recupere la piece sur la case cliquer si il y'en a une 
            if piece and self.plateau.est_piece_joueur(case, self.couleur_joueur):  #verifie que la piece appartient au joueur et que cest son tour
                self.case_selectionnee = case
                self.coups_valides = self.plateau.obtenir_coups_valides(case)
        else:
            # Essayer de jouer
            coup = self.plateau.creer_coup(self.case_selectionnee, case)
            if coup in self.coups_valides:
                self.jouer_coup_joueur(coup) #si le coup est possible le jouer et afficher l'explication de l'ia

            # Deselectionner
            self.case_selectionnee = None
            self.coups_valides = []

    def jouer_coup_joueur(self, coup):
        """Executer le coup du joueur et declencher la reponse de l'IA"""
        self.plateau.jouer_coup(coup)
        self.explication_courante = ""

        if self.verifier_fin_partie():
            return

        self.jouer_coup_ia() # L'IA repond apres le coup

    def jouer_coup_ia(self):
        """Calculer et executer le coup de l'IA avec explication"""
        if self.moteur_ia == "Stockfish":
            reglages = NIVEAUX_DIFFICULTE[self.difficulte]
            self.moteur.definir_difficulte(reglages["competence"], reglages["profondeur"])
            coup, analyse = self.moteur.obtenir_meilleur_coup(self.plateau.board)
            if coup:
                self.explication_courante = self.explicateur.expliquer_coup(
                    self.plateau.board, coup, analyse
                )
                self.plateau.jouer_coup(coup)
                self.verifier_fin_partie()
        else:
            # Lancer minimax dans un thread pour ne pas geler pygame
            self.ia_en_cours = True
            self.coup_ia_calcule = None
            self.explication_courante = "Minimax réfléchit... (prof. 4)"
            board_copie = self.plateau.board.copy()

            def calculer():
                self.coup_ia_calcule = minimax_meilleur_coup(board_copie, depth=4)
                self.ia_en_cours = False

            threading.Thread(target=calculer, daemon=True).start()

    def basculer_moteur(self):
        """Basculer entre Stockfish et Minimax"""
        self.moteur_ia = "Minimax" if self.moteur_ia == "Stockfish" else "Stockfish"
        self.explication_courante = f"Moteur IA : {self.moteur_ia}"

    def obtenir_indice(self):
        """Afficher un indice pour le joueur sans reveler le coup exact optimal"""
        if self.partie_terminee or not self.plateau.est_tour_joueur(self.couleur_joueur):
            return

        meilleur_coup, analyse = self.moteur.obtenir_meilleur_coup(self.plateau.board)
        if meilleur_coup:
            self.explication_courante = "Conseil: " + self.generateur_indice.generer_indice(
                self.plateau.board, meilleur_coup, analyse 
            ) # generer l'indice du coup optimal sans donner le coup

    def changer_difficulte(self, direction):
        """Changer le niveau de difficulte avec les fleches"""
        index_actuel = self.liste_difficultes.index(self.difficulte)
        nouvel_index = max(0, min(len(self.liste_difficultes) - 1, index_actuel + direction))
        self.difficulte = self.liste_difficultes[nouvel_index]
        self.explication_courante = f"Difficulté: {self.difficulte}" #different niveau de difficulte pour le moteur de calcul stockfish

    def verifier_fin_partie(self):
        """Verifier si la partie est terminee avec 3  possibilites : echec et mat, pat ou nulle"""
        if self.plateau.est_echec_et_mat():
            gagnant = "Noirs" if self.plateau.board.turn else "Blancs"
            self.explication_courante = f"♔ Échec et mat ! Les {gagnant} gagnent !"
            self.partie_terminee = True
            return True
        elif self.plateau.est_pat():
            self.explication_courante = "Pat ! Match nul."
            self.partie_terminee = True
            return True
        elif self.plateau.est_nulle():
            self.explication_courante = "Match nul."
            self.partie_terminee = True
            return True
        return False

    def reinitialiser_partie(self):
        """Reinitialiser la partie a l'etat initial pour recommencer une nouvelle partie et vider l'historique des coups"""
        self.plateau.reinitialiser()
        self.moteur.reinitialiser()
        self.case_selectionnee = None
        self.coups_valides = []
        self.explication_courante = "Nouvelle partie ! Les blancs commencent."
        self.partie_terminee = False

    def annuler_coup(self):
        """Annuler les deux derniers coups (joueur + IA) pour pouvoir rectifier son erreur et apprendre grace au score centipions"""
        if len(self.plateau.historique_coups) >= 2:
            self.plateau.annuler_coup()
            self.plateau.annuler_coup()
            self.explication_courante = "Coup annulé."
            self.partie_terminee = False

    def mettre_a_jour(self):
        """Mettre a jour l'etat du jeu — joue le coup minimax quand le thread a fini."""
        if not self.ia_en_cours and self.coup_ia_calcule is not None:
            coup = self.coup_ia_calcule
            self.coup_ia_calcule = None
            if coup:
                self.explication_courante = f"Minimax (prof. 4) joue : {self.plateau.board.san(coup)}"
                self.plateau.jouer_coup(coup)
                self.verifier_fin_partie()

    def afficher(self):
        """Afficher le jeu"""
        self.ecran.fill(COULEUR_FOND)

        # Dessiner le titre du programme 
        titre = self.police_titre.render("Chess AI Explainer", True, COULEUR_TEXTE)
        self.ecran.blit(titre, (DECALAGE_X, 15))

        # Dessiner le plateau 
        self.plateau.dessiner(self.case_selectionnee, self.coups_valides)

        # Dessiner le panneau lateral avec les informations et boutons de controle
        self.dessiner_panneau_lateral()

        pygame.display.flip()

    def dessiner_panneau_lateral(self):
        """Dessiner le panneau d'information a droite du plateau avec les details indices de la partie et boutons de controle"""
        panneau_x = DECALAGE_X + TAILLE_PLATEAU + 30
        largeur_panneau = LARGEUR_FENETRE - panneau_x - 20

        # Fond du panneau
        pygame.draw.rect(
            self.ecran, COULEUR_PANNEAU,
            (panneau_x, DECALAGE_Y, largeur_panneau, TAILLE_PLATEAU),
            border_radius=10
        )

        y = DECALAGE_Y + 20

        # Moteur IA actif
        couleur_moteur = COULEUR_ACCENT if self.moteur_ia == "Stockfish" else (100, 180, 255)
        etiquette_moteur = self.police_moyen.render(f"IA: {self.moteur_ia}  [M]", True, couleur_moteur)
        self.ecran.blit(etiquette_moteur, (panneau_x + 15, y))
        y += 30

        # Difficulte (uniquement pertinent pour Stockfish)
        etiquette_diff = self.police_moyen.render(f"Difficulté: {self.difficulte}", True, COULEUR_ACCENT)
        self.ecran.blit(etiquette_diff, (panneau_x + 15, y))
        y += 40

        # Indicateur de tour
        tour = "Blancs" if self.plateau.board.turn else "Noirs"
        etiquette_tour = self.police_moyen.render(f"Tour: {tour}", True, COULEUR_TEXTE)
        self.ecran.blit(etiquette_tour, (panneau_x + 15, y))
        y += 50

        # Boite d'explication
        titre_expl = self.police_moyen.render("Analyse IA:", True, COULEUR_ACCENT)
        self.ecran.blit(titre_expl, (panneau_x + 15, y))
        y += 30

        # Retour a la ligne de l'explication
        self.dessiner_texte_retour_ligne(
            self.explication_courante,
            panneau_x + 15, y,
            largeur_panneau - 30,
            self.police_petit, COULEUR_TEXTE
        )

        # Aide des controles en bas avec fonctions 
        controles_y = DECALAGE_Y + TAILLE_PLATEAU - 140
        controles = [
            "R - Nouvelle partie",
            "U - Annuler",
            "H - Indice",
            "M - Changer moteur",
            "←/→ - Difficulté",
            "ESC - Quitter"
        ]
        for ctrl in controles:
            texte_ctrl = self.police_petit.render(ctrl, True, (150, 150, 150))
            self.ecran.blit(texte_ctrl, (panneau_x + 15, controles_y))
            controles_y += 22

    def dessiner_texte_retour_ligne(self, texte, x, y, largeur_max, police, couleur):
        """Dessiner du texte avec retour a la ligne automatique pour la largeur du panneau"""
        mots = texte.split(' ')
        lignes = []
        ligne_courante = ""

        for mot in mots:
            ligne_test = ligne_courante + mot + " "
            if police.size(ligne_test)[0] <= largeur_max:
                ligne_courante = ligne_test
            else:
                if ligne_courante:
                    lignes.append(ligne_courante)
                ligne_courante = mot + " "

        if ligne_courante:
            lignes.append(ligne_courante)

        for ligne in lignes:
            surface_texte = police.render(ligne.strip(), True, couleur)
            self.ecran.blit(surface_texte, (x, y))
            y += police.get_height() + 4

    def quitter_jeu(self):
        """Nettoyer et quitter le programme de jeu"""
        self.moteur.quitter()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jeu = JeuEchecs()
    jeu.lancer()
