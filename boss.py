import pygame
from laser import Laser

class Boss:
    def __init__(self, x, y):
        self.sprite = pygame.image.load('./imagens/boss_final.png')
        self.sprite = pygame.transform.scale(self.sprite, (200, 400))
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.speed = 6
        self.ultimo_tempo = 0
        self.lasers = pygame.sprite.Group()
        self.vida = 15
        self.shoot = False
        self.ultimo_tempo_inimigo = 0
        self.inimigo = False

    def movimento(self, largura_tela):

        self.rect.x += self.speed

        if self.rect.left <= 0:
            self.speed =  -self.speed 
        elif self.rect.right >= largura_tela:
            self.speed = -self.speed

    def desenhar_boss(self, screen):

        screen.blit(self.sprite, self.rect.topleft)

    def atirar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tempo >= 1000:
            self.shoot = True
            self.ultimo_tempo = tempo_atual

    def receber_dano(self, dano):

        self.vida -= dano
        if self.vida <= 0:
            self.morrer()
            return True

    def morrer(self):
        self.kill()

    def gerar_inimigos(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tempo_inimigo >= 1500:
            self.inimigo = True
            self.ultimo_tempo_inimigo = tempo_atual
