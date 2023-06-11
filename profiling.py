from engine import Board, Color
from main import classic_setup
import random
import cProfile
import pstats

PER_GAME_MOVE_LIMIT = 200
GAME_COUNT = 40


def random_game(limit: int = PER_GAME_MOVE_LIMIT) -> bool:
    board = Board()
    classic_setup(board)
    for turn in range(limit):
        to_play: Color = Color.WHITE if turn % 2 == 0 else Color.BLACK
        player_moves = board.generate_possible_moves(to_play)
        if not player_moves:
            if board.is_in_check(to_play):
                print(f"{to_play} CHECKMATED")
                return False
            else:
                print(f"{to_play} STALEMATED")
                return False
        move = random.choice(player_moves)
        board.execute_move(move)
    print(f"{limit} MOVES EXHAUSTED")
    return True


def run_games(count: int = GAME_COUNT) -> None:
    for _ in range(count):
        random_game(PER_GAME_MOVE_LIMIT)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    op = profiler.run("run_games(GAME_COUNT)")
    stats = pstats.Stats(op)
    op.print_stats()
    print(f"AVERAGE PER GAME TIME: {stats.total_tt/GAME_COUNT}")
