import numpy as np
import numpy.typing as npt

from engine.types import Color
from engine.board import Board

PARALLEL_MAP = np.array(
    [[1 if i==7 or j==7 else 0 for i in range (0,15)] for j in range(0,15)],
    dtype=bool
)
PARALLEL_MAP[7,7] = 0
DIAGONAL_MAP = np.eye(15, dtype=bool) | np.flip(np.eye(15, dtype=bool), axis=1)
DIAGONAL_MAP[7,7] = 0
COMBINED_MAP = PARALLEL_MAP | DIAGONAL_MAP

def get_mask(l: tuple[int, int], map: str) -> npt.NDArray[np.bool_]:
    if map.upper()[0] == "P":
        mask = PARALLEL_MAP[7-l[0]:15-l[0], 7-l[1]:15-l[1]]
    elif map.upper()[0] == "D":
        mask = DIAGONAL_MAP[7-l[0]:15-l[0], 7-l[1]:15-l[1]]
    elif map.upper()[0] == "C":
        mask = COMBINED_MAP[7-l[0]:15-l[0], 7-l[1]:15-l[1]]
    return np.array(mask, copy=True)

def apply_mask(board: Board, loc: tuple[int, int], map: str) -> npt.NDArray[np.int8]:
    mask = get_mask(loc, map)
    color = board[loc[0], loc[1], 0]
    opponent_color = (~Color(color)).value


    bump_mask = mask & (board.board[:, :, 3] == 1)
    bumps = np.argwhere(bump_mask)
    closest_bumps = {}
    for bump in bumps:
        slope = ((bump[0] - loc[0])//max(abs(bump[0] - loc[0]), 1), (bump[1] - loc[1])//max(abs(bump[1] - loc[1]), 1))
        if (
            ((old_bump := closest_bumps.get(slope)) is None)
            or abs(bump[0] - loc[0]) < abs(old_bump[0] - loc[0])
            or abs(bump[1] - loc[1]) < abs(old_bump[1] - loc[1])
        ):
            closest_bumps[slope] = bump

    for vector, start in closest_bumps.items():
        x = (start[0]+vector[0], start[1]+vector[1])
        while 0 <= x[0] < 8 and 0 <= x[1] < 8:
            mask[x] = 0
            bump_mask[x] = 0
            x = (x[0]+vector[0], x[1]+vector[1])

    slide = mask & (~bump_mask)
    hit = bump_mask & (board.board[:, :, 0] == opponent_color)
    return np.argwhere(hit), np.argwhere(slide)