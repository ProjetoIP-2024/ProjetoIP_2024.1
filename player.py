import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, largura_tela):
        super().__init__()
        self.sprite = pygame.image.load('./imagens/navio_old.png')
        self.sprite = pygame.transform.scale(self.sprite, (150, 200))
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.tela = tela
        self.x = x
        self.y = y
        self.largura_tela = largura_tela
        self.velocidade = 5
        self.shoot = False
        self.vida = 5
        self.canhao = False
        self.canhao_melhor = False


    def control(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            if self.rect.right < self.largura_tela:
                self.rect.x += self.velocidade
        if teclas[pygame.K_SPACE]:
            self.shoot = True

    def draw(self):
        self.tela.blit(self.sprite, self.rect)
        self.desenhar_vida()

    def desenhar_vida(self):
        fonte = pygame.font.SysFont(None, 36)
        vida_texto = fonte.render(f'Vida: {self.vida}', True, (255, 0, 0))
        self.tela.blit(vida_texto, (10, 10))

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            return False
        return True
    
    def evolucao_canhao_melhor(self, canhao):
        if canhao:
            self.sprite = pygame.image.load('./imagens/Barco_exemplo2FINAL.png')
            self.sprite = pygame.transform.scale(self.sprite, (150, 200))
            self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
            self.velocidade = 5

    def evolucao_canhao(self, canhao):
        if canhao:
            self.sprite = pygame.image.load('./imagens/navio_old2.png')
            self.sprite = pygame.transform.scale(self.sprite, (150, 200))
            self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
            self.velocidade = 5
        
