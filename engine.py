from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union

from config import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE
from engine_types import (DIAGONAL_DIRECTIONS, PARALLEL_DIRECTIONS, Color,
                          Direction, Location, MoveType, SlidingVariation)


class Piece(ABC):
    """
    Abstract class to subclass all the pieces from.
    """

    name: str = "PIECE"
    color: Color
    loc: Location
    has_moved: bool
    is_captured: bool

    def __init__(self, color: Color, location: Location) -> None:
        self.color = color
        self.loc = location
        self.has_moved = False
        self.is_captured = False

    def is_opponent(self, another_piece: Piece) -> bool:
        return another_piece.color is ~self.color

    @abstractmethod
    def generate_moves(self, board: Board) -> list[Move]:
        pass

    def __str__(self) -> str:
        return UNICODE_PIECES[self.name][self.color.name]

    def __repr__(self) -> str:
        return f"{str(self)}@{str(self.loc)}"


class Board:

    board: list[list[Optional[Piece]]]
    all_pieces: list[Piece]

    def __init__(self) -> None:
        self.board = [[None for _ in range(BOARD_SIZE)] for __ in range(BOARD_SIZE)]
        self.all_pieces = []

    def place_new(self, piece_type: type[Piece], color: Color, location: Location, is_ghost: bool = False) -> Piece:
        if not is_ghost and self[location] is not None:
            raise ValueError(f"Can't place {color} {piece_type} at {location}. {self[location]} already present there.")
        new_pice: Piece = piece_type(color=color, location=location)
        new_pice.is_captured = is_ghost
        self.all_pieces.append(new_pice)
        if not is_ghost:
            self[location] = new_pice
        return new_pice

    def execute_move(self, move: Move) -> None:
        match move.type:
            case MoveType.PASSING:
                self._move_piece(move.piece, move.destination)
            case MoveType.CAPTURE:
                assert move.target_piece is not None
                assert move.target_piece.loc == move.destination
                self._capture_piece(move.target_piece)
                self._move_piece(move.piece, move.destination)
            case MoveType.CASTLE:
                pass

    def generate_possible_moves(self, color: Color, ignore_check: bool = False) -> list[Move]:
        moves: list[Move] = []

        def is_uncaptured_piece_of_color(piece: Piece) -> bool:
            return piece.color is color and piece.is_captured is False

        for piece in filter(is_uncaptured_piece_of_color, self.all_pieces):
            for move in piece.generate_moves(self):
                if ignore_check or not self._seek_move(move).is_in_check(color):
                    moves.append(move)
        return moves

    def is_in_check(self, color: Color) -> bool:
        opponent_color = ~color
        opponent_moves = self.generate_possible_moves(opponent_color, ignore_check=True)
        for move in opponent_moves:
            if move.is_attacking_king():
                return True
        return False

    def is_in_checkmate(self, color: Color) -> bool:
        return self.is_in_check(color) and len(self.generate_possible_moves(color)) == 0

    def is_in_stalemate(self, color: Color) -> bool:
        return not self.is_in_check(color) and len(self.generate_possible_moves(color)) == 0

    def _seek_move(self, move: Move) -> Board:
        board_sought = self._generate_deepcopy()
        mirror_piece = board_sought[move.piece.loc]
        assert mirror_piece is not None
        move_copy = Move(
            mirror_piece,
            move.type,
            move.destination,
            board_sought[move.target_piece.loc] if move.target_piece else None
        )
        board_sought.execute_move(move_copy)
        return board_sought

    def _generate_deepcopy(self) -> Board:
        deep_copy = Board()
        for piece in (self.all_pieces):
            deep_copy.place_new(type(piece), piece.color, piece.loc, piece.is_captured)
        return deep_copy

    def _capture_piece(self, piece: Piece) -> None:
        self[piece.loc] = None
        piece.is_captured = True

    def _move_piece(self, piece: Piece, destination: Location) -> None:
        self[piece.loc] = None
        piece.loc = destination
        self[destination] = piece
        piece.has_moved = True

    def __str__(self) -> str:
        visual: str = ""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece: Optional[Piece] = self[Location(i, j)]
                square_color: Color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                square_repr: str = UNICODE_SQUARE[square_color.name]
                visual += f" {piece} " if piece else f" {square_repr} "
            visual += "\n"
        return visual

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, location: Location) -> Optional[Piece]:
        return self.board[location.i][location.j]

    def __setitem__(self, location: Location, piece: Optional[Piece]) -> None:
        self.board[location.i][location.j] = piece


