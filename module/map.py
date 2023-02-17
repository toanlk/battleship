# -*- coding: utf-8 -*-

class Map:
    def __init__(self, boardWidth, boardHeight):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight

    # -----------------------------------------------------------------------------------------------------
    def draw(self, ships):
        # Initialize the map
        map = [['.' for x in range(self.boardHeight)] for y in range(self.boardWidth)]

        for ship in ships:
            for pos in ship['coordinates']:
                try:
                    map[pos[0]][pos[1]] = 'x'
                except:
                    pprint.pprint(pos)
                    pass
                
        # Draw the map
        for i in range(self.boardWidth):
            for j in range(self.boardHeight):
                print(map[i][j], end=" ")
            print()