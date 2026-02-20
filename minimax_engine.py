import chess
def score_minamax(piece,case,phase):
    """Evaluer la position d'une piece en fonction de sa valeur et de sa position sur le plateau"""
    valeurs = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    # Bonus de position pour les pieces
    Pion_position_debut = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5], 
        [5, -5, -10, 0, 0, -10, -5, 5], 
        [0, 0, 0, 20, 20, 0, 0, 0], 
        [ 5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10], 
        [50, 50, 50, 50, 50, 50, 50, 50], 
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    Pion_position_milieu = [
        [ 0,  0,  0,  0,  0,  0,  0,  0,],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 5, 25, 25, 5, 0, 0],
        [5, 5, 10, 27, 27, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    Pion_position_fin = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [10, 10, 10, 10, 10, 10, 10, 10],
        [15, 15, 15, 15, 15, 15, 15, 15],
        [20, 20, 20, 20, 20, 20, 20, 20],
        [30, 30, 30, 30, 30, 30, 30, 30],
        [80, 80, 80, 80, 80, 80, 80, 80],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    Cavalier_position_debut = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    Cavalier_position_milieu = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 20, 25, 25, 20, 0, -30],
        [-30, 5, 20, 25, 25, 20, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    Cavalier_position_fin = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 5, 10, 10, 5, 0, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 0, 5, 10, 10, 5, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    Fou_position_debut = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    Fou_position_milieu = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 12, 12, 12, 12, 12, 12, -10],
        [-10, 0, 12, 12, 12, 12, 0, -10],
        [-10, 5, 10, 12, 12, 10, 5, -10],
        [-10, 0, 8, 12, 12, 8, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    Fou_position_fin = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 8, 8, 5, 0, -10],
        [-10, 0, 5, 8, 8, 5, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    Tour_position_debut = [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5,0, 0, 5, 5, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0,0,0,0,0,0,0,0]
    ]

    Tour_position_milieu = [
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ]

    Tour_position_fin = [
        [-15, -15, -15, -15, -15, -15, -15, -15],
        [-10, -10, -10, -10, -10, -10, -10, -10],
        [-5, -5, -5, -5, -5, -5, -5, -5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [10, 10, 10, 10, 10, 10, 10, 10],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    Reine_position_debut = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0,-5],
        [-10, 0, 5, 5, 5, 5, 0,-10],
        [-10, 0, 0, 0, 0, 0, 0,-10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    Reine_position_milieu = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0,-5],
        [-10, 5, 5, 5, 5, 5, 0,-10],
        [-10, 0, 5, 0, 0, 0, 0,-10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    Reine_position_fin = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 10, 10, 5, 0, -5],
        [-5, 0, 5, 10, 10, 5, 0,-5],
        [-10, 0, 5, 5, 5, 5, 0,-10],
        [-10, 0, 0, 0, 0, 0, 0,-10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    Roi_position_debut = [
        [20, 30, 10, 0, 0, 10, 30, 20],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

    Roi_position_milieu = [
        [15, 25, 10, -5, -5, 10, 25, 15],
        [15, 15, -5, -10, -10, -5, 15, 15],
        [-10, -20, -20, -25, -25, -20, -20, -10],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30]
    ]

    Roi_position_fin = [
        [-50, -30, -30, -30, -30, -30, -30, -50],
        [-30, -30, 0, 0, 0, 0, -30, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-50, -40, -30, -20, -20, -30, -40, -50]
    ]

    if piece.piece_type == chess.PAWN:
        if phase == "debut":
            return valeurs[piece.piece_type] + Pion_position_debut[case//8][case%8]
        elif phase == "milieu":
            return valeurs[piece.piece_type] + Pion_position_milieu[case//8][case%8]
        else:
            return valeurs[piece.piece_type] + Pion_position_fin[case//8][case%8]
    elif piece.piece_type == chess.KNIGHT:
        if phase == "debut":
            return valeurs[piece.piece_type] + Cavalier_position_debut[case//8][case%8]
        elif phase == "milieu":
            return valeurs[piece.piece_type] + Cavalier_position_milieu[case//8][case%8]
        else:
            return valeurs[piece.piece_type] + Cavalier_position_fin[case//8][case%8]
    elif piece.piece_type == chess.BISHOP:
        if phase == "debut":
            return valeurs[piece.piece_type] + Fou_position_debut[case//8][case%8]
        elif phase == "milieu":
            return valeurs[piece.piece_type] + Fou_position_milieu[case//8][case%8]
        else:
            return valeurs[piece.piece_type] + Fou_position_fin[case//8][case%8]
    elif piece.piece_type == chess.ROOK:
        if phase == "debut":
            return valeurs[piece.piece_type] + Tour_position_debut[case//8][case%8]
        elif phase == "milieu":
            return valeurs[piece.piece_type] + Tour_position_milieu[case//8][case%8]
        else:
            return valeurs[piece.piece_type] + Tour_position_fin[case//8][case%8]
    elif piece.piece_type == chess.QUEEN:
        if phase == "debut":
            return valeurs[piece.piece_type] + Reine_position_debut[case//8][case%8]
        elif phase == "milieu":
            return valeurs[piece.piece_type] + Reine_position_milieu[case//8][case%8]
        else:
            return valeurs[piece.piece_type] + Reine_position_fin[case//8][case%8]
    elif piece.piece_type == chess.KING:
        if phase == "debut":
            return valeurs[piece.piece_type] + Roi_position_debut[case//8][case%8]
        elif phase == "milieu":
            return valeurs[piece.piece_type] + Roi_position_milieu[case//8][case%8]
        else:
            return valeurs[piece.piece_type] + Roi_position_fin[case//8][case%8] 
        #permet de retourner la valeur de  piece plus la valeur sur la case donnée avec la division classique pour la  ligne et le modulo pour la colonne
 
def phase_de_jeu(board):
    """Determiner la phase de jeu selon le materiel restant sur le plateau"""
    nb_pieces = len(board.piece_map())
    if nb_pieces >= 28:
        return "debut"
    elif 28 > nb_pieces >= 14:
        return "milieu"
    else:
        return "fin"

def evaluer_position(board):
    """Evaluer la position du plateau en fonction de la valeur des pieces et de leur position"""
    score = 0
    phase = phase_de_jeu(board)
    for case, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            score += score_minamax(piece, case, phase)
        if piece.color == chess.BLACK:
            score -= score_minamax(piece, chess.square_mirror(case), phase)
    return score

def minimax(board, depth, alpha, beta, maximizing):
    """Implémenter l'algorithme minimax avec alpha-beta pour évaluer les positions et trouver le meilleur coup"""
    if depth == 0 or board.is_game_over():
        return evaluer_position(board)
    if maximizing:
        max_eval = float('-inf')
        for each_move in board.legal_moves:
            board.push(each_move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for each_move in board.legal_moves:
            board.push(each_move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
        #pour plus d'explication lire README.md

def meilleur_coup(board, depth=4):
    """Retourner le meilleur coup calcule par minimax pour le camp dont c'est le tour"""
    best_move = None
    maximizing = board.turn == chess.WHITE
    best_value = float('-inf') if maximizing else float('inf')
    for move in board.legal_moves:
        board.push(move)
        move_value = minimax(board, depth - 1, float('-inf'), float('inf'), not maximizing)
        board.pop()
        if maximizing and move_value > best_value:
            best_value = move_value
            best_move = move
        elif not maximizing and move_value < best_value:
            best_value = move_value
            best_move = move
    return best_move
      
    
