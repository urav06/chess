"""
Engine Constants
"""
from engine.types import PieceType, Color, Piece

BOARD_SIZE = 8
UNICODE_PIECES = {
    PieceType.PAWN: {Color.BLACK: "◯", Color.WHITE: "●"},
    PieceType.KNIGHT: {Color.BLACK: "N", Color.WHITE: "❰N❱"},
    PieceType.BISHOP: {Color.BLACK: "B", Color.WHITE: "❰B❱"},
    PieceType.ROOK: {Color.BLACK: "R", Color.WHITE: "❰R❱"},
    PieceType.QUEEN: {Color.BLACK: "Q", Color.WHITE: "❰Q❱"},
    PieceType.KING: {Color.BLACK: "◺△◿", Color.WHITE: "◣▲◢"},
}
UNICODE_SQUARE = {Color.BLACK: "◼", Color.WHITE: "◻"}

FEN_MAPPING: dict[str, Piece] = {
    "p": Piece(Color.BLACK, PieceType.PAWN),
    "r": Piece(Color.BLACK, PieceType.ROOK),
    "n": Piece(Color.BLACK, PieceType.KNIGHT),
    "b": Piece(Color.BLACK, PieceType.BISHOP),
    "q": Piece(Color.BLACK, PieceType.QUEEN),
    "k": Piece(Color.BLACK, PieceType.KING),
    "P": Piece(Color.WHITE, PieceType.PAWN),
    "R": Piece(Color.WHITE, PieceType.ROOK),
    "N": Piece(Color.WHITE, PieceType.KNIGHT),
    "B": Piece(Color.WHITE, PieceType.BISHOP),
    "Q": Piece(Color.WHITE, PieceType.QUEEN),
    "K": Piece(Color.WHITE, PieceType.KING)
}
INV_FEN_MAPPING = {v: k for k, v in FEN_MAPPING.items()}

BOARD_DRAWING = """╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗
║▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░║
╟───┼───┼───┼───┼───┼───┼───┼───╢
║░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓║
╟───┼───┼───┼───┼───┼───┼───┼───╢
║▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░║
╟───┼───┼───┼───┼───┼───┼───┼───╢
║░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓║
╟───┼───┼───┼───┼───┼───┼───┼───╢
║▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░║
╟───┼───┼───┼───┼───┼───┼───┼───╢
║░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓║
╟───┼───┼───┼───┼───┼───┼───┼───╢
║▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░║
╟───┼───┼───┼───┼───┼───┼───┼───╢
║░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓│░░░│▓▓▓║
╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝"""