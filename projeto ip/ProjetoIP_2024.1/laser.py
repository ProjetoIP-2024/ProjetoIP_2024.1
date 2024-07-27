import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, imagem):
        super().__init__()
        self.sprite = pygame.image.load('./imagens/' + imagem +'.png')
        self.sprite = pygame.transform.scale(self.sprite, (75, 75))
        self.rect = self.sprite.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        self.destruicao()

    def destruicao(self):
        if self.rect.y < 0:
            self.kill()
