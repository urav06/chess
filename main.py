from engine import Board, Piece, Pawn, Knight, Bishop, Rook, Queen, King
from engine_types import Location, Color
from typing import Dict

from config import BOARD_SIZE

FEN_MAPPING: Dict[str, tuple[Color, type[Piece]]] = dict(
        p=(Color.BLACK, Pawn),
        r=(Color.BLACK, Rook),
        n=(Color.BLACK, Knight),
        b=(Color.BLACK, Bishop),
        q=(Color.BLACK, Queen),
        k=(Color.BLACK, King),
        P=(Color.WHITE, Pawn),
        R=(Color.WHITE, Rook),
        N=(Color.WHITE, Knight),
        B=(Color.WHITE, Bishop),
        Q=(Color.WHITE, Queen),
        K=(Color.WHITE, King)
    )


def fill_rank(board: Board, rank: int, rank_repr: str) -> None:
    for j in range(0, BOARD_SIZE):
        if rank_repr[j] != "x":
            color = FEN_MAPPING[rank_repr[j]][0]
            piece_type = FEN_MAPPING[rank_repr[j]][1]
            board.place_new(piece_type, color, Location(rank, j))


def from_fen(board: Board, fen_data: str) -> None:
    placement_data = fen_data.split(sep=" ")[0].split(sep="/")
    for rank_num, rank_data in enumerate(placement_data):
        rank_repr = "".join(int(c)*"x" if c.isdigit() else c for c in rank_data)
        fill_rank(board, rank_num, rank_repr)


def classic_setup(board: Board) -> None:
    from_fen(board, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")


if __name__ == "__main__":
    board = Board()
    from_fen(board, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    print(board)
