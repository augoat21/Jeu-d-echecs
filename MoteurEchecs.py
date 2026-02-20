# engine.py - Integration du moteur d'echecs Stockfish

import chess
import chess.engine
from config import CHEMIN_STOCKFISH, PROFONDEUR_DEFAUT, LIMITE_TEMPS_DEFAUT


class MoteurEchecs:
    def __init__(self):
        self.moteur = None
        self.niveau_competence = 10
        self.profondeur = PROFONDEUR_DEFAUT
        self.connecter()

    def connecter(self):
        """Connecter au moteur Stockfish."""
        try:
            self.moteur = chess.engine.SimpleEngine.popen_uci(CHEMIN_STOCKFISH)
            self.moteur.configure({"Skill Level": self.niveau_competence})
            print(f"[OK] Stockfish connecte: {CHEMIN_STOCKFISH}")
        except Exception as e:
            print(f"[ERREUR] Erreur Stockfish: {e}")
            print("  Vérifiez le chemin dans config.py")
            self.moteur = None

    def definir_difficulte(self, niveau_competence, profondeur):
        """Definir la difficulte de l'IA."""
        self.niveau_competence = niveau_competence
        self.profondeur = profondeur
        if self.moteur:
            self.moteur.configure({"Skill Level": niveau_competence})

    def obtenir_meilleur_coup(self, plateau):
        """
        Obtenir le meilleur coup et l'analyse pour la position courante.

        Retourne:
            tuple: (meilleur_coup, dictionnaire_analyse)
        """
        if not self.moteur:
            return self._coup_secours(plateau), {}

        try:
            # Analyser la position
            info = self.moteur.analyse(
                plateau,
                chess.engine.Limit(depth=self.profondeur, time=LIMITE_TEMPS_DEFAUT)
            )

            meilleur_coup = info.get("pv", [None])[0]

            # Construire les donnees d'analyse
            analyse = {
                "score": self._formater_score(info.get("score")),
                "valeur_score": self._obtenir_valeur_score(info.get("score")),
                "profondeur": info.get("depth", 0),
                "vp": info.get("pv", [])[:5],  # Variation principale (top 5 coups)
                "noeuds": info.get("nodes", 0),
            }

            # Obtenir l'analyse supplementaire pour l'explication
            analyse.update(self._analyser_position(plateau, meilleur_coup))

            return meilleur_coup, analyse

        except Exception as e:
            print(f"Erreur analyse: {e}")
            return self._coup_secours(plateau), {}

    def _formater_score(self, score):
        """Formater le score du moteur pour l'affichage."""
        if score is None:
            return "?"

        if score.is_mate():
            mat_en = score.white().mate()  # Toujours du point de vue des Blancs
            if mat_en is None:
                return "?"
            if mat_en > 0:
                return f"Mat en {mat_en}"
            else:
                return f"Mat en {-mat_en} (pour les Noirs)"
        else:
            cp = score.white().score()  # Toujours du point de vue des Blancs (+ = Blancs gagnent)
            if cp is not None:
                pions = cp / 100
                signe = "+" if pions >= 0 else ""
                return f"{signe}{pions:.2f}"
        return "?"

    def _obtenir_valeur_score(self, score):
        """Obtenir la valeur numerique du score en centipions."""
        if score is None:
            return 0
        if score.is_mate():
            mat_en = score.white().mate()  # Toujours du point de vue des Blancs
            if mat_en is None:
                return 0
            return 10000 if mat_en > 0 else -10000
        cp = score.white().score()  # Toujours du point de vue des Blancs
        return cp if cp else 0

    def _analyser_position(self, plateau, coup):
        """Analyser les details de la position pour generer l'explication."""
        analyse = {
            "est_capture": plateau.is_capture(coup) if coup else False,
            "est_echec": False,
            "est_roque": plateau.is_castling(coup) if coup else False,
            "piece_jouee": None,
            "piece_capturee": None,
            "donne_echec": False,
            "est_promotion": False,
            "menaces": [],
            "defenses": [],
        }

        if not coup:
            return analyse

        # Obtenir les infos de la piece
        piece = plateau.piece_at(coup.from_square)
        if piece:
            analyse["piece_jouee"] = piece.symbol()

        # Verifier la capture
        capturee = plateau.piece_at(coup.to_square)
        if capturee:
            analyse["piece_capturee"] = capturee.symbol()

        # Verifier la prise en passant
        if plateau.is_en_passant(coup):
            analyse["est_capture"] = True
            analyse["piece_capturee"] = 'p' if plateau.turn else 'P'

        # Verifier si le coup donne echec
        copie_plateau = plateau.copy()
        copie_plateau.push(coup)
        analyse["donne_echec"] = copie_plateau.is_check()

        # Verifier la promotion
        if coup.promotion:
            analyse["est_promotion"] = True
            analyse["piece_promotion"] = chess.piece_name(coup.promotion)

        # Analyser les elements tactiques
        analyse.update(self._analyser_tactiques(plateau, coup))

        return analyse

    def _analyser_tactiques(self, plateau, coup):
        """Detecter les motifs tactiques dans le coup."""
        tactiques = {
            "est_fourchette": False,
            "est_clouage": False,
            "est_enfilade": False,
            "attaque_piece_en_prise": False,
            "defend_piece": False,
            "controle_centre": False,
            "developpe_piece": False,
        }

        # Jouer le coup temporairement
        copie_plateau = plateau.copy()
        copie_plateau.push(coup)

        piece = plateau.piece_at(coup.from_square)
        if not piece:
            return tactiques

        # Verifier le controle du centre (e4, d4, e5, d5)
        cases_centrales = [chess.E4, chess.D4, chess.E5, chess.D5]
        if coup.to_square in cases_centrales:
            tactiques["controle_centre"] = True

        # Verifier le developpement (sortie de la rangee de depart)
        rangee_depart = chess.square_rank(coup.from_square)
        if (plateau.turn and rangee_depart == 0) or (not plateau.turn and rangee_depart == 7):
            if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                tactiques["developpe_piece"] = True

        # Verifier la fourchette (piece attaque plusieurs pieces adverses)
        attaques = copie_plateau.attacks(coup.to_square)
        pieces_attaquees = []
        for case in attaques:
            cible = copie_plateau.piece_at(case)
            if cible and cible.color != piece.color:
                if cible.piece_type in [chess.QUEEN, chess.ROOK, chess.KING]:
                    pieces_attaquees.append(cible.piece_type)

        if len(pieces_attaquees) >= 2:
            tactiques["est_fourchette"] = True

        return tactiques

    def _coup_secours(self, plateau):
        """Retourner un coup legal aleatoire quand le moteur est indisponible."""
        coups_legaux = list(plateau.legal_moves)
        if coups_legaux:
            import random
            return random.choice(coups_legaux)
        return None

    def obtenir_evaluation(self, plateau):
        """Obtenir l'evaluation de la position sans jouer de coup."""
        if not self.moteur:
            return {"score": "?", "valeur_score": 0}

        try:
            info = self.moteur.analyse(plateau, chess.engine.Limit(depth=self.profondeur))
            return {
                "score": self._formater_score(info.get("score")),
                "valeur_score": self._obtenir_valeur_score(info.get("score"))
            }
        except:
            return {"score": "?", "valeur_score": 0}

    def reinitialiser(self):
        """Reinitialiser l'etat du moteur."""
        pass  # Stockfish n'a pas besoin de reinitialisation explicite

    def quitter(self):
        """Liberer les ressources du moteur."""
        if self.moteur:
            self.moteur.quit()
            self.moteur = None
