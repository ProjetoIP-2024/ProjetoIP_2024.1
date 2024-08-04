import pygame
class Explosao(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.image.load('./imagens/' + 'explosao' +'.png')
        self.sprite = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=center)
        self.timer = 1000  # Duração da explosão em frames

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            return True