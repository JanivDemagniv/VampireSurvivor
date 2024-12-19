from setting import *

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