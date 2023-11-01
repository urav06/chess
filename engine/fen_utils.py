"""
Utils to load and save FEN strings
"""
from engine.board import Board
from engine.constants import BOARD_SIZE, FEN_MAPPING, INV_FEN_MAPPING
from engine.game import Game
from engine.types import Color, Piece, BLACK, WHITE


def from_fen(fen_string: str, game: Game) -> None:
    fen_data: list[str] = fen_string.strip().split(sep=" ")

    if len(fen_data) == 1:
        placement_string: str = fen_data[0]
    elif len(fen_data) == 6:
        placement_string, active_color_data, _, _, _, _ = fen_data
        active_color: Color = BLACK if active_color_data.lower() == "b" else WHITE
        game.active_color = active_color

    placement_data: list[str] = placement_string.split("/")
    if len(placement_data) != BOARD_SIZE:
        raise ValueError(f"Invalid number of rows in the FEN string: {len(placement_data)}")

    game.board.clear()
    for i, rank_data in enumerate(placement_data):
        rank_repr = "".join(
            int(c)*"x" if c.isdigit() else c for c in rank_data
        )
        for j, square_data in enumerate(rank_repr):
            if square_data != "x":
                piece: Piece = FEN_MAPPING[square_data]
                game.board.place_piece((i, j), piece)


def to_fen(board: Board) -> str:
    placement_string = ""
    for i, rank in enumerate(board.board):
        empty_counter = 0
        for j in range(len(rank)):
            if board.board[i, j, 3]:
                piece: Piece = board.get_piece((i, j))
                square_data = INV_FEN_MAPPING[piece]
                if empty_counter != 0:
                    placement_string += f"{empty_counter}"
                    empty_counter = 0
                    placement_string += f"{square_data}"
                else:
                    placement_string += f"{square_data}"
            else:
                empty_counter += 1

        if empty_counter != 0:
            placement_string += f"{empty_counter}"
        placement_string += "/"
    placement_string = placement_string.strip("/")
    return placement_string
