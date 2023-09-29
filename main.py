"""
Entrypoint for manual tests
"""
from bots import MinMaxBot
from bots import RandomBot
from engine import Color, Game, from_fen

if __name__ == "__main__":
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    print(game.board)

    mmb = MinMaxBot(max_depth=5, color=Color.BLACK)
    rb = RandomBot(color=Color.WHITE)

    while (moves := game.legal_moves()):
        if game.active_color == Color.BLACK:
            selected_move = mmb.select_move(game)
        else:
            selected_move = rb.select_move(game)
        game.execute_move(selected_move)
        print(f"{game.active_color} playd {selected_move}")
        print(game.board)
        game.active_color = ~game.active_color

    if game.is_in_checkmate(game.active_color):
        print(f"{~game.active_color} wins by checkmate.")
    
    elif game.is_in_stalemate(game.active_color):
        print(f"{~game.active_color} draws by stalemate.")
    else:
        print("Something fucky happened.")

