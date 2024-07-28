import pygame

class Objeto:
    def __init__(self, x, y, tela):
        self.sprite = pygame.image.load('./imagens/tronco.jpeg')
        self.sprite = pygame.transform.scale(self.sprite, (130, 20))
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.vel = 5
        self.tela = tela

    def movimentacao(self):
        self.rect.x += self.vel

    def draw(self):
        self.tela.blit(self.sprite, self.rect)
