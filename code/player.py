from setting import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos ,groups,collisions_sprites ):
        super().__init__(groups)
        self.load_images()
        self.state,self.frame_index = 'down', 0
        self.image = pygame.image.load(join('images','player','down','0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60,-90)

        #Movement
        self.dir = pygame.math.Vector2()
        self.speed = 500
        self.collision_sprites = collisions_sprites

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'down': [] , 'up': []}

        for state in self.frames.keys():
            for folder_path,sub_folders,file_names in walk(join('images','player',state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path,file_name)
                        surf = pygame.image.load(full_path)
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.dir.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
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

    def animate(self,dt):
        if self.dir.x != 0:
            self.state = 'right' if self.dir.x > 0 else 'left'
        if self.dir.y != 0:
            self.state = 'down' if self.dir.y > 0 else 'up'
        
        self.frame_index = self.frame_index + 5 * dt if self.dir else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        
