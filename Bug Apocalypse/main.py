import pygame as pg
from game import Game
from sys import exit
import time

g = Game()
pg.display.set_caption("Bug Apocalypse")
pg.mouse.set_visible(False)
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()


