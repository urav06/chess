from typing import Dict

from config import BOARD_SIZE
from engine import Bishop, Board, King, Knight, Pawn, Piece, Queen, Rook
from engine_types import Color, Location

FEN_MAPPING: Dict[str, tuple[Color, type[Piece]]] = {
    "p": (Color.BLACK, Pawn),
    "r": (Color.BLACK, Rook),
    "n": (Color.BLACK, Knight),
    "b": (Color.BLACK, Bishop),
    "q": (Color.BLACK, Queen),
    "k": (Color.BLACK, King),
    "P": (Color.WHITE, Pawn),
    "R": (Color.WHITE, Rook),
    "N": (Color.WHITE, Knight),
    "B": (Color.WHITE, Bishop),
    "Q": (Color.WHITE, Queen),
    "K": (Color.WHITE, King)
}

INV_FEN_MAPPING = {v: k for k, v in FEN_MAPPING.items()}


def from_fen(board: Board, fen_string: str) -> None:
    fen_data = fen_string.strip().split(sep=" ")

    if len(fen_data) == 1:
        placement_string = fen_data[0]
    elif len(fen_data) == 6:
        placement_string, color_data, _, _, _, _ = fen_data
        active_color = Color.BLACK if color_data.lower() == "b" else Color.WHITE
        board.active_color = active_color

    placement_data = placement_string.split("/")
    if len(placement_data) != BOARD_SIZE:
        raise ValueError("FEN Notation Error")

    for i, rank_data in enumerate(placement_data):
        rank_repr = "".join(int(c)*"x" if c.isdigit() else c for c in rank_data)
        for j, square_data in enumerate(rank_repr):
            if square_data != "x":
                color, piece_type = FEN_MAPPING[square_data]
                board.place_new(piece_type, color, Location(i, j))


def to_fen(board: Board) -> str:
    placement_string = ""
    for rank in board.board:
        empty_counter = 0
        for square in rank:
            if square is None:
                empty_counter += 1
            else:
                piece = square
                data = INV_FEN_MAPPING[(piece.color, type(piece))]
                if empty_counter != 0:
                    placement_string += f"{empty_counter}"
                    empty_counter = 0
                    placement_string += f"{data}"
                else:
                    placement_string += f"{data}"
        if empty_counter != 0:
            placement_string += f"{empty_counter}"
        placement_string += "/"
    placement_string = placement_string.strip("/")
    return placement_string
