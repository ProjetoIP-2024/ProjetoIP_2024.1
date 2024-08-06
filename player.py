import pygame #Importa a biblioteca Pygame ao módulo.
from laser import Laser #Importa a classe Laser, que contém os tiros disparados pelo player.

class Player(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, largura_tela):
        super().__init__()
        self.sprite = pygame.image.load('./imagens/navio_old.png') #Carrega a sprite utilizada no início do jogo.
        self.sprite = pygame.transform.scale(self.sprite, (150, 200)) #Escala do player.
        self.rect = self.sprite.get_rect(topleft=(x, y)) #Coordenada de spawn.
        self.tela = tela #Local em que o player será desenhado.
        self.x = x #Coordenada no eixo X.
        self.y = y #Coordenada no eico Y.
        self.largura_tela = largura_tela #Tamanho da tela no eixo X.
        self.velocidade = 5 #Velocidade do player.
        self.shoot = False #Verifica se o player atirou.
        self.vida = 5 #Número de vidas do player.
        self.canhao = False #Se o player coletou o canhão intermediário.
        self.canhao_melhor = False #Se o player coletou o canhão final(melhor).
        self.level = 1 #Nível do player.
        self.lasers = pygame.sprite.Group() #Tiros.


    def control(self):
        teclas = pygame.key.get_pressed() #Verifica quais teclas estão sendo pressionadas.
        if teclas[pygame.K_LEFT]: #Se for a tecla seta para a esquerda.
            if self.rect.left > 0: #Se não está no ponto X = 0.
                self.rect.x -= self.velocidade #Movimenta-se um número N = velocidade do player para a esquerda.
        if teclas[pygame.K_RIGHT]: #Se for a tecla seta para a direita.
            if self.rect.right < self.largura_tela: #Se não está no ponto Xmáx.
                self.rect.x += self.velocidade #Movimenta-se um número N = velocidade do player para a direita.
        if teclas[pygame.K_SPACE]: #Se a tecla for Space.
            self.shoot = True #Indica que atirou.
            self.tiros() #Chama a função de atirar
            print(self.level) #Printa o nível.
            canhao_som = pygame.mixer.Sound('./efeitos_sonoros/canhão_som.wav')
            canhao_som.set_volume(0.1)
            canhao_som.play()

        if self.level == 3:
            if teclas[pygame.K_z]:
                self.shoot = True
                self.tiros()

    def draw(self):
        self.tela.blit(self.sprite, self.rect) #Desenha o player na tela.
        self.desenhar_vida() #Chama a função que desenha as vidas do player na tela.

    def desenhar_vida(self):
        pass

    def receber_dano(self, dano):
        self.vida -= dano #Se tomou dano, reduz a vida em 1 unidade.
        if self.vida < 0: #Se morreu.
            return False #Retorna um booleano que indica que o player morreu.
        return True #Retorna um booleano que indica que o player ainda pode continuar a jogar.
    
    def evolucao_canhao_melhor(self, canhao):
        if canhao: #Se coletou o canhão melhor.
            self.sprite = pygame.image.load('./imagens/Barco_exemplo2FINAL.png') #Sprite utilizada no barco ao coletar este canhão.
            self.sprite = pygame.transform.scale(self.sprite, (150, 200)) #Escala do player.
            self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) #Desenha o player na tela.
            self.velocidade = 5 #Velocidade do player.
            self.level_up_3() #Indica que o nível do player é o 3°.

    def evolucao_canhao(self, canhao):
        if canhao: #Se coletou o canhão intermediário.
            self.sprite = pygame.image.load('./imagens/Barco-nivel2.png.png') #Sprite utilizada no barco ao coletar este canhão.
            self.sprite = pygame.transform.scale(self.sprite, (150, 200)) #Escala do player.
            self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) #Desenha o player na tela.
            self.velocidade = 5 #Velocidade do player.
            self.level_up_2() #Indica que o nível do player é o 2°.
    
    def level_up_2(self):
        self.level = 2 #Evolução ao nível 2.

    def level_up_3(self):
        self.level = 3 #Evolução ao nível 3.

    def tiros(self):
        if self.level == 1: #Se ainda está no nível 1.
            laser = Laser(self.rect.midtop, -10, 0, 'bala_canhao') #Tipo de tiro que será disparado.
            self.lasers.add(laser) #Adiciona o tiro.
        elif self.level == 2: #Se estaá no nível 2 - canhão que dispara 3 tiros ao mesmo tempo.
            laser_central = Laser(self.rect.midtop, -10, 0, 'bala_canhao') #Tiro que irá ser disparado pelo centro.
            laser_esquerdo = Laser(self.rect.midtop, -10, -2, 'bala_canhao') #Tiro que irá ser disparado pela esquerda.
            laser_direito = Laser(self.rect.midtop, -10, -2, 'bala_canhao') #Tiro que será disparado pela direita.
            self.lasers.add(laser_central, laser_esquerdo, laser_direito) #Adiciona os tiros.
        elif self.level == 3:
            teclas = pygame.key.get_pressed()
            laser_central = Laser(self.rect.midtop, -10, 0, 'bala_canhao')
            laser_esquerdo = Laser(self.rect.midtop, -10, -2, 'bala_canhao')
            laser_direito = Laser(self.rect.midtop, -10, -2, 'bala_canhao')
            self.lasers.add(laser_central, laser_esquerdo, laser_direito)
            if teclas[pygame.K_z]:
                tiro_especial = Laser(self.rect.midtop, -8, 0, 'bala_canhao')
                self.lasers.add(tiro_especial)
