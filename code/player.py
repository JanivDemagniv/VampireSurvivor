from setting import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos ,groups,collisions_sprites ):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player','down','0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60,0)

        #Movement
        self.dir = pygame.math.Vector2()
        self.speed = 500
        self.collision_sprites = collisions_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.dir = self.dir.normalize() if self.dir else self.dir

    def move(self,dt):
        self.hitbox_rect.x += self.dir.x * self.speed * dt
        self.collisions('horizontal')
        self.hitbox_rect.y += self.dir.y * self.speed * dt
        self.collisions('vertical')
        self.rect.center = self.hitbox_rect.center

    def collisions(self,dir):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if dir == 'horizontal':
                    if self.dir.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.dir.x < 0: self.hitbox_rect.left = sprite.rect.right
                if dir == 'vertical':
                    if self.dir.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.dir.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def update(self,dt):
        self.input()
        self.move(dt)
        
