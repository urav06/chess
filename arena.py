"""
Entrypoint for manual tests using the external chess library
"""
import time

import chess
from bots import MinMaxBot, RandomBot,MinMaxProBot


def main() -> None:
    board = chess.Board()
    players = (
        MinMaxBot(max_depth=3, color=chess.BLACK, name="phunsukh-wangdu"),
        MinMaxProBot(max_depth=3, color=chess.WHITE, name="yash-baheti")
    )
    while not board.is_game_over():
        active_player = players[0] if board.turn == players[0].color else players[1]
        st = time.time()
        selected_move: chess.Move = active_player.select_move(board)
        active_player.clock += time.time() - st
        board.push(selected_move)
        print(f"{active_player.name} played {selected_move}")
        print(board)
    else:
        outcome: chess.Outcome = board.outcome()
        if outcome.winner is not None:
            winning_player = players[0] if players[0].color is outcome.winner else players[1]
            print(f"{winning_player.name} won by {outcome.termination} in {board.fullmove_number} moves")
        else:
            print( f"Match ended with a draw due to {outcome.termination} in {board.fullmove_number} moves")

    players[0].display_time_taken()
    players[1].display_time_taken()

if __name__ == "__main__":
    main()