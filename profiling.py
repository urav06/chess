# type: ignore
"""
Profiling the engine
"""
import cProfile
import os
import pstats
import random

from dotenv import load_dotenv

from engine import Game, Move
from engine.fen_utils import from_fen
from github_action_utils import GithubActionUtils as gau

PER_GAME_MOVE_LIMIT = 200
GAME_COUNT = 25

def random_game(limit: int = PER_GAME_MOVE_LIMIT) -> bool:
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    for _ in range(limit):
        moves = list(game.legal_moves())
        if not moves:
            if game.is_in_check(color=game.active_color):
                return "CHECKMATE"
            return "STALEMATE"
        move: Move = random.choice(moves)
        game.execute_move(move)
        game.active_color = ~game.active_color
    return f"EXHAUSTED {limit} Moves"

def run_games(count: int = GAME_COUNT, game_results = None) -> None:
    for _ in range(count):
        ret = random_game(PER_GAME_MOVE_LIMIT)
        if os.getenv("ENVIRONMENT") != "GITHUB":
            print(ret)
        if ret not in game_results:
            game_results[ret] = 0
        game_results[ret] += 1
    return game_results

def run_profiler() -> None:
    profiler = cProfile.Profile()
    game_results = {}
    output = profiler.run("run_games(game_results=game_results)")
    stats = pstats.Stats(output)
    stats.print_stats()
    summary(stats, game_results)

def summary(stat: pstats.Stats, status: dict) -> None:
    if os.getenv("ENVIRONMENT") == "GITHUB":
        gau.markdown_line("### Game Statuses ###")
        gau.tabulate(["Status", "Count"], [[key, value] for key, value in status.items()])
        gau.markdown_line("")
        gau.markdown_line(f"Average Per Game Time: {stat.total_tt/GAME_COUNT}")
    else:
        print("GAME STATUS:")
        for key, value in status.items():
            print(f"{key}: {value}")
        print(f"AVERAGE PER GAME TIME: {stat.total_tt/GAME_COUNT}")


if __name__ == "__main__":
    load_dotenv()
    run_profiler()
