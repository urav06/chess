from board import Board
from pieces import Queen, Pawn, Bishop, Color, Location

if __name__ == "__main__":
    board = Board()
    board.place_new_piece(Bishop, Color.BLACK, Location(1,0))
    some_queen = board.place_new_piece(Queen, Color.WHITE, Location(1,1))
    some_pawn = board.place_new_piece(Pawn, Color.BLACK, Location(4,0))

    
    print(some_queen.generate_moves(board))
    board.visualize()