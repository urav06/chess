"""
Entrypoint for manual tests
"""
import time

from bots import MinMaxBot,MinMaxProBot
from engine import Color, Game, from_fen


def main() -> None:
    players = (
        MinMaxBot(max_depth=2, color=Color.BLACK),
        # MinMaxBot(max_depth=6, color=Color.WHITE),
        # RandomBot(color=Color.BLACK)
        MinMaxProBot(max_depth=2, color=Color.WHITE),
    )

    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    while next(game.legal_moves(), False):
        active_player = (
            players[0] if game.active_color == players[0].color else players[1]
        )
        st = time.time()
        selected_move = active_player.select_move(game)
        et = time.time()
        active_player.move_count += 1
        active_player.clock += et - st
        game.execute_move(selected_move)
        print(f"{active_player.name} played {selected_move}")
        print(game.board)

    inactive_player = (
        players[1] if game.active_color == players[0].color else players[0]
    )
    if game.is_in_checkmate(game.active_color):
        print(
            f"{inactive_player.name} wins by checkmate in {inactive_player.move_count} moves."
        )

    elif game.is_in_stalemate(game.active_color):
        print(
            f"{inactive_player.name} draws by stalemate in {inactive_player.move_count} moves."
        )
    else:
        print("Something fucky happened.")

    players[0].display_time_taken()
    players[1].display_time_taken()


if __name__ == "__main__":
    main()
