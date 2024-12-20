from setting import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import choice

class Game():
    def __init__(self):
        #Setup
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.title = pygame.display.set_caption('Vampire Survival')
        self.surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #Shooting
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        #Enemy Timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event,200)
        self.spawn_pos = []

        #Audio
        self.shoot_sound = pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_sound.set_volume(0.4)
        self.impact_suond = pygame.mixer.Sound(join('audio','impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio','music.wav'))
        self.music.set_volume(0.3)
        self.music.play(loops= -1)


        self.load_images()
        self.setup()
        

    def load_images(self):
        self.bullet_surface = pygame.image.load(join('images','gun','bullet.png')).convert_alpha()

        folders = list(walk(join('images','enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _,file_names in walk(join('images','enemies',folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_dir * 50
            Bullet(pos,self.bullet_surface,self.gun.player_dir,(self.all_sprites,self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True


    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))
        for x,y,image in map.get_layer_by_name('Ground').tiles():
            Sprites((x * TITLE_SIZE, y * TITLE_SIZE),image,self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionsSprites((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))

        for col_obj in map.get_layer_by_name('Collisions'):
            CollisionsSprites((col_obj.x,col_obj.y),pygame.Surface((col_obj.width,col_obj.height)),self.collision_sprites)
            
        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x,marker.y),self.all_sprites,self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_pos.append((marker.x,marker.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet,self.enemy_sprites,False,pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_suond.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
    
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player,self.enemy_sprites,False, pygame.sprite.collide_mask):
            self.running = False
    
    def start_game(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_pos),choice(list(self.enemy_frames.values())),self.player,self.collision_sprites ,(self.all_sprites,self.enemy_sprites))


            #Update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            #Draw
            self.surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            
        pygame.quit()
        

if __name__ == '__main__':
    game = Game()
    game.start_game()