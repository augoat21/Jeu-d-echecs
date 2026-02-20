# pieces.py - Utilitaires et aides au rendu des pieces d'echecs

import pygame
import chess
import os
from config import TAILLE_CASE


class RenduPieces:
    """Gere le chargement et le rendu des pieces d'echecs. Supporte les symboles Unicode et les fichiers images"""

    # Symboles Unicode des pieces
    PIECES_UNICODE = {
        'K': '♔', 'R': '♕', 'T': '♖', 'F': '♗', 'C': '♘', 'P': '♙',
        'k': '♚', 'r': '♛', 't': '♜', 'f': '♝', 'c': '♞', 'p': '♟'
    }

    # Noms de fichiers standard des pieces (pour le chargement d'images)
    FICHIERS_PIECES = {
        'K': 'wK', 'R': 'wR', 'T': 'wT', 'F': 'wF', 'C': 'wC', 'P': 'wP',
        'k': 'bK', 'r': 'bR', 't': 'bT', 'f': 'bF', 'c': 'bC', 'p': 'bP'
    }

    def __init__(self, chemin_ressources="assets/pieces"):
        self.chemin_ressources = chemin_ressources
        self.images = {}
        self.utiliser_images = self._charger_images()

        if not self.utiliser_images:
            self._creer_surfaces_unicode()

    def _charger_images(self):
        """Essayer de charger les images des pieces depuis le dossier ressource"""
        if not os.path.exists(self.chemin_ressources):
            return False

        try:
            for symbole, nom_fichier in self.FICHIERS_PIECES.items():
                for ext in ['.png', '.svg', '.jpg']:
                    chemin = os.path.join(self.chemin_ressources, f"{nom_fichier}{ext}")
                    if os.path.exists(chemin):
                        img = pygame.image.load(chemin)
                        img = pygame.transform.scale(img, (TAILLE_CASE - 10, TAILLE_CASE - 10))
                        self.images[symbole] = img #Essayer les formats d'image courants
                        break

            return len(self.images) == 12  #Toutes les pieces chargees
        except Exception as e:
            print(f"Impossible de charger les images des pieces: {e}")
            return False

    def _creer_surfaces_unicode(self):
        """Creer les surfaces des pieces avec des caracteres Unicode"""
        taille_police = TAILLE_CASE - 8

        
        noms_polices = ["Segoe UI Symbol", "Arial Unicode MS", "DejaVu Sans", "Symbola"] #essayer differentes polices supportant les symboles d'echecs
        police = None

        for nom in noms_polices:
            try:
                police = pygame.font.SysFont(nom, taille_police) #tester si la police peut afficher les symboles d'echecs
                test = police.render('♔', True, (0, 0, 0))
                if test.get_width() > 5:  # Rendu valide
                    break
            except:
                continue

        if not police:
            police = pygame.font.SysFont(None, taille_police)

        for symbole, caractere in self.PIECES_UNICODE.items():
            est_blanc = symbole.isupper()

            couleur = (255, 255, 255) if est_blanc else (40, 40, 40)
            couleur_contour = (40, 40, 40) if est_blanc else (255, 255, 255) #creer la surface avec la piece

            texte = police.render(caractere, True, couleur)  #rendu avec effet de contour pour la visibilite

            taille = max(texte.get_width(), texte.get_height()) + 4
            surface = pygame.Surface((taille, taille), pygame.SRCALPHA) #creer une surface legerement plus grande pour le contour

            contour = police.render(caractere, True, couleur_contour)
            for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                pos = ((taille - contour.get_width()) // 2 + dx,
                       (taille - contour.get_height()) // 2 + dy)
                surface.blit(contour, pos) #dessiner le contour (rendu dans 8 directions)

            pos = ((taille - texte.get_width()) // 2,
                   (taille - texte.get_height()) // 2)
            surface.blit(texte, pos) #dessiner la piece principale

            self.images[symbole] = surface

    def obtenir_surface_piece(self, symbole_piece):
        """Obtenir la surface pour un symbole de piece"""
        return self.images.get(symbole_piece)

    def dessiner_piece(self, ecran, symbole_piece, x, y):
        """Dessiner une piece a la position specifiee (centree de la case)"""
        surface = self.obtenir_surface_piece(symbole_piece)
        if surface:
            rect = surface.get_rect(center=(x + TAILLE_CASE // 2, y + TAILLE_CASE // 2))
            ecran.blit(surface, rect)


def valeur_piece(type_piece):
    """Retourner la valeur materielle d'un type de piece en fonction de la convention classique"""
    valeurs = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # Le roi n'a pas de prix car il est indispensable mais considéré reelement comme valeur infinie a coté des autres pieces
    }
    return valeurs.get(type_piece, 0)


def nom_piece_fr(symbole_piece):
    """Retourner le nom des pieces"""
    noms = {
        'P': 'Pion', 'C': 'Cavalier', 'F': 'Fou', 'T': 'Tour', 'R': 'Dame', 'K': 'Roi',
        'p': 'Pion', 'c': 'Cavalier', 'f': 'Fou', 't': 'Tour', 'r': 'Dame', 'k': 'Roi'
    }
    return noms.get(symbole_piece, 'Pièce')


def compter_materiel(plateau):
    """Compter la balance materielle sur le plateau.Positif = avantage blanc, negatif = avantage noir sans prendre en compte l'avantage de la position"""
    balance = 0
    for case in chess.SQUARES:
        piece = plateau.piece_at(case)
        if piece:
            valeur = valeur_piece(piece.piece_type)
            if piece.color == chess.WHITE:
                balance += valeur
            else:
                balance -= valeur
    return balance


def obtenir_activite_piece(plateau, couleur):
    """Estimer l'activite des pieces (nombre de cases controlees/valeur)"""
    activite = 0
    for case in chess.SQUARES:
        piece = plateau.piece_at(case)
        if piece and piece.color == couleur:
            activite += len(plateau.attacks(case)) #check le contrrole des cases par les pieces pour  estimer leur activite/valeur
    return activite


def est_piece_developpee(plateau, case):
    """Verifier si une piece a quitte sa position de depart"""
    piece = plateau.piece_at(case)
    if not piece:
        return False

    # Cases de depart des pieces
    departs_blancs = {
        chess.KNIGHT: [chess.B1, chess.G1],
        chess.BISHOP: [chess.C1, chess.F1],
        chess.ROOK: [chess.A1, chess.H1],
        chess.QUEEN: [chess.D1],
        chess.KING: [chess.E1]
    }

    departs_noirs = {
        chess.KNIGHT: [chess.B8, chess.G8],
        chess.BISHOP: [chess.C8, chess.F8],
        chess.ROOK: [chess.A8, chess.H8],
        chess.QUEEN: [chess.D8],
        chess.KING: [chess.E8]
    }

    departs = departs_blancs if piece.color == chess.WHITE else departs_noirs
    cases_depart = departs.get(piece.piece_type, [])

    return case not in cases_depart
