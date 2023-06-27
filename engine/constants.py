"""
Engine Constants
"""
from engine.types import PieceType, Color

BOARD_SIZE = 8
UNICODE_PIECES = {
    PieceType.PAWN: {Color.BLACK: "♟︎", Color.WHITE: "♙"},
    PieceType.KNIGHT: {Color.BLACK: "♞", Color.WHITE: "♘"},
    PieceType.BISHOP: {Color.BLACK: "♝", Color.WHITE: "♗"},
    PieceType.ROOK: {Color.BLACK: "♜", Color.WHITE: "♖"},
    PieceType.QUEEN: {Color.BLACK: "♛", Color.WHITE: "♕"},
    PieceType.KING: {Color.BLACK: "♚", Color.WHITE: "♔"},
}
UNICODE_SQUARE = {Color.BLACK: "◼", Color.WHITE: "◻"}
