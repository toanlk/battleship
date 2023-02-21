import pprint

class Map:
    def __init__(self, boardWidth, boardHeight):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight

    # -----------------------------------------------------------------------------------------------------
    def draw(self, ships, shot_map):
        # Initialize the map
        map = [[' . ' for x in range(self.boardHeight)] for y in range(self.boardWidth)]

        for ship in ships:
            for pos in ship['coordinates']:
                try:
                    map[pos[0]][pos[1]] = ' x '
                except:
                    print("Place ship issue: " + str(pos))
                    pass
        
        for pos in shot_map:
            try:
                map[pos[0]][pos[1]] = ' * '
            except:
                print("Shot issue: " + str(pos))
                pass
        
        hit_rate = self.hit_rate(ships, shot_map)
        print("Battleship hit: " + str(hit_rate) + "%" + "\n")

        # Draw the map
        for i in reversed(range(self.boardWidth)):
            for j in range(self.boardHeight):
                print(map[i][j], end=" ")
            print("\n")
            # print(str(i) + "\n")
        # for j in range(self.boardHeight):
        #     print(" " + str(j) + " ", end=" ")

    # -----------------------------------------------------------------------------------------------------
    def hit_rate(self, ships, shot_map):
        coordinates = []
        for ship in ships:
            for pos in ship['coordinates']:
                coordinates.append(pos)

        hit = 0
        for pos in coordinates:
            if pos in shot_map:
                hit = hit + 1

        return round(hit/len(coordinates) * 100)