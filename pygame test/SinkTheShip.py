import re 
import os 

class Ship:
    size:int
    x:chr
    y:chr
    orientation:chr
    sunk = False

    def __init__(self, x, y, size, orientation):
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation
        print("Ship created succesfully")

    

class Board:
    ships = []
    blocked_spots = []

    def create_fleet(self):
        BoardCreation = True
        while BoardCreation:
            if(len(self.ships) == 0): #0
                masts = "four-mast"
                size = 4
            elif(len(self.ships) > 0 and len(self.ships) <= 2): #1 2 
                masts = "three-mast"
                size = 3
            elif(len(self.ships) > 2 and len(self.ships) <= 5): # 3 4 5 
                masts = "two-mast"
                size = 2
            elif(len(self.ships) > 5 and len(self.ships) <= 9): # 6 7 8 9
                masts = "one-mast"
                size = 1

            prompt = f"Input coordinates and orientation of your {masts} ship (e.g. A5 N):\n"
            data = input(prompt).lower()
            match = re.search('[a-j][0-9][nesw]', data)
            if match:
                if not 
                x, y, orientation = match.group().split()[0]
                new_ship = Ship(x, y, size, orientation)
                self.ships.append(new_ship)
            else:
                print("Invalid input. Please provide coordinates and orientation in the correct format.")
                continue
            if (len(self.ships)) > 9: 
                BoardCreation = False




        
        
def start_game():
    dictionary = {
        "a":0,
        "b":1,
        "c":2,
        "d":3,
        "e":4,
        "f":5,
        "g":6,
        "h":7,
        "i":8,
        "j":9,
    }
    player_board = Board()
    player_board.create_fleet()
    print(player_board.ships)
    enemy_board = Board()


def main():
    start_screen = '''
Welcome to Sink The Ship

Rules are simple. You get a 10x10 grip map, where you have to place:
-One four-masted ship
-Two three-masted ships
-Three two-masted ships
-Four one-masted ship
To place a ship, you must input it's coordinates and orientation (e.g. A5 N - ship starts at coordinates A5 and is facing North). 
The order of placing the ships is from the biggest to the smallest.
The ships can't collide or be right next to each other. After placing the ships, your objective is to destroy your enemy's fleet.
In order to do it, you must send a missile to specified coordinates and hit his ships.
To sink a ship, you must hit all of it's masts. You of course don't see your opponent's board, so you must fire the missiles blindly.
After firing, you get a message if you've missed, hit or sunk his boat.


Do you want to start playing? Y/N
    
'''
    decision = input(start_screen)
    if(decision.lower() != 'y'):
        return
    else:
        start_game()

if __name__ == "__main__":
    main()