# type: ignore
"""
Profiling the engine
"""
import cProfile
import os
import pstats
import random
import subprocess

from dotenv import load_dotenv

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
                return "CHECKMATE"
            else:
                return "STALEMATE"
        move: Move = random.choice(moves)
        game.execute_move(move)
        game.active_color = ~game.active_color
    return f"EXHAUSTED {limit} Moves"

def run_games(count: int = GAME_COUNT, status = None) -> None:
    for _ in range(count):
        ret = random_game(PER_GAME_MOVE_LIMIT)
        if os.getenv("ENVIRONMENT") != "GITHUB":
            print(ret)
        if ret not in status:
            status[ret] = 0
        status[ret] += 1
    return status

def github_summary(stat: pstats.Stats, status: dict) -> None:
    github_markdown_line("Game Statuses:")
    for key, value in status.items():
        github_markdown_line(f"{key}: {value}")
    github_markdown_line("")
    github_markdown_line(f"Average Per Game Time: {stat.total_tt/GAME_COUNT}")


def github_markdown_line(line: str) -> None:
    subprocess.run(
        f"echo \"{line}\" >> $GITHUB_STEP_SUMMARY",
        shell=True,
        check=True
    )

if __name__ == "__main__":
    load_dotenv()
    profiler = cProfile.Profile()
    status = {}
    op = profiler.run("run_games(status=status)")
    stats = pstats.Stats(op)
    op.print_stats()
    print(f"AVERAGE PER GAME TIME: {stats.total_tt/GAME_COUNT}")
    print("GAME STATUS:")
    for key, value in status.items():
        print(f"{key}: {value}")
    if os.getenv("ENVIRONMENT") == "GITHUB":
        github_summary(stats, status)
