import pygame as pg
import time
import pygame as pg
import time
import re

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.SCREEN_W / 2, self.game.SCREEN_H / 2
        self.run_display = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = -100
        self.cursor_delay = 0.1
        self.last_cursor_move = 0

    def draw_menu_option(self, text, x, y, selected):
        rect = pg.Rect(0, 0, 300, 40)
        rect.center = (x, y)
        bg_color = self.game.WHITE if selected else self.game.BLUE
        text_color = self.game.BLACK if selected else self.game.WHITE
        self.game.draw_rounded_button(bg_color, rect, text, text_size=20, text_color=text_color)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()

class VerticalMenu(Menu):
    def __init__(self, game, title, options):
        super().__init__(game)
        self.title = title
        self.options = options 
        self.state_index = 0
        self.cursor_rect.midtop = (options[0][1] + self.offset, options[0][2])

    def move_cursor(self, keys):
        now = time.time()
        if now - self.last_cursor_move < self.cursor_delay:
            return


        if keys[pg.K_DOWN]:
            self.state_index = (self.state_index + 1) % len(self.options)
            self.last_cursor_move = now
        elif keys[pg.K_UP]:
            self.state_index = (self.state_index - 1) % len(self.options)
            self.last_cursor_move = now

        x, y = self.options[self.state_index][1:]
        self.cursor_rect.midtop = (x + self.offset, y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            keys = pg.key.get_pressed()
            self.game.check_events()
            self.check_input(keys)
            self.game.display.fill(self.game.BLUE)
            self.game.draw_text(self.title, 20, self.mid_w, self.mid_h - 100)

            for idx, (name, x, y) in enumerate(self.options):
                selected = idx == self.state_index
                self.draw_menu_option(name, x, y, selected)

            self.blit_screen()


class MainMenu(VerticalMenu):
    def __init__(self, game):
        self.bgrdWormL = pg.image.load("assets/MainMenu/backgroundWormLeft.png")
        self.bgrdWormR = pg.image.load("assets/MainMenu/backgroundWormRight.png")
        self.bgrdWormL = pg.transform.smoothscale(self.bgrdWormL, (self.bgrdWormL.get_width() // 2, self.bgrdWormL.get_height() // 2))
        self.bgrdWormR = pg.transform.smoothscale(self.bgrdWormR, (self.bgrdWormR.get_width() // 2, self.bgrdWormR.get_height() // 2))

        mid_w, mid_h = game.SCREEN_W / 2, game.SCREEN_H / 2
        options = [
            ("Start", mid_w, mid_h + 30),
            ("Options", mid_w, mid_h + 80),
            ("Credits", mid_w, mid_h + 130),
            ("Exit", mid_w, mid_h + 180)
        ]
        super().__init__(game, "Bug Apocalypse", options)

        self.left_x = 0
        self.left_y = (game.SCREEN_H - self.bgrdWormL.get_height()) // 2
        self.right_x = game.SCREEN_W - self.bgrdWormR.get_width()
        self.right_y = (game.SCREEN_H - self.bgrdWormR.get_height()) // 2

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            keys = pg.key.get_pressed()
            self.game.check_events()
            self.check_input(keys)
            self.game.display.fill(self.game.BLUE)
            self.game.display.blit(self.bgrdWormL, (self.left_x, self.left_y))
            self.game.display.blit(self.bgrdWormR, (self.right_x, self.right_y))
            self.game.draw_text("Bug Apocalypse", 40, self.mid_w, self.mid_h - 180)

            for idx, (name, x, y) in enumerate(self.options):
                selected = idx == self.state_index
                self.draw_menu_option(name, x, y, selected)

            self.blit_screen()

    def check_input(self, keys):
        self.move_cursor(keys)
        if keys[pg.K_RETURN]:
            selected = self.options[self.state_index][0]
            if selected == "Start":
                self.run_display = False
                self.game.curr_menu = self.game.name_input_menu
                #self.game.playing = True
            elif selected == "Options":
                self.game.curr_menu = self.game.options
            elif selected == "Credits":
                self.game.curr_menu = self.game.credits
            elif selected == "Exit":
                self.game.running = False
            self.run_display = False



class OptionsMenu(VerticalMenu):
    def __init__(self, game):
        mid_w, mid_h = game.SCREEN_W / 2, game.SCREEN_H / 2
        options = [
            ("Volume", mid_w, mid_h + 20),
            ("Controls", mid_w, mid_h + 70),
        ]
        super().__init__(game, "Options", options)

    def check_input(self, keys):
        self.move_cursor(keys)
        if keys[pg.K_ESCAPE]:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif keys[pg.K_RETURN]:
            selected = self.options[self.state_index][0]
            if selected == "Volume":
                pass  # tu możesz dodać logikę głośności
            elif selected == "Controls":
                pass  # tu możesz dodać logikę sterowania
            self.run_display = False



class NameInputMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.names = [""] * 4
        self.current_index = 0
        self.input_active = True
        self.error_message = ""
        self.error_timer = 0

    def is_valid_name(self, name):
        return re.fullmatch(r"[A-Z][a-zA-Z]{0,9}", name) is not None

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.handle_input()
            self.game.display.fill(self.game.BLUE)

            self.game.draw_text("Enter Worm Names", 30, self.mid_w, self.mid_h - 180)
            self.game.draw_text(f"Worm {self.current_index + 1}:", 24, self.mid_w, self.mid_h - 100)
            self.game.draw_text(self.names[self.current_index] + "|", 24, self.mid_w, self.mid_h - 60)

            if self.error_message and time.time() - self.error_timer < 2:
                self.game.draw_text(self.error_message, 16, self.mid_w, self.mid_h)

            self.blit_screen()

    def handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                self.run_display = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.run_display = False
                    self.game.curr_menu = self.game.options
                elif event.key == pg.K_BACKSPACE:
                    self.names[self.current_index] = self.names[self.current_index][:-1]
                elif event.key == pg.K_RETURN:
                    current_name = self.names[self.current_index]
                    if self.is_valid_name(current_name):
                        if self.current_index < 3:
                            self.current_index += 1
                        else:
                            self.game.worm_names = self.names.copy()
                            self.run_display = False
                            self.game.playing = True
                            #self.game.curr_menu = self.game.main_menu
                    else:
                        self.error_message = "Invalid name: Max 10 letters, starts with a capital, no digits"
                        self.error_timer = time.time()
                else:
                    if len(self.names[self.current_index]) < 10 and event.unicode.isprintable():
                        self.names[self.current_index] += event.unicode

class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if pg.key.get_pressed()[pg.K_ESCAPE]:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLUE)
            self.game.draw_text("Author: Mateusz Znaleźniak mz312243", 20, self.mid_w, self.mid_h)
            self.blit_screen()


