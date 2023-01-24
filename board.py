from pieces import Piece, Pawn, Color, Location
from config import BOARD_SIZE, UNICODE_SQUARE

class Board:
    SIZE = BOARD_SIZE
    def __init__(self) -> None:
        self.board = [[None for _ in range(self.SIZE)] for __ in range(self.SIZE)]

    def place_new_piece(self, piece_type: type[Piece], color: Color, location: Location) -> Piece:
        new_pice = piece_type(color=color, location=location)
        self.board[location.i][location.j] = new_pice
        return new_pice

    def visualize(self) -> None:
        visual = ""
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                piece = self.board[i][j]
                is_black_square = (i%2==0)^(j%2==0)
                square = UNICODE_SQUARE[Color.BLACK.value] if is_black_square else UNICODE_SQUARE[Color.WHITE.value]
                visual += f" {piece} " if piece else f" {square} "
            visual += "\n"
        print(visual)