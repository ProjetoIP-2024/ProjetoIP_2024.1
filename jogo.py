import pygame
from sys import exit
from inimigo import Inimigos
from player import Player
from obstaculos import Objeto
from laser import Laser
from coletavel import Coletavel
from boss import Boss
from explosao import Explosao
from random import randint

class Jogo:

    def __init__(self):
        pygame.init()
        self.largura_tela = 1920
        self.altura_tela = 1080
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        self.fps = pygame.time.Clock()
        self.velocidade_inimigo = 20
        self.inimigos = []
        self.lista_lasers = []
        self.lista_lasers_inimigo = []
        self.lista_objetos = []
        self.lista_coletaveis = []
        self.lista_tiro_especial = []
        self.explosoes = []
        self.contador_moedas = 0
        self.contador_sucata = 0
        self.contador_rum = 0
        self.contador_inimigos_mortos = 0  # Novo contador
        self.jogo = False
        self.menu = True
        self.vitoria = False
        self.tempo_ultimo_inimigo = pygame.time.get_ticks()
        self.ultimo_tempo = pygame.time.get_ticks()
        self.ultimo_tiro = 0
        self.ultimo_tiro_inimigo = 0
        self.matou = False
        self.já_evoluiu1 = False
        self.já_evoluiu2 = False
        self.imagem_inimigo = 'inimigo'
        self.imagem_moedas = pygame.transform.scale(pygame.image.load('./imagens/moeda.png'), (50,50)).convert_alpha()
        self.imagem_vida = pygame.transform.scale(pygame.image.load('./imagens/vida.png'), (34,34)).convert_alpha()
        self.imagem_rum = pygame.transform.scale(pygame.image.load('./imagens/rum.png'), (90,90)).convert_alpha()
        self.imagem_sucata = pygame.transform.scale(pygame.image.load('./imagens/sucata.png'), (45,45)).convert_alpha()
        self.imagem_inimigos_mortos = pygame.transform.scale(pygame.image.load('./imagens/inimigos_mortos.png'), (38,38)).convert_alpha()
        self.player = Player(self.tela, self.largura_tela // 2 - 50, self.altura_tela - 350, self.largura_tela)
        self.inimigo_principal = Inimigos(0, 0, self.tela, self.velocidade_inimigo, self.imagem_inimigo)
        self.inimigos.append(self.inimigo_principal)
        self.fase = 'fase_1'
        self.inimigos_por_nivel = 19
        self.inimigos_vivos = 20
        self.intervalo_tempo = 2000
        self.velocidade_tiro_inimigo = 8
        self.boss = Boss(0,0)
        self.tiro_eespecial = False

    def desenhar_menu(self, mensagem):
        self.tela.fill((0, 0, 0))
        fonte = pygame.font.SysFont(None, 74)
        texto = fonte.render(mensagem, True, (255, 255, 255))
        self.tela.blit(texto, (self.largura_tela // 2 - texto.get_width() // 2, self.altura_tela // 2 - texto.get_height() // 2))
        pygame.display.flip()

    def desenhar_contadores(self):
        fonte = pygame.font.SysFont(None, 36)
        contador_vidas = fonte.render(f"{self.player.vida + 1}", True, (255, 255, 255))
        contador_moedas = fonte.render(f"{self.contador_moedas}", True, (255, 255, 255))
        contador_sucatas = fonte.render(f"{self.contador_sucata}", True, (255, 255, 255))
        contador_rum = fonte.render(f"{self.contador_rum}", True, (255, 255, 255))
        contador_inimigos_mortos = fonte.render(f"{self.contador_inimigos_mortos}", True, (255, 255, 255))
        if self.fase == "fase_1":
            fase = fonte.render(f"Fase 1", True, (255, 255, 255))
        elif self.fase == "fase_2":
            fase = fonte.render(f"Fase 2", True, (255, 255, 255))
        elif self.fase == "fase_3":
            fase = fonte.render(f"Fase 3", True, (255, 255, 255))
        if self.fase == "boss":
            fase = fonte.render(f"BOSS", True, (255, 255, 255))
        self.tela.blit(self.imagem_rum, self.imagem_rum.get_rect(topleft = (1645 + 20, 50 - 20)))
        self.tela.blit(self.imagem_vida, self.imagem_vida.get_rect(topleft = (1390 + 20, 75 - 20)))
        self.tela.blit(self.imagem_sucata, self.imagem_sucata.get_rect(topleft = (1480 + 20, 65 - 20)))
        self.tela.blit(self.imagem_inimigos_mortos, self.imagem_inimigos_mortos.get_rect(topleft = (1750 + 20, 70 - 20)))
        self.tela.blit(self.imagem_moedas, self.imagem_moedas.get_rect(topleft = (1580 + 20, 65 - 20)))
        
        self.tela.blit(contador_vidas, (1448 + 20, 80 - 20))
        self.tela.blit(contador_moedas, (1630 + 20, 80 - 20))
        self.tela.blit(contador_sucatas, (1540 + 20, 80 - 20))
        self.tela.blit(contador_rum, (1720 + 20, 80 - 20))
        self.tela.blit(contador_inimigos_mortos, (1800 + 20, 80 - 20))  # Novo contador
        
        self.tela.blit(fase, (1740 + 20, 122 - 20))  # Novo contador


    def checar_colisoes(self):
        for laser in self.lista_lasers[:]:
            laser.update()
            for inimigo in self.inimigos[:]:
                if pygame.sprite.collide_rect(laser, inimigo):
                    if laser in self.lista_lasers:
                        self.inimigos.remove(inimigo)
                        self.lista_lasers.remove(laser)
                        self.inimigos_vivos -=1
                        self.contador_inimigos_mortos += 1  # Incrementar contador

                    num_aleatorio = randint(1, 100)
                    self.matou = True
                    print(num_aleatorio)

                    if 1 <= num_aleatorio <= 3 and not self.já_evoluiu1 and self.já_evoluiu2:
                        tipo_coletavel = 'canhao_melhor'
                    elif 1 <= num_aleatorio <= 3 and not self.já_evoluiu2 and not self.já_evoluiu1:
                        tipo_coletavel = 'moeda'
                    elif 3 < num_aleatorio <= 7 and not self.já_evoluiu2 and not self.já_evoluiu1:
                        tipo_coletavel = 'canhao'
                    elif 3 < num_aleatorio <= 7 and self.já_evoluiu2:
                        tipo_coletavel = 'moeda'
                    elif 7 < num_aleatorio <= 57:
                        tipo_coletavel = 'moeda'
                    elif 57 < num_aleatorio <= 92:
                        tipo_coletavel = 'sucata'
                    elif 92 < num_aleatorio <= 100:
                        tipo_coletavel = 'rum'
                    else:
                        tipo_coletavel = None

                    if tipo_coletavel:
                        coletavel = Coletavel(inimigo.rect.x, inimigo.rect.y, tipo_coletavel)
                        self.lista_coletaveis.append(coletavel)

            for objeto in self.lista_objetos[:]:
                if pygame.sprite.collide_rect(laser, objeto):
                    self.lista_lasers.remove(laser)
        if len(self.lista_tiro_especial) != 0:
            for laser in self.lista_tiro_especial[:]:
                laser.update()
                for inimigo in self.inimigos[:]:
                    if pygame.sprite.collide_rect(laser, inimigo):
                        explosao = Explosao(laser.rect.center)  
                        self.inimigos.remove(inimigo)
                        self.lista_tiro_especial.remove(laser)
                        self.explosoes.append(explosao)
                        self.inimigos_vivos -=1
                        self.contador_inimigos_mortos += 1  # Incrementar contador
                        self.matou = True
                    
                        for explosao in self.explosoes[:]:
                            explosao.update()
                            self.tela.blit(explosao.image, explosao.rect)
                            if explosao.update():
                                self.explosoes.remove(explosao)
                            for inimigo in self.inimigos[:]:
                                if pygame.sprite.collide_rect(explosao, inimigo):
                                        self.inimigos.remove(inimigo)
                                        self.inimigos_vivos -= 1
                                        self.contador_inimigos_mortos += 1


    def atualizar_jogo(self):
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.tempo_ultimo_inimigo >= self.intervalo_tempo:
            if self.inimigos_por_nivel > 0:
                novo_inimigo = self.inimigo_principal.gerar_novo_inimigo(self.velocidade_inimigo, self.imagem_inimigo)
                self.inimigos.append(novo_inimigo)
                self.tempo_ultimo_inimigo = tempo_atual
                self.inimigos_por_nivel -=1
            else:
                if self.inimigos_vivos == self.inimigos_por_nivel:
                    if self.fase == 'fase_1':
                        self.fase = 'fase_2'
                        self.velocidade_inimigo = 40
                        self.inimigos_por_nivel = 40
                        self.inimigos_vivos = 40
                        self.intervalo_tempo = 1200
                        self.velocidade_tiro_inimigo = 12
                        self.imagem_inimigo = 'shark(1)'
                    elif self.fase == 'fase_2':
                        self.fase = 'fase_3'
                        self.velocidade_inimigo = 55
                        self.inimigos_por_nivel = 50
                        self.inimigos_vivos = 50
                        self.intervalo_tempo = 800
                        self.velocidade_tiro_inimigo = 18
                        self.imagem_inimigo = 'lula'
                    elif self.fase == 'fase_3':
                        self.fase = 'boss'
                        self.velocidade_inimigo = 55
                        self.inimigos_por_nivel = 0
                        self.inimigos_vivos = 0
                        self.intervalo_tempo = 1200
                        self.velocidade_tiro_inimigo = 18


        if tempo_atual - self.ultimo_tempo >= 1200:
            objeto = Objeto(-230, 650, self.tela)
            self.lista_objetos.append(objeto)
            self.ultimo_tempo = tempo_atual

    def processar_lasers_inimigo(self):
        for laser in self.lista_lasers_inimigo[:]:
            laser.update()
            self.tela.blit(laser.sprite, laser.rect)
            if laser.rect.y > self.tela.get_height():
                self.lista_lasers_inimigo.remove(laser)
            elif pygame.sprite.collide_rect(laser, self.player):
                self.player.receber_dano(1)
                self.lista_lasers_inimigo.remove(laser)
    
    def processar_coletaveis(self):
        for coletavel in self.lista_coletaveis[:]:
            coletavel.update()
            self.tela.blit(coletavel.sprite, coletavel.rect)
            if coletavel.rect.y > self.altura_tela:
                self.lista_coletaveis.remove(coletavel)
            elif pygame.sprite.collide_rect(coletavel, self.player):
                if coletavel.tipo == 'canhao_melhor':
                    self.player.canhao_melhor = True
                    self.já_evoluiu1 = True
                    self.player.evolucao_canhao_melhor(self.player.canhao_melhor)
                    self.player.level_up_3()
                elif coletavel.tipo == 'canhao':
                    self.player.canhao = True 
                    self.player.evolucao_canhao(self.player.canhao)
                    self.já_evoluiu2 = True
                    self.player.level_up_2()
                elif coletavel.tipo == 'moeda':
                    print("Moeda coletada")
                    self.contador_moedas += 1
                elif coletavel.tipo == 'sucata':
                    print("Sucata coletada")
                    self.contador_sucata += 1
                    self.player.receber_dano(1)
                elif coletavel.tipo == 'rum':
                    print('Rum coletado')
                    self.contador_rum += 1
                    self.player.velocidade += 0.25
                self.lista_coletaveis.remove(coletavel)

    def executar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit() 
                    elif event.key == pygame.K_RETURN:
                        if self.menu:
                            self.menu = False
                            self.jogo = True
                            self.inimigos = [Inimigos(0, 0, self.tela, self.velocidade_inimigo, self.imagem_inimigo)]
                            self.player = Player(self.tela, self.largura_tela // 2 - 50, self.altura_tela - 350, self.largura_tela)
                            self.lista_lasers = []
                            self.lista_lasers_inimigo = []
                            self.lista_objetos = []
                            self.lista_coletaveis = []
                            self.contador_moedas = 0
                            self.contador_sucata = 0
                            self.contador_rum = 0
                            self.tempo_ultimo_inimigo = pygame.time.get_ticks()
                            self.ultimo_tempo = pygame.time.get_ticks()
                            self.ultimo_tiro = 0
                            self.ultimo_tiro_inimigo = 0
                        elif not self.jogo:
                            self.jogo = True
                            self.menu = False
                            self.largura_tela = 1920
                            self.altura_tela = 1080
                            self.fps = pygame.time.Clock()
                            self.velocidade_inimigo = 20
                            self.inimigos = []
                            self.lista_lasers = []
                            self.lista_lasers_inimigo = []
                            self.lista_objetos = []
                            self.lista_coletaveis = []
                            self.contador_moedas = 0
                            self.contador_sucata = 0
                            self.contador_rum = 0
                            self.contador_inimigos_mortos = 0  # Novo contador
                            self.vitoria = False
                            self.tempo_ultimo_inimigo = pygame.time.get_ticks()
                            self.ultimo_tempo = pygame.time.get_ticks()
                            self.ultimo_tiro = 0
                            self.ultimo_tiro_inimigo = 0
                            self.matou = False
                            self.já_evoluiu1 = False
                            self.já_evoluiu2 = False
                            self.imagem_inimigo = 'inimigo'
                            self.player = Player(self.tela, self.largura_tela // 2 - 50, self.altura_tela - 350, self.largura_tela)
                            self.inimigo_principal = Inimigos(0, 0, self.tela, self.velocidade_inimigo, self.imagem_inimigo)
                            self.inimigos.append(self.inimigo_principal)
                            self.fase = 'fase_1'
                            self.inimigos_por_nivel = 19
                            self.inimigos_vivos = 20
                            self.intervalo_tempo = 2000
                            self.velocidade_tiro_inimigo = 8
                            self.boss = Boss(0,0)
                            self.tiro_eespecial = False
                            self.lista_tiro_especial = []
                            self.explosoes = []


            if self.menu:
                self.desenhar_menu("BEM VINDO! APERTE ENTER PARA COMEÇAR")

            elif self.jogo:
                self.tela.fill('Blue')

                self.player.control()
                self.player.desenhar_vida()

                if self.player.shoot:
                    teclas = pygame.key.get_pressed()
                    tempo_atual = pygame.time.get_ticks()
                    if tempo_atual - self.ultimo_tiro >= 300:
                        self.player.shoot = False
                        if self.player.level == 1:
                            laser = Laser(self.player.rect.midtop, -10, 0, 'bala_canhao')
                            self.lista_lasers.append(laser)
                        elif self.player.level == 2:
                            laser_central = Laser(self.player.rect.midtop, -10, 0, 'bala_canhao')
                            laser_esquerdo = Laser(self.player.rect.midtop, -10, -2, 'bala_canhao')
                            laser_direito = Laser(self.player.rect.midtop, -10, 2, 'bala_canhao')
                            self.lista_lasers.append(laser_central)
                            self.lista_lasers.append(laser_esquerdo)
                            self.lista_lasers.append(laser_direito)
                        elif self.player.level == 3:
                            if teclas[pygame.K_SPACE]:
                                laser_central = Laser(self.player.rect.midtop, -10, 0, 'bala_canhao')
                                laser_esquerdo = Laser(self.player.rect.midtop, -10, -2, 'bala_canhao')
                                laser_direito = Laser(self.player.rect.midtop, -10, 2, 'bala_canhao')
                                self.lista_lasers.append(laser_central)
                                self.lista_lasers.append(laser_esquerdo)
                                self.lista_lasers.append(laser_direito)
                            if  teclas[pygame.K_z] and self.contador_moedas >= 12:
                                self.tiro_eespecial = True
                                self.tiro_especial = Laser(self.player.rect.midtop, -8, 0, 'bomba')
                                self.lista_tiro_especial.append(self.tiro_especial)
                                self.contador_moedas -= 12

                        self.ultimo_tiro = tempo_atual

                self.checar_colisoes()

                for inimigo in self.inimigos[:]:
                    inimigo.mover()
                    inimigo.gerar_inimigos()
                    if inimigo.atirar():
                        laser = Laser(inimigo.rect.midbottom, self.velocidade_tiro_inimigo, 0, 'fogo')
                        self.lista_lasers_inimigo.append(laser)

                self.atualizar_jogo()

                for objeto in self.lista_objetos[:]:
                    objeto.movimentacao()
                    if objeto.rect.x > self.largura_tela:
                        self.lista_objetos.remove(objeto)
                
                self.processar_lasers_inimigo()
                self.processar_coletaveis()

                for objeto in self.lista_objetos:
                    objeto.draw()

                for laser in self.lista_lasers:
                    self.tela.blit(laser.sprite, laser.rect)

                self.player.draw()
                self.desenhar_contadores()

                self.player.shoot = False

                if not self.player.receber_dano(0):
                    self.jogo = False

                for inimigo in self.inimigos:
                    if pygame.sprite.collide_rect(inimigo, self.player):
                        self.jogo = False

                if self.fase == 'boss':
                    if self.jogo:
                        self.boss.desenhar_boss(self.tela)
                        self.boss.movimento(self.largura_tela )
                        self.boss.atirar()

                    if self.boss.shoot:
                        laser_central = Laser(self.boss.rect.center, 10, 0, 'fogo')
                        laser_esquerdo = Laser(self.boss.rect.center, 10, -2, 'fogo')
                        laser_direito = Laser(self.boss.rect.center, 10, 2, 'fogo')
                        self.lista_lasers_inimigo.append(laser_central)
                        self.lista_lasers_inimigo.append(laser_esquerdo)
                        self.lista_lasers_inimigo.append(laser_direito)

                    if self.boss.inimigo:
                        novo_inimigo = self.inimigo_principal.gerar_novo_inimigo(self.velocidade_inimigo, self.imagem_inimigo)
                        self.inimigos.append(novo_inimigo)     

                    
                    if self.boss.receber_dano(0):
                        self.vitoria = True

                    for laser in self.lista_lasers[:]:
                        if pygame.sprite.collide_rect(laser, self.boss):
                            self.boss.receber_dano(1)
                            self.lista_lasers.remove(laser)
                    
                    if len(self.lista_tiro_especial) != 0:
                        for laser in self.lista_tiro_especial[:]:
                            laser.update()
                            if pygame.sprite.collide_rect(laser, self.boss):
                                explosao = Explosao(laser.rect.center)  
                                self.lista_tiro_especial.remove(laser)
                                self.explosoes.append(explosao)
                                self.boss.receber_dano(1)
                            
                                for explosao in self.explosoes[:]:
                                    explosao.update()
                                    self.tela.blit(explosao.image, explosao.rect)
                                    if explosao.update():
                                        self.explosoes.remove(explosao)
                                    if pygame.sprite.collide_rect(explosao, inimigo):
                                        self.boss.receber_dano(4)
                    
                for tiro in self.lista_tiro_especial:
                    self.tela.blit(tiro.sprite, tiro.rect)

                for tiro in self.lista_tiro_especial[:]:
                    for obstaculo in self.lista_objetos:
                        if pygame.sprite.collide_rect(tiro, obstaculo):
                            self.lista_tiro_especial.remove(tiro)


                self.boss.shoot = False
                pygame.display.flip()
                self.fps.tick(60)

            elif self.vitoria:
                self.jogo = False
                self.desenhar_menu('VITORIA')
            elif not self.jogo:
                self.desenhar_menu('VOCÊ PERDEU! APERTE ENTER PARA REINICIAR OU ESC PARA FECHAR')

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
