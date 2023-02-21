import json
import random

class Position:
    
    def __init__(self, ships):
        self.ships = ships
        self.ship_type = {
            "CV": 4, # Carrier
            "BB": 4, # Battleship
            "OR": 2, # Oil rig
            "CA": 3, # Cruiser
            "DD": 2, # Destroyer
        }
        self.positions = []
        self.all_position = []

    # -----------------------------------------------------------------------------------------------------
    def generate(self):
        for ship in self.ships:
            for i in range(0, ship['quantity']):
                # print(ship['type'] + ': ' + str(ship['quantity']))
                position = self.generate_position(ship['type'])
                self.positions.append({'coordinates': position, 'type': ship['type']})
                self.all_position.extend(position)

        return self.positions

    # -----------------------------------------------------------------------------------------------------
    def generate_position(self, ship_type):
        positions = []
        is_exist = False
        size = self.ship_type.get(ship_type, [])
        
        while not is_exist:
            positions = self.generate_position_randomly(size, ship_type)
            print(ship_type + ": " + str(positions))
            if not self.is_ship_exist(positions):
                is_exist = True
            else:
                continue

        return positions

    def is_ship_exist(self, positions):
        is_exist = False
        for pos in positions:
            if pos in self.all_position:
                is_exist = True
        return is_exist

    def generate_position_randomly(self, size, ship_type):
        # odd for horizontal and even for vertical, pick row and column
        direction = random.randint(1, size)

        row = random.randint(0, 19)
        col = random.randint(0, 7)

        if ship_type == "CV":
            row = random.randint(1, 19) 
            col = random.randint(0, 6)                                       
        # row = 6
        # col = 11
        # direction = 0
        positions = self.get_simple_position(direction, row, col, size)

        if ship_type == "OR":
            if (direction % 2 != 0) :
                extra_positions = self.get_simple_position(direction, row, col + 1, size)
            else:
                extra_positions = self.get_simple_position(direction, row + 1, col, size)
            positions.extend(extra_positions)
        elif ship_type == "CV":
            if (direction % 2 != 0) :
                if (row - size > 0):
                    fix_row = row - 2
                else:
                    fix_row = row + 1
                # print('Row - Col => ' + str(row)+ ' => ' + str(col))
                # print('Fix_Row - Size => ' + str(fix_row)+ ' => ' + str(size))
                extra_positions = self.get_simple_position(direction, fix_row, col + 1, 1)
            else:
                if (col - size > 0):
                    fix_col = col - 1
                else:
                    fix_col = col + 2
                # print('Row - Col => ' + str(row)+ ' => ' + str(col))
                # print('Fix_Col - Size => ' + str(fix_col)+ ' => ' + str(size))
                extra_positions = self.get_simple_position(direction, row - 1, fix_col, 1)
            positions.extend(extra_positions)

        return positions

    def get_simple_position(self, direction, row, col, size):
        positions = []
        if (direction % 2 != 0) :
            # left first, then right
            if (row - size > 0):
                for i in range(0, size):
                    positions.append([row - i, col])
            else: # row
                for i in range(0, size):
                    positions.append([row + i, col])
        else:
            # top first, then bottom
            if (col - size > 0):
                for i in range(0, size):
                    positions.append([row, col - i])
            else: # row
                for i in range(0, size):
                    positions.append([row, col + i])
        return positions