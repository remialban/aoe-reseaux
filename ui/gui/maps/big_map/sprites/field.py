import pygame.sprite


class Field(pygame.sprite.Sprite):
    def __init__(self):
        self.sprite_image = pygame.image.load("assets/sand.png")
        self.image = pygame.transform.scale(self.sprite_image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (400, 400)