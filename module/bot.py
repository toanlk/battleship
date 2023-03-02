import random
import numpy as np

class Bot:
    def __init__(self, boardWidth = 8, boardHeight = 20):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight

        # targets = []
        # potential_targets = []
        # self.SHOT_MAP = np.zeros([boardHeight, boardWidth])
        # self.SIMPLE_SHOT_MAP = []

        # self.SHIP_MAP = np.zeros([boardHeight, boardWidth])
        # # self.SHIP_INFO = {"Carrier": 5, "Battleship": 4, "Destroyer": 3, "Submarine": 3, "Patrol Boat": 2}
        # self.SHIP_INFO = {"Battleship": 4}
        # self.SHIP_COORDINATE_DICT = dict()
        # self.COORDINATE_SHIP_DICT = dict()
        # self.SUNK_SHIP_COORDINATES = []
        # self.PROB_MAP = np.zeros([boardHeight, boardWidth])
        
    # -----------------------------------------------------------------------------------------------------
    def guess_random(self, shot_map):
        while True:
            guess_row, guess_col = random.randint(0, (self.boardHeight - 1)), random.randint(0, (self.boardWidth - 1))

            if shot_map[guess_row, guess_col] == 0:
                break

        return guess_row, guess_col

    def target_hit(self, target_row, target_col, is_sunk, ship_hit, targets, potential_targets, shot_map):
        if is_sunk:
            targets = []
            potential_targets = []
        else:
            targets.append((target_row, target_col))
            potential_targets = [(target_row + 1, target_col), (target_row, target_col + 1),
                                (target_row - 1, target_col), (target_row, target_col - 1)]

            data = []
            for guess_row, guess_col in potential_targets:
                if (0 <= guess_row < self.boardHeight) and \
                        (0 <= guess_col < self.boardWidth) and \
                        (shot_map[guess_row][guess_col] == 0) and \
                        ((guess_row, guess_col) not in targets):
                    data.append((guess_row, guess_col))

            potential_targets = data

        return targets, potential_targets  

    def hunt_target(self, targets, potential_targets, shot_map):
        if targets and len(potential_targets) > 0:
            guess_row, guess_col = potential_targets.pop()
        else:
            guess_row, guess_col = self.guess_random(shot_map)
            
        return guess_row, guess_col, potential_targets