from setting import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
    
    def draw(self,target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HIEGHT / 2)
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite,'ground')]

        for layer in [ground_sprites,object_sprites]:
            for sprite in sorted(layer, key= lambda sprite: sprite.rect.centery):
                self.surface.blit(sprite.image,sprite.rect.topleft + self.offset)