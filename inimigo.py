import pygame

class Inimigos(pygame.sprite.Sprite):
    
    def __init__(self, x, y, tela):
        super().__init__()
        self.sprite = pygame.image.load('./imagens/inimigo.png')
        self.sprite = pygame.transform.scale(self.sprite, (100, 200))
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.tela = tela
        self.velocidade = 20
        self.ultimo_movimento = pygame.time.get_ticks()
        self.direcao_x = self.velocidade 
        self.direcao_y = 0 
        self.ultimo_tiro = 0

    def gerar_inimigos(self):
        self.tela.blit(self.sprite, self.rect)

    def mover(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_movimento >= 200:
            self.rect.x += self.direcao_x
            self.rect.y += self.direcao_y
        
            largura_tela = self.tela.get_width()

            if self.rect.right >= largura_tela:
                self.rect.right = largura_tela
                self.direcao_x = -self.velocidade 
                self.rect.y += 200 
            elif self.rect.left <= 0:
                self.direcao_x = self.velocidade 
                self.rect.y += 200

            self.ultimo_movimento = tempo_atual

    def gerar_novo_inimigo(self):
        novo_inimigo = Inimigos(0, 0, self.tela)
        return novo_inimigo

    def atirar(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tiro >= 3000:
            self.ultimo_tiro = tempo_atual
            return True
        return False
