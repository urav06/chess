from pieces import Pawn, Color, Location
from config import BOARD_SIZE, UNICODE_SQUARE

class Board:
    SIZE = BOARD_SIZE
    def __init__(self) -> None:
        self.board = [[None for _ in range(self.SIZE)] for __ in range(self.SIZE)]

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

if __name__ == "__main__":
    board = Board()
    board.board[1][0] = Pawn(Color.BLACK, Location(1, 0))
    board.visualize()