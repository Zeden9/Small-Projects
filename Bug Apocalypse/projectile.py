import pygame as pg
import math
import time as t
from random import randint
class Projectile:
    def __init__(self, game, x, y, angle, speed):
        self.game = game
        self.x = x
        self.y = y
        self.radius = 4
        self.speed = speed
        self.vel_x = speed * math.cos(angle)
        self.vel_y = -speed * math.sin(angle)
        self.gravity = 0.1
        self.active = True
        self.explosion_frames = [
        pg.image.load(f"assets/Sprites/explosion-1-f/explosion-f{i}.png").convert_alpha() 
        for i in range(1,8)
        ]

    def update(self):
        #print(f"Velx: {self.vel_y}")
        self.vel_y += self.gravity


  

class Missile(Projectile):
    def __init__(self, game, x, y, angle, speed):
        super().__init__(game, x, y, angle, speed)
        self.image = pg.image.load("assets/Sprites/missile.png").convert_alpha()

    def draw(self, surface):
        angle = -math.degrees(math.atan2(self.vel_y, self.vel_x+self.game.wind)) - 90  # korekta kąta
        rotated = pg.transform.rotate(self.image, angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

    def update(self):
        super().update()
        self.x += self.vel_x + self.game.wind
        self.y += self.vel_y + self.game.wind
        if self.game.map.is_solid(int(self.x), int(self.y)):
            self.active = False
            self.game.map.destroy_at(int(self.x), int(self.y), radius=30)
            self.game.explosions.append(
                Explosion(self.game, self.x, self.y, self.explosion_frames, radius=120, damage=50)
            )


class Grenade(Projectile):
    def __init__(self, game, x, y, angle, speed):
        super().__init__(game, x, y, angle, speed)
        super().update()
        self.rect = pg.Rect(x, y, 10, 21)
        self.rect.center = (int(self.x), int(self.y))
        self.image = pg.image.load("assets/Sprites/grenade.png").convert_alpha()
        self.impact = pg.mixer.Sound("assets/sound/GRENADEIMPACT.wav")
        self.impact.set_volume(0.1)
        self.fuse = 3  # sekundy
        self.throw_time = t.time()
        self.gravity = 0.05
        self.vel_x == self.vel_x
        self.vel_y == self.vel_y

    def collides_at(self, x, y):
        for px in range(self.rect.width):
            for py in range(self.rect.height):
                check_x = int(x + px - self.rect.width / 2)
                check_y = int(y + py - self.rect.height / 2)
                if self.game.map.is_solid(check_x, check_y):
                    return True
        return False

    def update(self):
        super().update()
        self.vel_y += self.gravity

        new_x = self.x + self.vel_x
        if not self.collides_at(new_x, self.y):
            self.x = new_x
        else:
            if abs(self.vel_x) > 0.1:
                self.impact.play()
            self.vel_x *= -0.6  

        new_y = self.y + self.vel_y
        if not self.collides_at(self.x, new_y):
            self.y = new_y
        else:
            if abs(self.vel_y) > 0.5:
                self.impact.play()
            self.vel_y *= -0.3  
            self.vel_x *= 0.6   

        self.rect.center = (int(self.x), int(self.y))

        if abs(self.vel_x) < 0.2:
            self.vel_x = 0

        if t.time() - self.throw_time > self.fuse:
            self.active = False
            self.game.map.destroy_at(int(self.x), int(self.y), radius=30)
            explosion = Explosion(self.game, self.x, self.y, self.explosion_frames, radius=100, damage=70)
            self.game.explosions.append(explosion)            

    def draw(self, surface):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.image, rect)


class Explosion:
    def __init__(self, game, x, y, frames, radius, damage, frame_duration=50):
        self.game = game
        self.x = x
        self.y = y
        self.frames = frames
        self.frame_duration = frame_duration  # ms per frame
        self.radius = radius
        self.damage = damage
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.finished = False
        i = randint(1,3)
        pg.mixer.music.load(f"assets/sound/Explosion{i}.wav")
        pg.mixer.music.set_volume(0.01)
        pg.mixer.music.play()
        self.deal_damage_and_knockback()

    def deal_damage_and_knockback(self):
        center = pg.math.Vector2(self.x, self.y)

        for team in self.game.players:
            for worm in team:
                worm_center = pg.math.Vector2(worm.rect.center)
                dist = worm_center.distance_to(center)

                if dist <= self.radius:
                    dmg = int(self.damage * (1 - dist / self.radius))
                    worm.hp -= dmg

                    direction = (worm_center - center).normalize()
                    knockback_strength = (1 - dist / self.radius) * 5 
                    worm.vel_x += direction.x * knockback_strength
                    worm.vel_y += direction.y * knockback_strength


    def update(self, dt):
        if self.finished:
            return

        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.frame_duration:
            self.time_since_last_frame = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, surface):
        if not self.finished:
            frame = self.frames[self.current_frame]
            rect = frame.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(frame, rect)


    