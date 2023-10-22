"""
Entrypoint for manual tests
"""
import time
from bots import MinMaxBot
from bots import RandomBot
from engine import Color, Game, from_fen

if __name__ == "__main__":
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)

    mmb = MinMaxBot(max_depth=3, color=Color.BLACK)
    rb = RandomBot(color=Color.WHITE)

    players = (mmb, rb)

    while next(game.legal_moves(), False):
        if game.active_color == players[0].color:
            active_player = players[0]
        else:
            active_player = players[1]
        st = time.time()
        selected_move = active_player.select_move(game)
        et = time.time()
        active_player.total_time += et-st
        game.execute_move(selected_move)
        print(f"{active_player.name} played {selected_move}")
        print(game.board)

    if game.is_in_checkmate(game.active_color):
        print(f"{~game.active_color} wins by checkmate.")

    elif game.is_in_stalemate(game.active_color):
        print(f"{~game.active_color} draws by stalemate.")
    else:
        print("Something fucky happened.")

    players[0].display_time_taken()
    players[1].display_time_taken()
