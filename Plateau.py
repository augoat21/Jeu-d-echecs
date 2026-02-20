# board.py - Creation de l'interace du jeu gestion affichage et logique du jeu

import pygame
import chess
from config import *


class Plateau:
    def __init__(self, ecran):
        self.ecran = ecran         # stocke l'inteface de rendu pour ensuite dessiner dessus
        self.board = chess.Board() # librairie python chess permet davoir les pieces en position de depart
        self.historique_coups = [] # stock tout les coups joué pour de un pouvoir annuler le coup si erreur de deux pour avoir l'historique
        self.dernier_coup = None   # stock le dernier coup seulement pour le surligner  

        self.images_pieces = self.charger_pieces() # charge la representation des pieces pour les dessiner ensuite

    def charger_pieces(self):
        """Fonction qui sert a charger les images des pieces avec des carecteres unicode. Cela nous permettra de dessiner les pieces sur le plateau ensuite  """
        pieces = {}
        caracteres_pieces = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }

        police = pygame.font.SysFont("Segoe UI Symbol", TAILLE_CASE - 10) # transforme les symbole en dessin affichable 

        for symbole, caractere in caracteres_pieces.items():
            couleur = (255, 255, 255) if symbole.isupper() else (30, 30, 30)
            texte = police.render(caractere, True, couleur)
            pieces[symbole] = texte
            # permet d'afficher les 12 pieces en fonction de leur symbole et de les stocker dans un dictionnaire (majuscule  pour les blanches et  minuscule pour les noires)

        return pieces
        

    def dessiner(self, case_selectionnee=None, coups_valides=None):
        """Fonction permettant d'afficher tout les points précedement créer"""
        coups_valides = coups_valides or []
        cases_valides = [c.to_square for c in coups_valides]

        for rangee in range(8):
            for colonne in range(8):
                x = DECALAGE_X + colonne * TAILLE_CASE
                y = DECALAGE_Y + rangee * TAILLE_CASE
                case = self.coords_vers_case(rangee, colonne) # Parcours toutes les cases du plateau pour verifier les conditions qui vont suivre 

                
                est_claire = (rangee + colonne) % 2 == 0
                couleur = CASE_BLANCHE if est_claire else CASE_NOIRE
                pygame.draw.rect(self.ecran, couleur, (x, y, TAILLE_CASE, TAILLE_CASE)) # permet d'assigner a chaque case une couleur on fonction de position rangee colonne

                
                if self.dernier_coup:
                    if case in [self.dernier_coup.from_square, self.dernier_coup.to_square]:
                        s = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
                        s.fill(COULEUR_DERNIER_COUP)
                        self.ecran.blit(s, (x, y)) # Surbrillance la case de depart de la piece et celle d'arrivee du coup joué

                
                if case == case_selectionnee:
                    s = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
                    s.fill(COULEUR_SELECTION)
                    self.ecran.blit(s, (x, y)) # Surbrillance de la case de la piece selectionnée

                
                piece = self.board.piece_at(case)
                if piece and piece.piece_type == chess.KING:
                    if self.board.is_check() and piece.color == self.board.turn:
                        s = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
                        s.fill(COULEUR_ECHEC)
                        self.ecran.blit(s, (x, y)) # Surbrillance de la case du roi en rouge si il est en echec

                
                if case in cases_valides:
                    centre = (x + TAILLE_CASE // 2, y + TAILLE_CASE // 2)
                    if self.board.piece_at(case):
                        pygame.draw.circle(self.ecran, (100, 100, 100), centre, TAILLE_CASE // 2 - 5, 4)
                    else:
                        pygame.draw.circle(self.ecran, (100, 100, 100, 150), centre, 12) # indique les coups valides en mettant les points pour les cases de deplacement et les ronds pour les pieces mengeables
                

                
                if piece:
                    image_piece = self.images_pieces[piece.symbol()]
                    rect_piece = image_piece.get_rect(center=(x + TAILLE_CASE // 2, y + TAILLE_CASE // 2))
                    self.ecran.blit(image_piece, rect_piece) # permet de bien positionner les pieces au centre de la case avec le bon symbole

        # Dessiner les coordonnees du plateau a-h 1-8
        self.dessiner_coordonnees()

    def dessiner_coordonnees(self):
        """Methode pour ajoutet les coordonnées du plateau a-h 1-8"""
        police = pygame.font.SysFont(NOM_POLICE, 14)
        colonnes = 'abcdefgh'

        for i in range(8):
            etiquette = police.render(colonnes[i], True, COULEUR_TEXTE)
            x = DECALAGE_X + i * TAILLE_CASE + TAILLE_CASE // 2 - 4
            self.ecran.blit(etiquette, (x, DECALAGE_Y + TAILLE_PLATEAU + 5)) # place les lettres en bas du plateau avec des ajustements pixel (-4/+5)

            etiquette = police.render(str(8 - i), True, COULEUR_TEXTE)
            y = DECALAGE_Y + i * TAILLE_CASE + TAILLE_CASE // 2 - 7
            self.ecran.blit(etiquette, (DECALAGE_X - 20, y)) # place les chiffres a gauche du plateau avec des ajustements pixel (-7/-20)

    def coords_vers_case(self, rangee, colonne):
        """Convertir les coordonnees du plateau en index de case d'echecs"""
        return chess.square(colonne, 7 - rangee)

    def case_vers_coords(self, case):
        """Convertir un index de case d'echecs en coordonnees du plateau"""
        colonne = chess.square_file(case)
        rangee = 7 - chess.square_rank(case)
        return rangee, colonne

    def obtenir_piece_a(self, case):
        """Obtenir la piece sur une case"""
        return self.board.piece_at(case)

    def est_piece_joueur(self, case, couleur_joueur):
        """Verifier si la piece sur la case appartient au joueur"""
        piece = self.board.piece_at(case)
        return piece and piece.color == couleur_joueur

    def est_tour_joueur(self, couleur_joueur):
        """Verifier si c'est le tour du joueur"""
        return self.board.turn == couleur_joueur

    def obtenir_coups_valides(self, case):
        """Obtenir tous les coups valides depuis une case donnée"""
        return [coup for coup in self.board.legal_moves if coup.from_square == case]

    def creer_coup(self, case_depart, case_arrivee):
        """Creer un objet coup, en gerant les promotions de pion automatiquement en dame pour simplifier l'interface"""
        piece = self.board.piece_at(case_depart)
        if piece and piece.piece_type == chess.PAWN:
            rangee_arrivee = chess.square_rank(case_arrivee)
            if (piece.color and rangee_arrivee == 7) or (not piece.color and rangee_arrivee == 0):
                return chess.Move(case_depart, case_arrivee, promotion=chess.QUEEN) 
                # promotion automatique en dame pour simplfier l'interface si un pion noir arrive sur premiere rangée blanche et inversement
        return chess.Move(case_depart, case_arrivee)

    def jouer_coup(self, coup):
        """Executer un coup sur le plateau et mettre a jour l'historique"""
        self.historique_coups.append(self.board.copy())
        self.board.push(coup)
        self.dernier_coup = coup

    def annuler_coup(self):
        """Annuler le dernier coup joué precedement"""
        if self.historique_coups:
            self.board = self.historique_coups.pop()
            self.dernier_coup = None if not self.historique_coups else self.board.peek()

    def reinitialiser(self):
        """Reinitialiser le plateau a la position de depart et viderla cache de l'historique des coups"""
        self.board = chess.Board()
        self.historique_coups = []
        self.dernier_coup = None

    def est_echec_et_mat(self):
        """Verifier si la position courante est un echec et mat"""
        return self.board.is_checkmate()

    def est_pat(self):
        """Verifier si la position courante est un pat"""
        return self.board.is_stalemate()

    def est_nulle(self):
        """Verifier les conditions de nulle"""
        return (self.board.is_insufficient_material() or
                self.board.is_fifty_moves() or
                self.board.is_repetition())

    def obtenir_fen(self):
        """Obtenir la position courante en notation FEN"""
        return self.board.fen()

    def obtenir_coup_san(self, coup):
        """Obtenir le coup en notation algebrique standard"""
        return self.board.san(coup)
