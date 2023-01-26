from engine import Board,Color,Move,Location,Queen,Knight,Rook,Bishop,King,Pawn

if __name__ == "__main__":
    board = Board()
    BLACK_PIECES=[
    board.place_new_piece(Rook,Color.BLACK,(0,0)),
    board.place_new_piece(Knight,Color.BLACK,(0,1)),
    board.place_new_piece(Bishop,Color.BLACK,(0,2)),
    board.place_new_piece(Queen,Color.BLACK,(0,3)),
    board.place_new_piece(King,Color.BLACK,(0,4)),
    board.place_new_piece(Bishop,Color.BLACK,(0,5)),
    board.place_new_piece(Knight,Color.BLACK,(0,6)),
    board.place_new_piece(Rook,Color.BLACK,(0,7)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,0)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,1)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,2)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,3)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,4)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,5)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,6)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,7)),
    ]
    WHITE_PIECES=[
    # board.place_new_piece(Rook,Color.WHITE,(2,1)),
    # board.place_new_piece(Knight,Color.WHITE,(2,2)),
    # board.place_new_piece(Bishop,Color.WHITE,(2,3)),
    # board.place_new_piece(Queen,Color.WHITE,(2,4)),
    # board.place_new_piece(King,Color.WHITE,(1,4)),
    # board.place_new_piece(Bishop,Color.WHITE,(2,5)),
    # board.place_new_piece(Knight,Color.WHITE,(2,6)),
    # board.place_new_piece(Rook,Color.WHITE,(2,7)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,0)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,1)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,2)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,3)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,4)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,5)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,6)),
    # board.place_new_piece(Pawn,Color.BLACK,(1,7)),
    ]
    board.visualize()
    current_position =4
    output= BLACK_PIECES[current_position].generate_moves(board)
    check_attacks = BLACK_PIECES[current_position].ATTACKS
    print(output)
    print("Attack from ",{BLACK_PIECES[current_position].name},check_attacks)
