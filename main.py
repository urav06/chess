"""
Entrypoint for manual tests
"""
import time

from bots import MinMaxBot, RandomBot, MinMaxProBot
from engine import Color, Game, from_fen, to_fen


def main():
    players = (
        MinMaxBot(max_depth=3, color=Color.BLACK),
        # MinMaxBot(max_depth=6, color=Color.WHITE),
        # RandomBot(color=Color.BLACK)
        MinMaxProBot(max_depth=2, color=Color.WHITE),
    )

    game = Game()
    # from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    from_fen('1n1qkbn1/r2pp1p1/b7/ppp5/4QP2/2P2Kp1/1P1P2B1/r7', game)
    # from_fen('rn1qkbnr/pb1ppppp/2p5/8/p4P2/2P5/1P1PP1PP/RNBQKBNR', game)
    # print("Game Started here is", game.board)
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
