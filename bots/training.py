import random

from bots.agent import Agent
from engine import Game, from_fen


def evaluate_out_of_bounds(agent: Agent) -> None:
    GAME_COUNT = 100
    MAX_MOVES = 250
    game = Game()
    TOTAL_SELECTED_MOVES = 0
    INVALID_SELECTED_MOVES = 0
    for _ in range(GAME_COUNT):
        game.reset()
        from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
        for _ in range(MAX_MOVES):
            if not (moves := list(game.legal_moves())):
                break
            TOTAL_SELECTED_MOVES += 1
            agent_move = agent.select_move(game.board, moves)
            if agent_move >= len(moves):
                INVALID_SELECTED_MOVES += 1
                agent_move = random.randint(0, len(moves)-1)
            game.execute_move(moves[agent_move])
            game.active_color = ~game.active_color
    print(f"Out of {TOTAL_SELECTED_MOVES} moves, {INVALID_SELECTED_MOVES} were invalid")


def train_out_of_bounds(agent: Agent) -> None:
    game = Game()
    from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", game)
    MAX_MOVES = 250
    for _ in range(MAX_MOVES):
        if not (moves := list(game.legal_moves())):
            break
        agent.train(game.board, moves, 0.1)
        agent_move = agent.select_move(game.board, moves)
        if agent_move >= len(moves):
            agent_move = random.randint(0, len(moves)-1)
        game.execute_move(moves[agent_move])
        game.active_color = ~game.active_color


if __name__ == "__main__":
    agent = Agent([100, 100])
