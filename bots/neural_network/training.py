"""
Training script for the neural network bot.
"""

import random

from bots.neural_network.bot import NNBot
from engine import Game, from_fen


def evaluate_out_of_bounds(agent: NNBot) -> None:
    game_count = 100
    max_moves = 250
    game = Game()
    total_selected_moves = 0
    invalid_selected_moves = 0
    for _ in range(game_count):
        game.reset()
        from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
        for _ in range(max_moves):
            if not (moves := list(game.legal_moves())):
                break
            total_selected_moves += 1
            agent_move = agent.select_move(game.board, moves)
            if agent_move >= len(moves):
                invalid_selected_moves += 1
                agent_move = random.randint(0, len(moves)-1)
            game.execute_move(moves[agent_move])
    print(f"Out of {total_selected_moves} moves, {invalid_selected_moves} were invalid")


def train_out_of_bounds(agent: NNBot) -> None:
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    max_moves = 250
    for _ in range(max_moves):
        if not (moves := list(game.legal_moves())):
            break
        agent.train(game.board, moves, 0.1)
        agent_move = agent.select_move(game.board, moves)
        if agent_move >= len(moves):
            agent_move = random.randint(0, len(moves)-1)
        game.execute_move(moves[agent_move])


if __name__ == "__main__":
    nn_bot = NNBot([100, 100])
