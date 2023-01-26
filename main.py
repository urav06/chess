from engine import Board, Queen, Color, Location, Move, MoveType

if __name__ == "__main__":
    board = Board()
    some_queen = board.place_new_piece(Queen, Color.BLACK, Location(1, 0))
    board.visualize()
