import pygame
import sys

x = 1920 #DIMENSÕES DA TELA(EIXO X)
y = 1080 #DIMENSÕES DA TELA(EIXO Y)
screen = pygame.display.set_mode((x, y)) #criei essa variavel para poder chamamar a "tela" mais para frente -- João
time = pygame.time.Clock() #tambem botei essa variavel para contar o tempo de duração da partida -- João

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed=-8):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        self.destruicao()

    def destruicao(self):
        if self.rect.y < 0:
            self.kill()
