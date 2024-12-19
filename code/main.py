from setting import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from random import randint
from groups import AllSprites

class Game():
    def __init__(self):
        #Setup
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.title = pygame.display.set_caption('Vampire Survival')
        self.surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))
        self.load_images()

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        #Shooting
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        self.setup()
        

    def load_images(self):
        self.bullet_surface = pygame.image.load(join('images','gun','bullet.png')).convert_alpha()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
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

    
    def start_game(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #Update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)

            #Draw
            self.surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            
        pygame.quit()
        

if __name__ == '__main__':
    game = Game()
    game.start_game()