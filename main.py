"""
Entrypoint for manual tests
"""
from engine import Game, from_fen

if __name__ == "__main__":
    game = Game()
    from_fen("7k/N5pp/8/8/2R1r3/8/8/4K3", game)
    print(game.board)
