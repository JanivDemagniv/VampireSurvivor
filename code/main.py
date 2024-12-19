from setting import *
from player import Player

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

        #Sprites
        self.player = Player((WINDOW_WIDTH/2,WINDOW_HIEGHT/2),self.all_sprites)

    
    def start_game(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)

            self.surface.fill('red')
            self.all_sprites.draw(self.surface)
            pygame.display.update()
            
        pygame.quit()
        

if __name__ == '__main__':
    game = Game()
    game.start_game()