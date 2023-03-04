import random
import json
import numpy as np

class Bot:
    def __init__(self, boardWidth = 8, boardHeight = 20, sessionID = None, data = None):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.sessionID = sessionID

        self.SHOT_MAP = np.zeros([self.boardHeight, self.boardWidth])
        self.SIMPLE_SHOT_MAP = []

        self.TARGETS = []
        self.POTENTIAL_TARGETS = []

        data['shot_map'] = self.SHOT_MAP.tolist()
        data['simple_shot_map'] = self.SIMPLE_SHOT_MAP
        data['targets'] = self.TARGETS
        data['potential_targets'] = self.POTENTIAL_TARGETS
        self.save_file(self.sessionID, data)

    # -----------------------------------------------------------------------------------------------------
    def read_file(self, session_id):
        data =[]
        with open("cache/" + session_id + ".json", 'r') as file:
            data = json.load(file)
        return data

    def save_file(self, session_id, data):
        with open("cache/" + session_id + ".json", "w") as outfile:
            outfile.write(data)

    def shoot(self, session_id, data, max_shots):

        # targets = []
        # if 'targets' in json_object:
        #     targets = json_object['targets']

        # potential_targets = []
        # if 'potential_targets' in json_object:
        #     potential_targets = json_object['potential_targets']

        # shot_map = np.zeros([json_object['boardWidth'], json_object['boardHeight']])
        # if 'shot_map' in json_object:
        #     shot_map = np.array(json_object['shot_map'])

        # simple_shot_map = []
        # if 'simple_shot_map' in json_object:
        #     simple_shot_map = json_object['simple_shot_map']

        json_object = self.read_file(session_id)

        fire_position = []
        for i in range(0, max_shots):
            guess_row, guess_col, self.POTENTIAL_TARGETS = self.hunt_target(self.TARGETS, self.POTENTIAL_TARGETS, self.SHOT_MAP)
            fire_position.append([guess_row, guess_col])

            self.SHOT_MAP[guess_row][guess_col] = 1
            self.SIMPLE_SHOT_MAP.append([guess_row, guess_col])

        # json_object['simple_shot_map'] = self.SIMPLE_SHOT_MAP
        # json_object['shot_map'] = self.SHOT_MAP.tolist()
        # json_object['targets'] = self.TARGETS
        # json_object['potential_targets'] = self.POTENTIAL_TARGETS

        # self.save_file(session_id, json.dumps(json_object))

        return fire_position

    def notify(self, session_id, data):
        json_object = self.read_file(session_id)

        shot_map = np.array(json_object['shot_map'])
        targets = np.array(json_object['targets'])
        potential_targets = json_object['potential_targets']
     
        if data['shots']['status'] == "HIT":
            is_sunk = False
            if len(data['sunkShips']) > 0:
                is_sunk = True
            
            guess_row = data['shots']['coordinate'][0]
            guess_col = data['shots']['coordinate'][1]
            
            self.TARGETS, self.POTENTIAL_TARGETS = BOT.target_hit(guess_row, guess_col, is_sunk, data['sunkShips']['coordinates'], self.TARGETS, self.POTENTIAL_TARGETS, self.SHOT_MAP)
        elif data['shots']['status'] == "MISS":
            self.POTENTIAL_TARGETS = BOT.target_miss(self.TARGETS, self.POTENTIAL_TARGETS, self.SHOT_MAP)

        json_object['targets'] = self.TARGETS
        json_object['potential_targets'] = self.POTENTIAL_TARGETS
        self.save_file(session_id, json.dumps(json_object))

    def game_over(self, session_id, data):
        self.save_file(session_id + "_game_over", json.dumps(data))

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