class Move:
    """
    A class to represent a possible move for a given piece.

    piece: The piece that will make this move.
    type: The type of move. Passing, Capture or Castle.
    destination: The resulting location of the piece after the move is made.
    target_piece: The opponent piece being captured or the friendly rook in the case of castling.

    CASTLING: The move is only generated for the king. The rook is the target_piece.
        upon execution, both the pieces move.
    """

    piece: Piece
    type: MoveType
    destination: Location
    target_piece: Optional[Piece]

    def __init__(
        self, piece: Piece,
        type: MoveType,
        destination: Location,
        target_piece: Optional[Piece] = None
    ) -> None:
        if type in (MoveType.CAPTURE, MoveType.CASTLE) and target_piece is None:
            raise ValueError(f"Target piece not provided for {type.name} move")

        if type == MoveType.CAPTURE and target_piece and destination != target_piece.loc:
            raise ValueError(
                f"Target not at the destination. {destination} != {target_piece.loc}"
            )

        self.piece = piece
        self.type = type
        self.destination = destination
        self.target_piece = target_piece

    def is_attacking_king(self) -> bool:
        return type(self.target_piece) is King and self.type is MoveType.CAPTURE

    def __repr__(self) -> str:
        match self.type:
            case MoveType.PASSING:
                return f"{str(self.piece)}:{str(self.piece.loc)}->{str(self.destination)}"
            case MoveType.CAPTURE:
                return f"{str(self.piece)}:{str(self.piece.loc)}->{str(self.destination)}"\
                    f":>{str(self.target_piece)}<"
            case MoveType.CASTLE:
                return f"{str(self.piece)}:CASTLES:{'queenside' or 'kingside'}"


class SlidingPiece(Piece):
    """
    Mixin Class to generate moves for pieces that move in straight lines.
    Applicable Pieces: Rook, Bishop, Queen.
    """

    slidng_variation: SlidingVariation = SlidingVariation(0)
    sliding_step_limit: Union[int, float] = 0

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the sliding piece on the given board.
        """
        can_move_parallelly: bool = SlidingVariation.PARALLEL in self.slidng_variation
        can_move_diagonally: bool = SlidingVariation.DIAGONAL in self.slidng_variation
        directions = (
            (PARALLEL_DIRECTIONS if can_move_parallelly else [])
            + (DIAGONAL_DIRECTIONS if can_move_diagonally else [])
        )
        moves: list[Move] = []
        for direction in directions:
            step: int = 1
            while (
                step <= self.sliding_step_limit
                and (dest := self.loc.get_relative(direction.value, step))
                and dest.is_in_bounds()
            ):
                target: Union[Piece, None] = board[dest]
                if target is None:
                    step += 1
                    moves.append(Move(self, MoveType.PASSING, dest))
                elif self.is_opponent(target):
                    moves.append(Move(self, MoveType.CAPTURE, dest, target))
                    break
                elif not self.is_opponent(target):
                    break
        return moves


class Pawn(Piece):

    name = "PAWN"

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the pawn on the given board.
        """
        moves: list[Move] = []
        front: Direction = Direction.N if self.color == Color.WHITE else Direction.S
        front_left: Direction = Direction.NW if self.color == Color.WHITE else Direction.SE
        front_right: Direction = Direction.NE if self.color == Color.WHITE else Direction.SW
        one_ahead: Location = self.loc.get_relative(front.value)
        two_ahead: Location = self.loc.get_relative(front.value, 2)
        attacking_diagonals: tuple[Location, Location] = (
            self.loc.get_relative(front_left.value), self.loc.get_relative(front_right.value)
        )

        if one_ahead.is_in_bounds() and board[one_ahead] is None:
            moves.append(Move(self, MoveType.PASSING, one_ahead))
            if not self.has_moved and two_ahead.is_in_bounds() and board[two_ahead] is None:
                moves.append(Move(self, MoveType.PASSING, two_ahead))

        for dest in attacking_diagonals:
            if (
                dest.is_in_bounds()
                and (target := board[dest]) is not None
                and self.is_opponent(target)
            ):
                moves.append(Move(self, MoveType.CAPTURE, dest, target))

        return moves


