import pygame as pg
import time as t 
import math
from projectile import *

class Worm:
    def __init__(self, game, x, y, color, name):
        self.name = name
        self.game = game
        self.rect = pg.Rect(x,y, 22, 26)
        self.color = color
        self.speed = 0.1
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.12
        self.jump_power = 1
        self.on_ground = False
        self.last_jump_time = 0
        self.jump_cooldown = 0.4
        self.charging_shot = False
        self.charge_start_time = 0
        self.min_shot_power = 5
        self.max_shot_power = 15
        self.hp = 100
        self.aim = 0
        self.facing = "R"
        self.weapons = ["rkt", "gnd"]
        self.curweapon = "rkt"
        self.weapon_icons = {
            "rkt": pg.image.load("assets/Sprites/bazooka_icon.png").convert_alpha(),
            "gnd": pg.image.load("assets/Sprites/grenade_icon.png").convert_alpha()
        }
        self.sprites = {
            "idle_L": pg.image.load("assets/Sprites/wormL.png").convert_alpha(),
            "idle_R": pg.image.load("assets/Sprites/wormR.png").convert_alpha(),
            "fly_L": pg.image.load("assets/Sprites/wormflyupL.png").convert_alpha(),
            "fly_R": pg.image.load("assets/Sprites/wormflyupR.png").convert_alpha(),
            "Dead" : pg.image.load("assets/Sprites/grave.png").convert_alpha()
        }
        self.alive = True

       
    def handle_input(self, keys):
        if self.game.state == "normal":
            if keys[pg.K_LEFT]:
                self.vel_x -= self.speed
                if self.facing == "R":
                    self.facing = "L"
                    self.aim = 3.2
            if keys[pg.K_RIGHT]:
                self.vel_x += self.speed
                if self.facing == "L":
                    self.facing = "R"
                    self.aim = 0
            if keys[pg.K_UP]:
                if self.aim < 1.3 and self.facing == "R":
                    self.aim += 0.01
                if self.aim > 1.8 and self.facing == "L":
                    self.aim -= 0.01
                
            if keys[pg.K_DOWN]:
                if self.aim > -1.5 and self.facing == "R":
                    self.aim -= 0.01
                if self.aim < 4.5 and self.facing == "L":
                    self.aim += 0.01
            if keys[pg.K_SPACE]:
                if not self.charging_shot:
                    self.charging_shot = True
                    self.charge_start_time = pg.time.get_ticks() 

            else:
                if self.charging_shot:
                    self.charging_shot = False
                    charge_duration = (pg.time.get_ticks() - self.charge_start_time) / 1000  
                    charge_duration = max(0.1, min(charge_duration, 2))  

                    power = self.min_shot_power + (self.max_shot_power - self.min_shot_power) * (charge_duration / 2)

                    start_x = self.rect.centerx
                    start_y = self.rect.centery
                    if self.curweapon == "gnd":
                        projectile = Grenade(self.game, start_x, start_y, self.aim, speed=power)
                    elif self.curweapon == "rkt":
                        projectile = Missile(self.game, start_x, start_y, self.aim, speed=power)

                    self.game.projectiles.append(projectile)
                    self.game.state = "waiting_for_projectile"

            if keys[pg.K_TAB]:
                if not self.tab_pressed:
                    self.switch_weapon()
                    self.tab_pressed = True
            else:
                self.tab_pressed = False

        if abs(self.vel_x) < 0.001:
            self.vel_x = 0

        

        if keys[pg.K_LSHIFT] and self.on_ground and self.game.current_time - self.last_jump_time > self.jump_cooldown:
            self.vel_y -= self.jump_power
            self.on_ground = False
            self.last_jump_time = t.time()

    def switch_weapon(self):

        curweapon_index = (self.weapons.index(self.curweapon) + 1) % len(self.weapons)
        self.curweapon = self.weapons[curweapon_index]

    def apply_horizontal_movement(self):
        if not hasattr(self, 'pos_x'):
            self.pos_x = float(self.rect.x)
        self.vel_x *= 0.9
        self.pos_x += self.vel_x
        new_x = int(self.pos_x)
        climbed = False

        for climb in range(4):  
            new_y = self.rect.y - climb
            if not self.collides_at(new_x, new_y):
                self.rect.x = new_x
                self.rect.y = new_y
                self.pos_y = float(self.rect.y)
                climbed = True
                break

        if not climbed:
            self.pos_x -= self.vel_x  

    def apply_gravity(self):
        if not hasattr(self, 'pos_y'):
            self.pos_y = float(self.rect.y)

        if not self.on_ground:
            if self.vel_y < 0:
                self.vel_y += self.gravity * 0.3
            else:
                self.vel_y += self.gravity * 0.7
        else:
            self.vel_y = 0
            self.jumped = False

        self.pos_y += self.vel_y
        new_y = int(self.pos_y)

        if not self.collides_at(self.rect.x, new_y):
            self.rect.y = new_y
            self.on_ground = False
        else:
            if self.vel_y > 0:
                self.on_ground = True
            else:
                self.on_ground = False
            self.vel_y = 0
            self.pos_y = float(self.rect.y)

    def apply_screen_limits(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos_x = self.rect.left
        if self.rect.right > self.game.SCREEN_W:
            self.rect.right = self.game.SCREEN_W
            self.pos_x = self.rect.left

        if int(self.rect.bottomleft[1]) == int(self.game.SCREEN_H):
            self.alive = False

    def move(self, keys):
        self.handle_input(keys)
        self.apply_horizontal_movement()
        self.apply_gravity()
        self.apply_screen_limits()

    def update_physics(self):
        self.apply_horizontal_movement()
        self.apply_gravity()
        self.apply_screen_limits()

    def collides_at(self, x, y):
        for px in range(self.rect.width):
            for py in range(self.rect.height):
                check_x = x + px
                check_y = y + py
                if self.game.map.is_solid(check_x, check_y):
                    return True
        return False

    def draw_weapon_icon(self, surface):
        icon = self.weapon_icons.get(self.curweapon)
        if icon:
            icon_rect = icon.get_rect()
            screen_width, screen_height = surface.get_size()
            icon_rect.bottomright = (screen_width - 10, screen_height - 10)
            surface.blit(icon, icon_rect)

    def draw(self, surface, active):
        if not self.alive:
            sprite = self.sprites["Dead"]
        else:
            sprite = self.sprites[f"idle_{self.facing}"]
        rect = sprite.get_rect(center=self.rect.center)
        surface.blit(sprite, rect.topleft)
        if self.alive:
            if self.charging_shot:
                duration = (pg.time.get_ticks() - self.charge_start_time) / 1000
                charge_ratio = min(duration / 2, 1)
                bar_width = 50
                pg.draw.rect(surface, (255, 255, 255), (self.rect.x-10, self.rect.y+35, bar_width, 10), 2)
                pg.draw.rect(surface, (240, 30, 0), (self.rect.x-10, self.rect.y+35, bar_width * charge_ratio, 10))

            if active:
                # pointer + crosshair 
                pg.draw.polygon(
                    self.game.display, (255, 255, 0),
                    [
                        (self.rect.centerx, self.rect.top - 15),
                        (self.rect.centerx - 10, self.rect.top - 25),
                        (self.rect.centerx + 10, self.rect.top - 25),
                    ]
                )

                if self.vel_x == 0:
                    aim_length = 20
                    center_x = self.rect.centerx
                    center_y = self.rect.centery
                    end_x = int(center_x + aim_length * math.cos(self.aim))
                    end_y = int(center_y - aim_length * math.sin(self.aim))
                    pg.draw.line(surface, (255, 0, 0), (end_x - 3, end_y), (end_x + 3, end_y), 2)
                    pg.draw.line(surface, (255, 0, 0), (end_x, end_y - 3), (end_x, end_y + 3), 2)
            else:
                self.game.draw_text(self.name, 14, self.rect.centerx, self.rect.top - 15)
                self.game.draw_text(f"HP: {self.hp}", 14, self.rect.centerx, self.rect.top - 30)


    

        