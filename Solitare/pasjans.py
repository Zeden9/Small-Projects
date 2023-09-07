# This is a sample Python script.
import random
import inspect
#import gui 


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Card:
    id = 0
    colour = None
    value = None
    hidden = None

    def show_properties(self):
        print(f"ID: {self.id}\n"
              f"Colour: {self.colour}\n"
              f"Value: {self.value}\n"
              f"Hidden: {self.hidden}\n")


colours = ['Trefl', "Karo", "Kier", "Pik"]


def create_cardset():
    card_set = [Card() for _ in range(52)]
    i = 1
    colour_id = 0
    value = 1
    for card in card_set:
        card.id = i
        card.colour = colours[colour_id]
        card.value = value
        card.hidden = True
        if card.id % 13 == 0:
            colour_id += 1
            value = 1
        else:
            value += 1
        i += 1
    
    random.shuffle(card_set)
    return card_set


def create_game(card_set: list):
    card_set = card_set
    board = [[0 for y in range(13)] for x in range(7)]
    card_index = 0
    for x in range(7):
        for y in range(x+1):
            board[x][y] = card_set[card_index]
            card_index += 1


    for y in range(13):
        for x in range(7):
            
            if(board[x][y] == 0):
                pass
            else:
                card_colour = "Pik"
                card_value = str(board[x][y].value)
                card_hidden = str(board[x][y].hidden)
                # gui.create_card(card_value, card_colour, card_hidden, x, y)
                print(" ", end="")
           #else:
                if(x == y): board[x][y].hidden = False

                if(board[x][y].hidden == False):                    
                    if(board[x][y].value == 1):
                        print("A", end="")
                    elif(board[x][y].value == 10):
                        print("D", end="")
                    elif(board[x][y].value == 11): 
                        print("J", end="")
                    elif(board[x][y].value == 12):
                        print("Q", end="")
                    elif(board[x][y].value == 13):
                        print("K", end="")
                    else:
                        print(board[x][y].value, end="")
                else:
                    print("*", end="")
        print("")   
                         






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #gui.window.mainloop()
    cards = create_cardset()
    create_game(cards)
    # for card in cards:
    #     card.show_properties()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
