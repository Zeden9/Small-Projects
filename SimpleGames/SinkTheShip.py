import re 
import os
from typing import List 
import random

letters_a_j = 'abcdefghij'
numbers_0_9 = '1234567890'
directions = 'swne'

class Ship:
    size:int
    x:chr
    y:int
    orientation:chr
    sunk = False
    sections_hit = []
    sections = []

    def __init__(self, x, y, size, orientation):
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation
        self.sections = []
        directions = {
            'n':(0,-1),
            's':(0,1),
            'e':(1,0),
            'w':(-1,0)
        }
        dx = directions[orientation][0]
        dy = directions[orientation][1]
        for n in range(size):
            new_cords = [chr(ord(x)+(n*dx)), y+(n*dy)]
            self.sections.append(new_cords)
        os.system("cls")
        print("Ship created succesfully")

    

class Board:
    isAlive = True
    ships: List[Ship] = []
    blocked_spots = []
    shot_spots = [["a",5]]
    missed_spots = [["a",6]]
    def __init__(self):
        self.ships = []
        self.blocked_spots = []

    #def cords_beyond_border(self, cords):


    def cords_available(self, cords):
        if cords in self.blocked_spots:
            return False
        else:
            return True
        
    def block_position(self, ship:Ship):
        orientation = ship.orientation.lower()
        x = ship.x
        y = ship.y
        size = ship.size

        directions = {
            'n' : [(0,-1), (-1,-1), (1,-1)],
            's' : [(0,1), (-1,1), (1,1)],
            'w' : [(-1,0), (-1,-1), (-1, +1)],
            'e' : [(1,0), (1,-1), (1, 1)]
        }

        if orientation == 'n':
            self.blocked_spots.extend([ [x, y+1], [x, y-size] ])
        elif orientation == 's':
            self.blocked_spots.extend([ [x, y-1], [x, y+size] ])
        elif orientation == 'w':
            self.blocked_spots.extend([ [chr(ord(x)+1), y], [chr(ord(x)-size), y] ])
        elif orientation == 'e':
            self.blocked_spots.extend([ [chr(ord(x)-1), y], [chr(ord(x)+size), y] ])
     
        for n in range(size):
            for dx, dy in directions[orientation]:
                if orientation == 'n' or orientation == 's':
                    self.blocked_spots.append([chr(ord(x) + dx), y+(n*dy)])
                else:
                    self.blocked_spots.append([chr(ord(x) + (n*dx)), y+dy])

    def detect_collision(self, cords, size, orientation):
        if self.cords_available(cords):
            directions = {
                'n':(0,-1),
                's':(0,1),
                'e':(1,0),
                'w':(-1,0)
            }
            x = cords[0]
            y = cords[1]
            dx = directions[orientation][0]
            dy = directions[orientation][1]
            for n in range(1, size):
                new_x = chr(ord(x)+(n*dx))
                new_y = y+(n*dy)
                if(new_y > 9 or new_y < 0 or ord(new_x) < 97 or ord(new_x) > 106): #cords are not available on the board
                    print("Out of bounds")
                    return True
                new_cords = [new_x, new_y]
                if not self.cords_available(new_cords):
                    return True
            return False
        else:
            return True 
 
    def create_fleet(self, isPlayer):
        os.system('cls')
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
            if(isPlayer):
                prompt = f"Input coordinates and orientation of your {masts} ship (e.g. A5 N):\n"
                data = input(prompt).lower()
            else:
                data = random.choice(letters_a_j) + random.choice(numbers_0_9) + random.choice(directions)
            match = re.search('[a-j][0-9][nesw]', str(data))
            if match:
                x, y, orientation = match.group().split()[0]
                y = int(y)
                if not self.detect_collision([x,y],size,orientation):
                    new_ship = Ship(x, y, size, orientation)
                    self.block_position(new_ship)
                    self.ships.append(new_ship)
                    #print(f"\n\nShips:{self.ships}\nBlocked:{self.blocked_spots}")
                    self.show()
                else:
                    print("The coordinates are already taken.")
                    continue
            else:
                print("Invalid input. Please provide coordinates and orientation in the correct format.")
                continue
            if (len(self.ships)) > 9: 
                BoardCreation = False

    def show(self):
        print("YOUR FLEET\n# A B C D E F G H I J K")
        cord_y = 97 #ascii for a
        for x in range(10):
            print(str(x), end="")
            for y in range(10):
                output = " *"
                cords = [chr(cord_y+y), x]
                for ship in self.ships:
                    if cords in ship.sections:
                        output = " O"
                        continue
                    elif cords in ship.sections_hit:
                        output = " X"
                print(output, end="")
            
            print("\n", end="")

        print("\nYOUR SHOTS\n# A B C D E F G H I J K")
        for x in range(10):
            print(str(x), end="")
            for y in range(10):
                output = " *"
                cords = [chr(cord_y+y), x]
                for ship in self.ships:
                    if cords in self.shot_spots:
                        output = " X"
                        continue
                    elif cords in self.missed_spots:
                        output = " O"
                print(output, end="")
            print("\n", end="")

    def shoot(self, enemy:Board)




        
        
def start_game():
    player_board = Board()
    AIboard = Board()
    board_decision = input("Do you want to create the board yourself [Y], or randomly generate it? [N] Y/N: ")
    if(board_decision.lower == "n"):
        player_board.create_fleet(False)
    else:
        player_board.create_fleet(True)
    AIboard.create_fleet(False)




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

