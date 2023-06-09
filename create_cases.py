from engine import Board
from engine_types import PieceType,Piece,Location,Color
import numpy as np

board = Board()
# BLACK_PIECES = [
#   board.place_new(Piece(Color.BLACK, PieceType.ROOK), Location(0, 0)),
#   board.place_new(Piece(Color.BLACK, PieceType.KNIGHT), Location(0, 1)),
#   board.place_new(Piece(Color.BLACK, PieceType.BISHOP), Location(0, 2)),
#   board.place_new(Piece(Color.BLACK, PieceType.QUEEN), Location(0, 3)),
#   board.place_new(Piece(Color.BLACK, PieceType.KING), Location(0, 4)),
#   board.place_new(Piece(Color.BLACK, PieceType.BISHOP), Location(0, 5)),
#   board.place_new(Piece(Color.BLACK, PieceType.KNIGHT), Location(0, 6)),
#   board.place_new(Piece(Color.BLACK, PieceType.ROOK), Location(0, 7)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 0)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 1)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 2)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 3)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 4)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 5)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 6)),
#   board.place_new(Piece(Color.BLACK, PieceType.PAWN), Location(1, 7)),
# ]
# WHITE_PIECES = [
#   board.place_new(Piece(Color.WHITE, PieceType.ROOK), Location(7, 0)),
#   board.place_new(Piece(Color.WHITE, PieceType.KNIGHT), Location(7, 1)),
#   board.place_new(Piece(Color.WHITE, PieceType.BISHOP), Location(7, 2)),
#   board.place_new(Piece(Color.WHITE, PieceType.QUEEN), Location(7, 3)),
#   board.place_new(Piece(Color.WHITE, PieceType.KING), Location(7, 4)),
#   board.place_new(Piece(Color.WHITE, PieceType.BISHOP), Location(7, 5)),
#   board.place_new(Piece(Color.WHITE, PieceType.KNIGHT), Location(7, 6)),
#   board.place_new(Piece(Color.WHITE, PieceType.ROOK), Location(7, 7)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 0)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 1)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 2)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 3)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 4)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 5)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 6)),
#   board.place_new(Piece(Color.WHITE, PieceType.PAWN), Location(6, 7)),
# ]
# a = board.board
# np.save("test_data",a,allow_pickle= True)

knight_list = [(0,0),(0,4),(3,4),(4,3)]
move_map = {
  (0, 0): [(1, 2), (2, 1)],
  (0, 4): [(1, 6), (1, 2), (2, 5), (2, 3)],
  (3, 4):[(1, 5), (1, 3), (2, 6), (2, 2), (4, 6), (4, 2), (5, 5), (5, 3)],
  (4, 3): [(2, 4), (2, 2), (3, 5), (3, 1), (5, 5), (5, 1), (6, 4), (6, 2)]
}
count = 0
for val in knight_list:
  count = count+1
  board = Board()
  board.set_square(location = Location(*val),piece= Piece(Color.WHITE,PieceType.KNIGHT))
  len_board = len(move_map[val])
  color_white = len_board/2
  for pos in move_map[val]:
    if color_white>0:
      board.set_square(location = Location(*move_map[val]),piece = Piece(Color.WHITE,PieceType.ROOK))
    else:
      board.set_square(location=Location(*move_map[val]), piece=Piece(Color.BLACK, PieceType.ROOK))
  a = board.board
  np.save(f"test_knight_{count}",a,allow_pickle=True)

bishop_list = [(0,0),(0,7),(3,4),(4,4)]
move_map = {
  (0, 0): [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)],
  (0, 7): [(1,6),(2,5),(3,4),(4,3),(5,2),(6,1,(7,0))],
  (3, 4): [(1,6),(2,5),(4,3),(5,2),(6,1),(7,0),(2,3),(1,2),(0,1),(4,5),(5,6),(6,7)],
  (4, 4): [(0,0),(1,1),(2,2),(3,3),(5,5),(6,6),(7,7),(5,3),(6,2),(7,1),(3,5),(2,6),(1,7)]
}

count = 0
for val in bishop_list:
  count = count + 1
  board = Board()
  board.set_square(location=Location(*val), piece=Piece(Color.WHITE, PieceType.BISHOP))
  len_board = len(move_map[val])
  color_white = len_board / 2
  for pos in move_map[val]:
    if color_white > 0:
      board.set_square(location=Location(*move_map[val]), piece=Piece(Color.WHITE, PieceType.ROOK))
    else:
      board.set_square(location=Location(*move_map[val]), piece=Piece(Color.BLACK, PieceType.ROOK))
  a = board.board
  np.save(f"test_bishop_{count}", a, allow_pickle=True)