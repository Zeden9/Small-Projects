import pygame as pg
from menu import *
from worm import *
from Map import *
import time as t 
import threading
from random import uniform

class Game():
    def __init__(self):
        pg.init()
        self.wind = uniform(-3, 3)
        self.clock = pg.time.Clock()
        self.elapsed_time = 0
        self.timer_running = True
        threading.Thread(target=self.update_timer, daemon=True).start()
        self.pause_countdown = 0
        self.pause_thread = None
        self.running, self.playing = True, False
        self.SCREEN_W, self.SCREEN_H = 1080, 720
        self.display = pg.Surface((self.SCREEN_W, self.SCREEN_H))
        self.window = pg.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.fontname = pg.font.get_default_font()
        self.BLACK, self.WHITE, self.BLUE = (0, 0, 0), (255, 255, 255), (70, 130, 180)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self) 
        self.name_input_menu = NameInputMenu(self)
        self.curr_menu = self.main_menu
        self.map = Map(self)
        self.current_time = 0
        self.projectiles = []
        self.state = "normal"
        self.currentPlayerId = 0
        self.wait_timer_start = 0
        #name_input_menu.names[]
        #print(self.name_input_menu.names)
        
        self.currentPlayerId = 0
        self.currentWormIndices = [0, 0] 
        self.explosions = []
        self.backgroundMusic = pg.mixer.Sound("assets/sound/bgmusic.wav")
        self.backgroundMusic.set_volume(0.05)


    def game_loop(self):
        self.player1 = [
        Worm(self, 100, 400, (255, 0, 0), self.name_input_menu.names[0]), 
        Worm(self, 200, 400, (255, 0, 0), self.name_input_menu.names[1])
        ]
        self.player2 = [
            Worm(self, self.SCREEN_W - 100, 400, (0, 0, 255), self.name_input_menu.names[2]), 
            Worm(self, self.SCREEN_W - 200, 400, (0, 0, 255), self.name_input_menu.names[3])
        ]
        self.players = [self.player1, self.player2]
        
        if self.playing:
            self.backgroundMusic.play()
            self.last_switch_time = t.time()
            self.elapsed_time = 0
            pg.mixer.music.load(f"assets/sound/StartRound.wav")
            pg.mixer.music.set_volume(0.5)
            pg.mixer.music.play()
        while self.playing:
            keys = pg.key.get_pressed()
            self.current_time = t.time()
            self.check_events()

            self.check_worms()
            for projectile in self.projectiles:
                projectile.update()

            if self.state == "waiting_for_projectile":
                if all(not p.active for p in self.projectiles):
                    self.start_pause_countdown(5)
                    self.state = "post_turn_pause"

            

            if self.state == "normal" and self.current_time - self.last_switch_time >= 15:
                self.start_pause_countdown(5)

            self.projectiles = [p for p in self.projectiles if p.active]

            self.map.draw(self.display)

            for i, worms in enumerate(self.players):
                for j, worm in enumerate(worms):
                    if worm.hp <= 0 and worm.alive:
                        worm.alive = False

                    is_active = (i == self.currentPlayerId and j == self.currentWormIndices[i])
                    if is_active:
                        if not worm.alive:
                            if(not self.check_worms()):
                                self.start_pause_countdown(5)
                        worm.move(keys)
                    else:
                        worm.update_physics()

                    worm.draw(self.display, active=is_active)
                    if is_active:
                        worm.draw_weapon_icon(self.display)

            for projectile in self.projectiles:
                projectile.draw(self.display)

            self.update_explosions(self.clock.tick(144)) 

            if self.state == "game_over":
                self.timer_running = False
                #print(self.timer_running)
                self.draw_text(f"Game Over!", 50, self.SCREEN_W // 2, 50)
            elif self.state == "post_turn_pause": 
                self.draw_text(f"Next turn starts in {self.pause_countdown}", 50, self.SCREEN_W // 2, 50)

            #print(self.state)
            
            self.draw_timer()

            self.draw_wind_arrow()
            self.window.blit(self.display, (0, 0))
            #print(self.timer_running)
            
            if keys[pg.K_ESCAPE]:
                self.timer_running = False
                #print(self.timer_running)
                self.reset_game()
            pg.display.update()
    
    def update_explosions(self, dt):
        for e in self.explosions:
            e.update(dt)
        self.explosions = [e for e in self.explosions if not e.finished]

        for e in self.explosions:
            e.draw(self.display)
    
    def update_timer(self):
        while self.timer_running:
            time.sleep(1)
            self.elapsed_time += 1

    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02}:{secs:02}"

    def draw_timer(self):
        time_str = self.format_time(self.elapsed_time)
        timer_rect = pg.Rect(10, self.SCREEN_H - 50, 100, 40) 
        self.draw_rounded_button(color=self.BLUE, rect=timer_rect, text=time_str, text_size=20)

    def switch_player(self):
        for i, worms in enumerate(self.players):
            if i != self.currentPlayerId:
                for worm in worms:
                    worm.vel_x = 0

        self.wind = uniform(-3, 3)

        num_players = len(self.players)

        for _ in range(num_players):
            self.currentPlayerId = (self.currentPlayerId + 1) % num_players
            worms = self.players[self.currentPlayerId]

            if not any(w.alive for w in worms):
                continue

            for i in range(len(worms)):
                index = (self.currentWormIndices[self.currentPlayerId] + i + 1) % len(worms)
                if worms[index].alive:
                    self.currentWormIndices[self.currentPlayerId] = index
                    self.last_switch_time = self.current_time
                    ##print(f"Changed to player {self.currentPlayerId}, worm {index}")
                    return

        #print("No worm alive – game over.")
        self.reset_game()

    def start_pause_countdown(self, duration=3, gameOver=False):
        if self.state == "post_turn_pause" and not gameOver:
            return

        def countdown():
            self.pause_countdown = duration
            while self.pause_countdown > 0 and self.playing:
                time.sleep(1)
                self.pause_countdown -= 1
            if self.playing:
                if gameOver:
                    self.reset_game()
                else:
                    self.switch_player()
                    self.state = "normal"

        self.state = "game_over" if gameOver else "post_turn_pause"
        self.pause_thread = threading.Thread(target=countdown)
        self.pause_thread.start()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
      
    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.fontname, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def draw_rounded_button(self, color, rect, text, text_size=20, text_color=None, radius=20, border_thickness=5):
        pg.draw.rect(self.display, self.WHITE, rect, border_radius=radius, width=border_thickness*2)
        pg.draw.rect(self.display, color, rect.inflate(-border_thickness*1.5, -border_thickness*1.5), border_radius=radius)
        self.draw_text(text, text_size, rect.centerx, rect.centery)

    def check_worms(self):
        alive_players = [any(worm.alive for worm in team) for team in self.players]

        if sum(alive_players) <= 1:
            self.start_pause_countdown(30, True)
            return True

    def draw_wind_arrow(self):
        wind_strength = abs(self.wind)

        if wind_strength < 1:
            strength_level = 1
        elif wind_strength < 2:
            strength_level = 2
        else:
            strength_level = 3

        direction = "R" if self.wind > 0 else "L"
        arrow_path = f"assets/Sprites/wind/wind{direction}{strength_level}.png"
        arrow_image = pg.image.load(arrow_path).convert_alpha()
        img_w, img_h = arrow_image.get_size()
        aspect_ratio = img_w / img_h
        new_w = int(50*aspect_ratio)
        arrow_image = pg.transform.smoothscale(arrow_image, (new_w,50))

        x = self.SCREEN_W - new_w - 20
        y = 20
        self.display.blit(arrow_image, (x, y))

    def reset_game(self):
        self.timer_running = True
        self.name_input_menu = NameInputMenu(self)
        self.playing = False
        self.pause_countdown = 0
        self.pause_thread_running = False
        self.state = "normal"
        self.wind = uniform(-3, 3)
        self.clock = pg.time.Clock()
        self.elapsed_time = 0
        self.curr_menu = self.main_menu
        self.map = Map(self)
        self.current_time = 0
        self.currentPlayerId = 0
        self.wait_timer_start = 0
        self.player1 = [
            Worm(self, 100, 100, (255, 0, 0), self.name_input_menu.names[0]), 
            Worm(self, 200, 100, (255, 0, 0), self.name_input_menu.names[1])
            ]
        self.player2 = [
            Worm(self, self.SCREEN_W - 100, 100, (0, 0, 255), self.name_input_menu.names[2]), 
            Worm(self, self.SCREEN_W - 200, 100, (0, 0, 255), self.name_input_menu.names[3])
            ]
        self.players = [self.player1, self.player2]
        self.currentWormIndices = [0, 0]
        self.explosions = []
        pg.mixer.stop()       
        pg.mixer.music.stop() 