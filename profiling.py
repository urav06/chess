"""
Profiling the engine
"""
import random
import cProfile
import pstats

from engine import Game, Move
from engine.fen_utils import from_fen

PER_GAME_MOVE_LIMIT = 200
GAME_COUNT = 4

def random_game(limit: int = PER_GAME_MOVE_LIMIT) -> bool:
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    for _ in range(limit):
        moves = list(game.legal_moves())
        if not moves:
            if game.is_in_check(color=game.active_color):
                print("CHECKMATED")
            else:
                print("STALEMATED")
            return False
        move: Move = random.choice(moves)
        game.execute_move(move)
        game.active_color = ~ game.active_color
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
    