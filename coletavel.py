import pygame

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo  # Tipo de coletável: 'moeda', 'sucata', etc.
        self.sprite = pygame.image.load('./imagens/' + self.tipo + '.png')
        if self.tipo != "rum":
            self.sprite = pygame.transform.scale(self.sprite, (50, 50))
        else:
            self.sprite = pygame.transform.scale(self.sprite, (70, 70))
        self.rect = self.sprite.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 5  # Velocidade de descida; ajuste conforme necessário
