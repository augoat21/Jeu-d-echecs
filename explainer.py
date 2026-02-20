# explainer.py - Generateur d'explications de coups

import chess


class ExplicateurCoup:
    """Genere des explications en langage naturel pour les coups d'echecs."""

    NOMS_PIECES = {
        'P': 'pion', 'C': 'cavalier', 'F': 'fou', 'T': 'tour', 'R': 'reine', 'K': 'roi',
        'p': 'pion', 'c': 'cavalier', 'f': 'fou', 't': 'tour', 'r': 'reine', 'k': 'roi'
    }

    VALEURS_PIECES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    # déjà expliqué dans pieces.py
    def __init__(self):
        pass

    def expliquer_coup(self, plateau, coup, analyse):
        """Generer une explication en langage naturel pour un coup d'echecs."""
        if not coup:
            return "Aucun coup disponible."

        explications = []

        
        piece = plateau.piece_at(coup.from_square)
        nom_piece = self.NOMS_PIECES.get(piece.symbol(), "pièce") if piece else "pièce"
        case_depart = chess.square_name(coup.from_square)
        case_arrivee = chess.square_name(coup.to_square) # obtenir les infos de base du coup pour construire la description

        desc_coup = self._decrire_coup(plateau, coup, nom_piece, case_depart, case_arrivee, analyse)
        explications.append(desc_coup) # construire la description du coup avec le moteur d'analyse


        
        expl_tactique = self._expliquer_tactiques(analyse)
        if expl_tactique:
            explications.append(expl_tactique) # ajouter les explications tactiques (immediats concrets)

        
        expl_strategique = self._expliquer_strategie(plateau, coup, analyse)
        if expl_strategique:
            explications.append(expl_strategique) # ajouter les explications strategiques (long termes et positionnels)

        
        expl_evaluation = self._expliquer_evaluation(analyse)
        if expl_evaluation:
            explications.append(expl_evaluation) # ajouter le contexte d'evaluation (avantage materiel, positionnel ou decisif)

        return " ".join(explications)

    def _decrire_coup(self, plateau, coup, nom_piece, case_depart, case_arrivee, analyse):
        """Generer la description de base du coup."""

        # Coups speciaux
        if analyse.get("est_roque"):
            if chess.square_file(coup.to_square) > chess.square_file(coup.from_square):
                return "Petit roque ! Le roi se met en sécurité tout en activant la tour."
            else:
                return "Grand roque ! Le roi se met en sécurité sur l'aile dame."

        if analyse.get("est_promotion"):
            piece_promo = analyse.get("piece_promotion", "dame")
            return f"⬆Promotion ! Le pion devient une {piece_promo} en {case_arrivee}." # en reine pour simplifier meme si dans de rare cas le cavalier est plus pertinent

        
        if analyse.get("est_capture"):
            capturee = analyse.get("piece_capturee", "")
            nom_capturee = self.NOMS_PIECES.get(capturee, "pièce") # Coups de capture

            # verifier si c'est un bon/mauvais echange
            if capturee:
                obj_piece = plateau.piece_at(coup.from_square)
                obj_capturee = plateau.piece_at(coup.to_square)

                if obj_piece and obj_capturee:
                    val_piece = self.VALEURS_PIECES.get(obj_piece.piece_type, 0)
                    val_capturee = self.VALEURS_PIECES.get(obj_capturee.piece_type, 0)

                    if val_capturee > val_piece:
                        return f"Gain matériel ! Le {nom_piece} capture le {nom_capturee} en {case_arrivee}."
                    elif val_capturee == val_piece:
                        return f"Échange : le {nom_piece} prend le {nom_capturee} en {case_arrivee}."

            return f"Le {nom_piece} capture en {case_arrivee}."

        # Coups d'echec
        if analyse.get("donne_echec"):
            return f"Échec ! Le {nom_piece} attaque le roi adverse depuis {case_arrivee}."

        # Coups normaux
        return f"Le {nom_piece} se déplace de {case_depart} vers {case_arrivee}."

    def _expliquer_tactiques(self, analyse):
        """Expliquer les motifs tactiques du coup avec des situations precises"""
        tactiques = []

        if analyse.get("est_fourchette"):
            tactiques.append("Fourchette ! Cette pièce attaque plusieurs cibles en même temps.") # attaque deux pieces en meme temps

        if analyse.get("est_clouage"):
            tactiques.append("Clouage ! Une pièce adverse est immobilisée.") # bloque une piece adverse qui protege une piece plus importante derriere elle

        if analyse.get("est_enfilade"):
            tactiques.append("Enfilade ! Une pièce de valeur est forcée de bouger, exposant une autre.") # une piece de valeur est attaque et doit se deplacer laissant une piece derriere

        if analyse.get("attaque_piece_en_prise"):
            tactiques.append("Cette pièce attaque un élément non défendu.") # attaque une piece qui n'est pas defendue

        return " ".join(tactiques) if tactiques else ""

    def _expliquer_strategie(self, plateau, coup, analyse):
        """Expliquer les aspects strategiques du coup avec des concepts positionnels"""
        strategies = []

        if analyse.get("controle_centre"):
            strategies.append("Contrôle du centre : position clé sur l'échiquier.")

        if analyse.get("developpe_piece"):
            strategies.append("Développement : la pièce entre en jeu activement.")

        # verifier les coups pour mettre en sécurité le roi 
        piece = plateau.piece_at(coup.from_square)
        if piece and piece.piece_type == chess.KING:
            colonne_arrivee = chess.square_file(coup.to_square)
            if colonne_arrivee in [0, 1, 6, 7]:  # Deplacement vers le bord pour chercher la sécurité
                strategies.append("Le roi cherche la sécurité.")

        # Verifier les avances de pion pour les promotions potentielles  valeur 1->9
        if piece and piece.piece_type == chess.PAWN:
            rangee_arrivee = chess.square_rank(coup.to_square)
            if (piece.color and rangee_arrivee >= 5) or (not piece.color and rangee_arrivee <= 2):
                strategies.append("Pion avancé : menace de promotion à surveiller.")

        return " ".join(strategies) if strategies else ""

    def _expliquer_evaluation(self, analyse):
        """Expliquer l'evaluation de la position apres un coup en se basant sur le modele stockfish de calcul"""
        score = analyse.get("score", "")
        valeur_score = analyse.get("valeur_score", 0)

        if not score:
            return ""

        # Verifier le mat
        if "Mat" in score:
            return f"🎯 {score} !"

        # Interpreter le score en centipions evaluation stockfish : echelle faites à partir des blancs (+ avantage blanc)/(- avantage noir) +100 un pion d'avance est considéré
        if valeur_score > 300:
            return f" Avantage décisif ({score})."
        elif valeur_score > 150:
            return f" Bel avantage ({score})."
        elif valeur_score > 50:
            return f" Légère avance ({score})."
        elif valeur_score > -50:
            return f" Position équilibrée ({score})."
        elif valeur_score > -150:
            return f" Légère difficulté ({score})."
        else:
            return f" Position difficile ({score})."

    def expliquer_position(self, plateau):
        """Generer une explication de la position courante"""
        explications = []

        # Comptage materiel
        materiel = self._compter_materiel(plateau)
        if materiel > 0:
            explications.append(f"Les blancs ont un avantage matériel de {materiel} point(s).")
        elif materiel < 0:
            explications.append(f"Les noirs ont un avantage matériel de {-materiel} point(s).")
        else:
            explications.append("Le matériel est égal.")

        # Statut d'echec
        if plateau.is_check():
            explications.append("Le roi est en échec !")

        # Phase de la partie evaluée à partir des pieces restantes
        total_pieces = len(plateau.piece_map())
        if total_pieces > 24:
            explications.append("Nous sommes en ouverture.")
        elif total_pieces > 12:
            explications.append("Nous sommes en milieu de partie.")
        else:
            explications.append("Nous sommes en finale.")

        return " ".join(explications)

    def _compter_materiel(self, plateau):
        """Compter la balance materielle à l'aide du comptage en centipions"""
        balance = 0
        for case, piece in plateau.piece_map().items():
            valeur = self.VALEURS_PIECES.get(piece.piece_type, 0)
            if piece.color:  # Blancs
                balance += valeur
            else:  # Noirs
                balance -= valeur
        return balance


class GenerateurIndice:
    """Genere des indices utiles pour les joueurs."""

    def __init__(self, explicateur):
        self.explicateur = explicateur

    def generer_indice(self, plateau, meilleur_coup, analyse):
        """Generer un indice sans reveler le coup exact"""
        if not meilleur_coup:
            return "Analysez la position attentivement"

        indices = []
        piece = plateau.piece_at(meilleur_coup.from_square)

        if piece:
            nom_piece = self.explicateur.NOMS_PIECES.get(piece.symbol(), "pièce")

            # Donner une direction vague
            if analyse.get("est_capture"):
                indices.append(f"Cherchez une capture avec votre {nom_piece}.")
            elif analyse.get("donne_echec"):
                indices.append("Il y a un échec disponible.")
            elif analyse.get("est_fourchette"):
                indices.append("Une fourchette est possible !")
            elif analyse.get("controle_centre"):
                indices.append("Pensez à contrôler le centre.")
            elif analyse.get("developpe_piece"):
                indices.append("Développez vos pièces.")
            else:
                indices.append(f"Votre {nom_piece} peut améliorer sa position.")

        return " ".join(indices) if indices else "Réfléchissez à la meilleure suite."
