from setting import *
from player import Player
from sprites import *

from random import randint

class Game():
    def __init__(self):
        #Setup
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.title = pygame.display.set_caption('Vampire Survival')
        self.surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HIEGHT))

        #Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #Sprites
        self.player = Player((WINDOW_WIDTH/2,WINDOW_HIEGHT/2),self.all_sprites,self.collision_sprites)
        for i in range(6):
            w,h = randint(60,100),randint(50,100)
            x,y = randint(0,WINDOW_WIDTH),randint(0,WINDOW_HIEGHT)
            CollisionsSprites((x,y),(w,h),(self.all_sprites,self.collision_sprites))

    
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
            self.all_sprites.draw(self.surface)
            pygame.display.update()
            
        pygame.quit()
        

if __name__ == '__main__':
    game = Game()
    game.start_game()