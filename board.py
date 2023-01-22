from pieces import Pawn, Color, Location
from config import BOARD_SIZE

class Board:
    SIZE = BOARD_SIZE
    def __init__(self) -> None:
        self.board = [[None for _ in range(self.SIZE)] for __ in range(self.SIZE)]

    def visualize(self) -> None:
        visual = ""
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                piece = self.board[i][j]
                visual += f"{piece} " if piece else " _ "
            visual += "\n"
        print(visual)

if __name__ == "__main__":
    board = Board()
    board.board[1][0] = Pawn(Color.BLACK, Location(1, 0))
    board.visualize()