import pygame
from laser import Laser

pygame.init()

largura_tela = 1920
altura_tela = 1080
tela = pygame.display.set_mode((largura_tela, altura_tela))

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, largura_tela):
        super().__init__()
        self.sprite = pygame.image.load('./imagens/navio.png')
        self.sprite = pygame.transform.scale(self.sprite, (150, 200))
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.tela = tela
        self.x = x
        self.y = y
        self.largura_tela = largura_tela
        self.velocidade = 5
        self.shoot = False  # Novo atributo para indicar se o jogador está disparando

    def control(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            if self.rect.left > 0:  # Verifica se o jogador não ultrapassa a borda esquerda da tela
                self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            if self.rect.right < self.largura_tela:  # Verifica se o jogador não ultrapassa a borda direita da tela
                self.rect.x += self.velocidade
        if teclas[pygame.K_SPACE]:
            self.shoot = True  # Define o flag de disparo como True

    def draw(self):
        self.tela.blit(self.sprite, self.rect)
