# type: ignore
"""
Profiling the engine
"""
import cProfile
import os
import time
import pstats
import random

from dotenv import load_dotenv

from engine import Game, Move
from engine.fen_utils import from_fen
from github_action_utils import GithubActionUtils as gau

load_dotenv()
PER_GAME_MOVE_LIMIT = 250
GAME_COUNT = int(os.getenv("WORKFLOW_INPUT") or os.getenv("PROFILER_GAME_COUNT", "50"))


def random_game() -> bool:
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    for _ in range(PER_GAME_MOVE_LIMIT):
        moves = list(game.legal_moves())
        if not moves:
            if game.is_in_check(color=game.active_color):
                return "Checkmate"
            return "Stalemate"
        move: Move = random.choice(moves)
        game.execute_move(move)
    return f"Exhausted {PER_GAME_MOVE_LIMIT} Moves"


def run_games(raw: bool = False) -> None:
    results = {}
    for _ in range(GAME_COUNT):
        ret = random_game()
        if os.getenv("ENVIRONMENT") != "GITHUB" and not raw:
            print(ret)
        if ret not in results:
            results[ret] = 0
        results[ret] += 1
    return results


def run_profiler() -> None:
    profiler = cProfile.Profile()
    profiler_games_results = profiler.runcall(run_games)
    stats = pstats.Stats(profiler)
    # Run raw games without profiler to get a baseline
    start = time.time()
    run_games(raw=True)
    raw_elapsed = time.time() - start
    stats.print_stats()
    summary(stats, profiler_games_results, raw_elapsed)


def summary(stat: pstats.Stats, status: dict, raw_time: float) -> None:
    if os.getenv("ENVIRONMENT") == "GITHUB":
        gau.markdown_line(f"### Profiled {sum(status.values())} Random Games ###")
        gau.tabulate(["Status", "Count"], [[key, value] for key, value in status.items()])
        gau.markdown_line("")
        gau.markdown_line(f"Average Per Game Time: {round(stat.total_tt/GAME_COUNT, 5)} s.")
        gau.markdown_line(f"Average Per Game Time (Raw): {round(raw_time/GAME_COUNT, 5)} s.")
    else:
        print("GAME STATUS:")
        for key, value in status.items():
            print(f"{key}: {value}")
        print(f"AVERAGE PER GAME TIME: {stat.total_tt/GAME_COUNT}")
        print(f"AVERAGE PER GAME TIME (RAW): {raw_time/GAME_COUNT}")


if __name__ == "__main__":
    run_profiler()
