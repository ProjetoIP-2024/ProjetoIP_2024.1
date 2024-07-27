import pygame

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Tamanho do coletável
        self.image.fill((0, 255, 0))  # Cor verde como exemplo; substitua com a imagem real
        self.rect = self.image.get_rect(topleft=(x, y))
        self.tipo = tipo  # Tipo de coletável: 'moeda', 'sucata', etc.

    def update(self):
        self.rect.y += 5  # Velocidade de descida; ajuste conforme necessário