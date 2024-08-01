import pygame

class Explosao():
    def __init__(self, imagem):
        super().__init__()
        self.sprite = pygame.image.load('./imagens/' + imagem +'.png')
        self.sprite = pygame.transform.scale(self.sprite, (300, 300))
