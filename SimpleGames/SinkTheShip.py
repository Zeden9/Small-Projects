import re 
import os 

class Ship:
    size:int
    x:chr
    y:int
    orientation:chr
    sunk = False

    def __init__(self, x, y, size, orientation):
        if (y > 9 or y < 0 or ord(x) < 97 or ord(x) > 106):
            return False
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation
        print("Ship created succesfully")

    

class Board:
    ships = []
    blocked_spots = []

    def cords_taken(self, cords):
        if cords in self.blocked_spots:
            return True
        else:
            return False
        
    def block_position(self, ship:Ship):

        if ship.orientation.lower() == 'n':
            self.blocked_spots.append([ship.x, ship.y-1])
            self.blocked_spots.append([ship.x, ship.y+ship.size])
            for n in range(ship.size):
                self.blocked_spots.append([ship.x, ship.y+n])
                self.blocked_spots.append([chr(ord(ship.x)-1), ship.y+n])
                self.blocked_spots.append([chr(ord(ship.x)+1), ship.y+n])
            

        elif ship.orientation.lower() == 's':
            self.blocked_spots.append([ship.x, ship.y+1])
            self.blocked_spots.append([ship.x, ship.y-ship.size])
            for n in range(ship.size):
                self.blocked_spots.append([ship.x, ship.y-n])
                self.blocked_spots.append([chr(ord(ship.x)-1), ship.y-n])
                self.blocked_spots.append([chr(ord(ship.x)+1), ship.y-n])


        elif ship.orientation.lower() == 'w':
            self.blocked_spots.append([chr(ord(ship.x)+1), ship.y])
            self.blocked_spots.append([chr(ord(ship.x)-ship.size), ship.y])
            for n in range(ship.size):
                self.blocked_spots.append([chr(ord(ship.x)-n), ship.y]) 
                self.blocked_spots.append([chr(ord(ship.x)-n), ship.y-1])
                self.blocked_spots.append([chr(ord(ship.x)-n), ship.y+1])

        elif ship.orientation.lower() == 'e':
            self.blocked_spots.append([chr(ord(ship.x)-1), ship.y])
            self.blocked_spots.append([chr(ord(ship.x)+ship.size), ship.y])
            for n in range(ship.size):
                self.blocked_spots.append([chr(ord(ship.x)+n), ship.y])
                self.blocked_spots.append([chr(ord(ship.x)+n), ship.y-1])
                self.blocked_spots.append([chr(ord(ship.x)+n), ship.y+1])
        return

    def detect_collision(self, cords, size, orientation):
        if self.cords_taken(cords):
            return True
 
            


    def create_fleet(self):
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
            prompt = f"Input coordinates and orientation of your {masts} ship (e.g. A5 N):\n"
            data = input(prompt).lower()
            match = re.search('[a-j][0-9][nesw]', data)
            if match:
                x, y, orientation = match.group().split()[0]
                y = int(y)
                if not self.detect_collision([x,y],size,orientation):
                    new_ship = Ship(x, y, size, orientation)
                    self.block_position(new_ship)
                    self.ships.append(new_ship)
                    print(f"\n\nShips:{self.ships}\nBlocked:{self.blocked_spots}")
                else:
                    print("The coordinates are already taken.")
                    continue
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