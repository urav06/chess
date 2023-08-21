from engine.game import Game
from engine.fen_utils import to_fen, from_fen
from engine.types import (Color, WHITE, BLACK, KING, ROOK,
    PAWN, BISHOP, KNIGHT, QUEEN,
    Location, Move, MoveType, Piece, PieceType)


# This function computes the number of possible moves for a given layer
def compute_layer(game, layer):
    all_moves = game.legal_moves(color=Color.WHITE, pieces=(Piece(WHITE, KING), Location(7, 4)))
    count = 0
    for move in all_moves:
        game.execute_move(move)
        if layer == 1:
            count = count+1
            continue
        else:
            count = count+compute_layer(game, layer-1)
    return count


def initialize_game():
    new_game = Game()
    new_game.reset()
    # from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", new_game)
    from_fen("3rkr2/3ppp2/8/8/8/8/3PPP2/4K3", new_game)
    output = compute_layer(new_game, 2)
    print("Output is", output)


if __name__ == "__main__":
    initialize_game()
