import random
import numpy as np

class Bot:
    def __init__(self, boardWidth = 8, boardHeight = 20, sessionID = None):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.sessionID = sessionID

        self.shot_map = np.zeros([inviteRequest['boardWidth'], inviteRequest['boardHeight']])
        self.simple_shot_map = []
        self.targets = []
        self.potential_targets = []

    # -----------------------------------------------------------------------------------------------------
    def guess_random(self, shot_map):
        while True:
            guess_row, guess_col = random.randint(0, (self.boardHeight - 1)), random.randint(0, (self.boardWidth - 1))

            if shot_map[guess_row, guess_col] == 0:
                break

        return guess_row, guess_col

    # -----------------------------------------------------------------------------------------------------
    def target_hit(self, target_row, target_col, is_sunk, ship_hit, targets, potential_targets, shot_map):
        if is_sunk:
            potential_targets = []

        targets.append((target_row, target_col))
        
        potential_targets = [(target_row + 1, target_col), (target_row, target_col + 1),
                    (target_row - 1, target_col), (target_row, target_col - 1)]

        # if len(targets) > 1:
        #     potential_targets = self.guest_target(targets, shot_map)
                            
        potential_targets = self.calculate_targets(potential_targets, targets, shot_map)

        return targets, potential_targets

    def target_miss(self, targets, potential_targets, shot_map):
        data = []
        potential_targets = []
        for target_row, target_col in targets:
            data = [(target_row + 1, target_col), (target_row, target_col + 1),
                        (target_row - 1, target_col), (target_row, target_col - 1)]
            potential_targets.extend(data)
        
        potential_targets = self.calculate_targets(potential_targets, targets, shot_map)

        return potential_targets

    def calculate_targets(self, potential_targets, targets, shot_map):
        data = []
        for guess_row, guess_col in potential_targets:
                if (0 <= guess_row < self.boardHeight) and \
                        (0 <= guess_col < self.boardWidth) and \
                        (shot_map[guess_row][guess_col] == 0) and \
                        ((guess_row, guess_col) not in targets):
                    data.append((guess_row, guess_col))
        return data

    # -----------------------------------------------------------------------------------------------------
    def hunt_target(self, targets, potential_targets, shot_map):
        if targets and len(potential_targets) > 0:
            guess_row, guess_col = potential_targets.pop()
            print("Target: " + str([guess_row, guess_col]))
        else:
            guess_row, guess_col = self.guess_random(shot_map)
            print("Hunt: " + str([guess_row, guess_col]))
            
        return guess_row, guess_col, potential_targets

    # -----------------------------------------------------------------------------------------------------
    def guest_target(self, targets, shot_map):
        # print('guest_target')
        y = targets[0][0]
        x = targets[0][1]

        max_size = (4 - len(targets)) + 1

        direction_x = ''
        direction_y = ''
        low_y = targets[0][0]
        high_y = targets[0][0]
        low_x = targets[0][1]
        high_x = targets[0][1]
        # print(str(targets))
        for pos in targets:
            # print("Pos: " + str(pos[1]))
            if pos[1] > x or pos[1] < x:
                direction_x = 'x'
            if pos[0] > y or pos[0] < y:
                direction_y = 'y'
            if pos[1] < low_x:
                low_x = pos[1]
            if pos[1] > high_x:
                high_x = pos[1]
            if pos[0] < low_y:
                low_y = pos[0]
            if pos[0] > high_y:
                high_y = pos[0]

        potential_targets = []
        if 'x' in direction_x:
            lst = []
            for i in range(1, max_size):
                new_x = high_x + i
                lst.append((y, new_x))
            lst.reverse()
            potential_targets.extend(lst)

            lst = []
            for i in range(1, max_size):
                new_x = low_x - i
                lst.append((y, new_x))
            lst.reverse()
            potential_targets.extend(lst)

        if 'y' in direction_y:
            lst = []
            for i in range(1, max_size):
                new_y = high_y + i
                lst.append((new_y, x))
            lst.reverse()
            potential_targets.extend(lst)

            lst = []
            for i in range(1, max_size):
                new_y = low_y - i
                lst.append((new_y, x))
            lst.reverse()
            potential_targets.extend(lst)

        potential_targets = self.calculate_targets(potential_targets, targets, shot_map)
        # print(potential_targets)
        return potential_targets