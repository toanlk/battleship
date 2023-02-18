import random
import numpy as np

class Bot:
    def __init__(self, boardWidth = 8, boardHeight = 20):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight

    # -----------------------------------------------------------------------------------------------------
    def guess_random(self, shot_map, length=None):
        while True:
            row = random.randint(0, 7)
            col = random.randint(0, 19)
            guess_row, guess_col = row, col
            # if length:
            #     if (guess_row + guess_col) % length != 0:
            #         continue
            # if self.SHOT_MAP[guess_row][guess_col] == 0:
            #     break
            if [guess_row, guess_col] not in shot_map:
                break

        return [guess_row, guess_col]