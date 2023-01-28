from engine import Board, Piece, Pawn, Knight, Bishop, Rook, Queen, King
from engine_types import Location, Color
from typing import Dict

from config import BOARD_SIZE


def _fill_row(board: Board, rank: int, color: Color, row: str) -> list[Piece]:
    assert len(row) == BOARD_SIZE
    pieces: list[Piece] = []
    row = row.lower()
    mapping: Dict[str, type[Piece]] = dict(
        p=Pawn, r=Rook, n=Knight, b=Bishop, q=Queen, k=King
    )
    for j in range(0, BOARD_SIZE):
        piece = board.place_new(mapping[row[j]], color, Location(rank, j))
        pieces.append(piece)
    return pieces


def classic_setup(board: Board) -> tuple[list[Piece], list[Piece]]:
    # BLACK SETUP
    black_pieces = []
    black_pieces += _fill_row(board, 0, Color.BLACK, "rnbqkbnr")
    black_pieces += _fill_row(board, 1, Color.BLACK, "pppppppp")

    # WHITE SETUP
    white_pieces = []
    white_pieces += _fill_row(board, 7, Color.WHITE, "rnbqkbnr")
    white_pieces += _fill_row(board, 6, Color.WHITE, "pppppppp")

    return (black_pieces, white_pieces)

if __name__ == "__main__":
    board = Board()
    classic_setup(board)
    print(board)
