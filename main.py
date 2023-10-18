"""
Entrypoint for manual tests
"""
from bots import MinMaxBot
from bots import RandomBot
from engine import Color, Game, from_fen, to_fen

if __name__ == "__main__":
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)

    mmb = MinMaxBot(max_depth=2, color=Color.BLACK)
    rb = RandomBot(color=Color.WHITE)

    while next(game.legal_moves(), False):
        if game.active_color == mmb.color:
            active_player = mmb
        else:
            active_player = rb
        selected_move = active_player.select_move(game)
        game.execute_move(selected_move)
        print(f"{active_player.name} played {selected_move}")
        print(game.board)

    if game.is_in_checkmate(game.active_color):
        print(f"{~game.active_color} wins by checkmate.")

    elif game.is_in_stalemate(game.active_color):
        print(f"{~game.active_color} draws by stalemate.")
    else:
        print("Something fucky happened.")
