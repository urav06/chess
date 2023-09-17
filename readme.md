# Chess Engine & Bots

This repository contains a chess engine written in Python. Adding tools to train bots to play chess is a work in progress.

## Engine

The Chess Engine provides the following features:
- Physics of the chess board
- Legal move generation for all pieces.
- Check, checkmate, stalemate detection.
- The basic chess rules such as castling and pawn promotion are included.
- The chess rules not included yet are: en passant, 50 move rule, 3-fold repetition.

### Pre-requisites
 - Python 3.10 or higher.
 - numpy and other packages listed in requirements.txt


### Usage

A chess game can be initialized as follows:

```python
from engine import Game

game = Game()
print(game.board)
"""
◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
"""
```