from setting import *
from math import atan2, degrees

class Sprites(pygame.sprite.Sprite):
    def __init__(self,pos,surf ,*groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True

class CollisionsSprites(pygame.sprite.Sprite):
    def __init__(self, pos,surf,*groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player,*groups):
        #player connections
        self.player = player
        self.distance = 140
        self.player_dir = pygame.Vector2(1,0)

        #sprite setup
        super().__init__(*groups)
        self.gun_surf = pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_dir * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH /2 , WINDOW_HIEGHT / 2)
        self.player_dir = (mouse_pos - player_pos).normalize()

    def gun_rotate(self):
        angle = degrees(atan2(self.player_dir.x,self.player_dir.y)) - 90
        if self.player_dir.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf,angle,1) 
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf,abs(angle),1) 
            self.image = pygame.transform.flip(self.image, False ,True)

    def update(self, _):
        self.get_direction()
        self.gun_rotate()
        self.rect.center = self.player.rect.center + self.player_dir * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, surf , dir ,*groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.speed = 1000
        self.dir = dir
        self.shooted = pygame.time.get_ticks()
        self.shoot_time = 1000

    def update(self,dt):
        current_time = pygame.time.get_ticks()
        self.rect.center += self.dir * self.speed * dt
        if current_time - self.shooted >= self.shoot_time:
            self.kill()
        