class Knight(Piece):

    name = "KNIGHT"

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the knight on the given board.
        """
        moves: list[Move] = []
        for delta_i in [-2, -1, 1, 2]:
            for delta_j in [-2, -1, 1, 2]:
                if (
                    abs(delta_i) != abs(delta_j)
                    and (dest := self.loc.get_relative((delta_i, delta_j)))
                    and dest.is_in_bounds()
                ):
                    if (target := board[dest]) is None:
                        moves.append(Move(self, MoveType.PASSING, dest))
                    elif target.color != self.color:
                        moves.append(Move(self, MoveType.CAPTURE, dest, target))
        return moves


class Bishop(SlidingPiece):

    slidng_variation = SlidingVariation.DIAGONAL
    sliding_step_limit = float('inf')
    name = "BISHOP"


class Rook(SlidingPiece):

    slidng_variation = SlidingVariation.PARALLEL
    sliding_step_limit = float('inf')
    name = "ROOK"


class Queen(SlidingPiece):

    slidng_variation = SlidingVariation.PARALLEL | SlidingVariation.DIAGONAL
    sliding_step_limit = float('inf')
    name = "QUEEN"


class King(SlidingPiece):

    slidng_variation = SlidingVariation.PARALLEL | SlidingVariation.DIAGONAL
    sliding_step_limit = 1
    name: str = "KING"

    def generate_moves(self, board: Board) -> list[Move]:
        return super().generate_moves(board)

    def generate_castling_moves(self, board: Board) -> list[Move]:
        castling_moves: list[Move] = []

        def get_castling_space(rook: Rook) -> list[Location]:
            if rook.loc.j < self.loc.j:
                return [Location(self.loc.i, j) for j in range(rook.loc.j+1, self.loc.j)]
            else:
                return [Location(self.loc.i, j) for j in range(self.loc.j+1, rook.loc.j)]

        def is_eligible_rook_queenside(piece: Piece) -> bool:
            return (
                type(piece) is Rook
                and piece.color is self.color
                and piece.has_moved is False
                and piece.loc.j == 0
                and piece.loc.i == self.loc.i
                and all(board[space] is None for space in get_castling_space(piece))
            )

        def is_eligible_rook_kingside(piece: Piece) -> bool:
            return (
                type(piece) is Rook
                and piece.color is self.color
                and piece.has_moved is False
                and piece.loc.j == 7
                and piece.loc.i == self.loc.i
                and all(board[space] is None for space in get_castling_space(piece))
            )

        if (queenside_rook := next(filter(is_eligible_rook_queenside, board.all_pieces), None)):
            kings_path = [Location(self.loc.i, j) for j in range(self.loc.j-2, self.loc.j+1)]
            opponent_moves = board.generate_possible_moves(~self.color, ignore_check=True)
            if not any(opponent_move.destination in kings_path for opponent_move in opponent_moves):
                castling_moves.append(Move(self, MoveType.CASTLE, Location(self.loc.i, self.loc.j-2), queenside_rook))

        if (kingside_rook := next(filter(is_eligible_rook_kingside, board.all_pieces), None)):
            kings_path = [Location(self.loc.i, j) for j in range(self.loc.j, self.loc.j+3)]
            opponent_moves = board.generate_possible_moves(~self.color, ignore_check=True)
            if not any(opponent_move.destination in kings_path for opponent_move in opponent_moves):
                castling_moves.append(Move(self, MoveType.CASTLE, Location(self.loc.i, self.loc.j+2), kingside_rook))

        return castling_moves
