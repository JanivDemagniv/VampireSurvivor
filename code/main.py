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

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()
        

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

    
    def start_game(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #Update
            self.all_sprites.update(dt)

            #Draw
            self.surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            
        pygame.quit()
        

if __name__ == '__main__':
    game = Game()
    game.start_game()