from board import Board
from pieces import Queen, Pawn, Bishop, Color, Location

if __name__ == "__main__":
    board = Board()
    some_bishop = Bishop(Color.BLACK, location=Location(1,0))
    board.board[1][0] = some_bishop
    some_queen = Queen(Color.BLACK, location=Location(1,1))
    board.board[1][1] = some_queen
    some_pawn = Pawn(Color.BLACK, location=Location(4,0))
    board.board[4][0] = some_pawn

    
    print(some_queen.generate_moves(board))
    board.visualize()