import pygame as pg

class Map:
    def __init__(self, game):
        self.game = game
        self.background = pg.transform.smoothscale(
            pg.image.load("assets/Maps/Map1/Map1skybox.png").convert(),
            (self.game.SCREEN_W, self.game.SCREEN_H))
        self.map_img = pg.transform.smoothscale(
            pg.image.load("assets/Maps/Map1/Map1img.png").convert_alpha(),
            (self.game.SCREEN_W, self.game.SCREEN_H))
        self.mask_img = pg.transform.smoothscale(
            pg.image.load("assets/Maps/Map1/Map1Mask.png").convert(),
            (self.game.SCREEN_W, self.game.SCREEN_H))
        self.mask_surface = pg.mask.from_surface(self.mask_img)


        print(self.background.get_size())
        print(self.map_img.get_size())
        print(self.mask_surface.get_size())

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.map_img, (0, 0))

    def is_solid(self, x, y):
        
        try:
            color = self.mask_img.get_at((int(x), int(y)))
            return color == pg.Color(0, 0, 0)
        except IndexError:
            return True 
            
    def get_collision_type(self, rect):
        offset = 1

        if self.is_solid(rect.centerx, rect.bottom + offset):
            return 'floor'
        elif self.is_solid(rect.centerx, rect.top - offset):
            return 'ceiling'
        elif self.is_solid(rect.left - offset, rect.centery):
            return 'left'
        elif self.is_solid(rect.right + offset, rect.centery):
            return 'right'
        return None



    def destroy_at(self, x, y, radius):

            for dx in range(-radius, radius):
                for dy in range(-radius, radius):
                    if dx**2 + dy**2 < radius**2:
                        px = int(x + dx)
                        py = int(y + dy)
                        if 0 <= px < self.mask_img.get_width() and 0 <= py < self.mask_img.get_height():
                            self.mask_img.set_at((px, py), (255, 255, 255))  
                            self.map_img.set_at((px, py), (0, 0, 0, 0))      

            self.mask_surface = pg.mask.from_surface(self.mask_img)
