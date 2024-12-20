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

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,frames,player,collision_sprites ,*groups):
        super().__init__(*groups)
        self.player = player

        self.frames, self.frame_index = frames,0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        self.rect = self.image.get_frect(center = pos) 
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.dir = pygame.Vector2()
        self.speed = 350

    def move(self,dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.dir = (player_pos - enemy_pos).normalize()

        self.hitbox_rect.centerx += self.dir.x * self.speed * dt
        self.collisions('horizontal')
        self.hitbox_rect.centery += self.dir.y * self.speed * dt
        self.collisions('vertical')
        self.rect.center = self.hitbox_rect.center

    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def collisions(self,dir):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if dir == 'horizontal':
                    if self.dir.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.dir.x < 0: self.hitbox_rect.left = sprite.rect.right
                if dir == 'vertical':
                    if self.dir.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.dir.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def update(self, dt):
        self.move(dt)
        self.animate(dt)