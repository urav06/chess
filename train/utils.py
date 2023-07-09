import numpy as np
import numpy.typing as npt

from engine import Move, Board
from engine.types import (
    PASSING, CAPTURE, CASTLE, PROMOTION, CAPTURE_AND_PROMOTION
)


def vectorize_move(move: Move) -> npt.NDArray[np.int8]:
    if move.type is PASSING:
        return np.array([move[0], move[1], [PASSING, 0]])
    elif move.type is CAPTURE:
        return np.array([move[0], move[1], [CAPTURE, move.target]])
    elif move.type is CASTLE:
        return np.array([move[0], move[1], [CASTLE, move.castle_type]])
    elif move.type is PROMOTION:
        return np.array([move[0], move[1], [PROMOTION, move.promotion_rank]])
    elif move.type is CAPTURE_AND_PROMOTION:
        return np.array([move[0], move[1], [CAPTURE_AND_PROMOTION, move.promotion_rank]])
    else:
        raise ValueError(f"Invalid move type: {move.type}")


def generate_input_vector(board: Board, moves: list[Move], length: int) -> npt.NDArray[np.int8]:
    return np.concatenate((
        board.board.reshape(-1),
        np.array(list(map(vectorize_move, moves))).reshape(-1),
        np.full((length - 256 - (len(moves)*6)), -1),
    )).reshape(length, 1)