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
        pygame.mixer.init()
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
        self.imagem_moedas = pygame.transform.scale(pygame.image.load('./imagens/moeda.png'), (50, 50)).convert_alpha()
        self.imagem_vida = pygame.transform.scale(pygame.image.load('./imagens/vida.png'), (34, 34)).convert_alpha()
        self.imagem_rum = pygame.transform.scale(pygame.image.load('./imagens/rum.png'), (90, 90)).convert_alpha()
        self.imagem_sucata = pygame.transform.scale(pygame.image.load('./imagens/sucata.png'), (45, 45)).convert_alpha()
        self.imagem_inimigos_mortos = pygame.transform.scale(pygame.image.load('./imagens/inimigos_mortos.png'),
                                                             (38, 38)).convert_alpha()
        self.imagem_fundo_menu_original = pygame.image.load('./imagens/fundo.jpg').convert()
        self.imagem_fundo_menu = pygame.transform.scale(self.imagem_fundo_menu_original,
                                                        (self.largura_tela, self.altura_tela))
        self.imagem_fundo_perda_original = pygame.image.load('./imagens/gameover.jpg').convert()
        self.imagem_fundo_perda = pygame.transform.scale(self.imagem_fundo_perda_original,
                                                         (self.largura_tela, self.altura_tela))
        self.imagem_fundo_vitoria_original = pygame.image.load('./imagens/vitoria.jpg').convert()
        self.imagem_fundo_vitoria = pygame.transform.scale(self.imagem_fundo_vitoria_original,
                                                           (self.largura_tela, self.altura_tela))
        self.fonte_menu = pygame.font.Font('./imagens/Crang.ttf', 90)  # Tamanho ajustado
        self.fonte_menor = pygame.font.Font('./imagens/Crang.ttf', 60)
        self.fonte_informaçao = pygame.font.Font('./imagens/Crang.ttf', 40)
        self.fonte_game_over = pygame.font.Font('./imagens/Crang.ttf', 60)

        self.player = Player(self.tela, self.largura_tela // 2 - 50, self.altura_tela - 350, self.largura_tela)
        self.inimigo_principal = Inimigos(0, 0, self.tela, self.velocidade_inimigo, self.imagem_inimigo)
        self.inimigos.append(self.inimigo_principal)
        self.fase = 'fase_1'
        self.inimigos_por_nivel = 19
        self.inimigos_vivos = 20
        self.intervalo_tempo = 2000
        self.velocidade_tiro_inimigo = 8
        self.boss = Boss(0, 0)
        self.tiro_eespecial = False

        pygame.mixer.music.load('musica_jogo.mp3')
        pygame.mixer.music.play(-1)

    def desenhar_menu(self):
        self.tela.blit(self.imagem_fundo_menu, (0, 0))  # Desenha o fundo do menu

        # Mensagem de título
        titulo = "SEA MONSTERS"
        texto_titulo = self.fonte_menu.render(titulo, True, (0, 0, 0))  # Fonte e cor do texto
        largura_titulo = texto_titulo.get_width()
        altura_titulo = texto_titulo.get_height()
        pos_x_titulo = self.largura_tela // 2 - largura_titulo // 2
        pos_y_titulo = 100  # Ajuste o valor para mover o título mais para baixo

        # Mensagem de instrução
        instrucoes = "aperte enter para começar"
        texto_instrucoes = self.fonte_menor.render(instrucoes, True, (255, 255, 255))  # Fonte e cor do texto
        largura_instrucoes = texto_instrucoes.get_width()
        altura_instrucoes = texto_instrucoes.get_height()
        pos_x_instrucoes = self.largura_tela // 2 - largura_instrucoes // 2
        pos_y_instrucoes = self.altura_tela // 2 - altura_instrucoes // 2  # Centro vertical

        # Instruções de controle
        controle_titulo = "CONTROLES"
        texto_controle_titulo = self.fonte_menor.render(controle_titulo, True, (255, 255, 255))
        largura_controle_titulo = texto_controle_titulo.get_width()
        altura_controle_titulo = texto_controle_titulo.get_height()
        pos_x_controle_titulo = self.largura_tela // 2 - largura_controle_titulo // 2
        pos_y_controle_titulo = self.altura_tela - 300  # Ajuste o valor para posicionar a seção de controles

        controle_mover_direita = "Movimento: seta direita p direita, seta esquerda p esquerda"
        controle_atirar = "Atirar: espaço"
        controle_ataque = "Ataque especial: Z"

        texto_controle_mover_direita = self.fonte_informaçao.render(controle_mover_direita, True, (255, 255, 255))
        texto_controle_atirar = self.fonte_informaçao.render(controle_atirar, True, (255, 255, 255))
        texto_controle_ataque = self.fonte_informaçao.render(controle_ataque, True, (255, 255, 255))

        largura_controle_mover_direita = texto_controle_mover_direita.get_width()
        largura_controle_atirar = texto_controle_atirar.get_width()
        largura_controle_ataque = texto_controle_ataque.get_width()

        altura_controle_mover_direita = texto_controle_mover_direita.get_height()
        altura_controle_atirar = texto_controle_atirar.get_height()
        altura_controle_ataque = texto_controle_ataque.get_height()

        pos_x_controle_mover_direita = self.largura_tela // 2 - largura_controle_mover_direita // 2
        pos_x_controle_atirar = self.largura_tela // 2 - largura_controle_atirar // 2
        pos_x_controle_ataque = self.largura_tela // 2 - largura_controle_ataque // 2

        pos_y_controle_mover_direita = pos_y_controle_titulo + altura_controle_titulo + 20
        pos_y_controle_atirar = pos_y_controle_mover_direita + altura_controle_mover_direita + 10
        pos_y_controle_ataque = pos_y_controle_atirar + altura_controle_atirar + 10

        # Desenha o texto na tela
        self.tela.blit(texto_titulo, (pos_x_titulo, pos_y_titulo))
        self.tela.blit(texto_instrucoes, (pos_x_instrucoes, pos_y_instrucoes))

        # Desenha as instruções de controle
        self.tela.blit(texto_controle_titulo, (pos_x_controle_titulo, pos_y_controle_titulo))
        self.tela.blit(texto_controle_mover_direita, (pos_x_controle_mover_direita, pos_y_controle_mover_direita))
        self.tela.blit(texto_controle_atirar, (pos_x_controle_atirar, pos_y_controle_atirar))
        self.tela.blit(texto_controle_ataque, (pos_x_controle_ataque, pos_y_controle_ataque))

        pygame.display.flip()

    def desenhar_perda(self, ):
        self.tela.blit(self.imagem_fundo_perda, (0, 0))  # Desenha o fundo da tela de Game Over

        # Mensagem de Game Over
        game_over_texto = "GAME OVER"
        texto_game_over = self.fonte_menu.render(game_over_texto, True, (255, 0, 0))  # Fonte e cor do texto
        largura_game_over = texto_game_over.get_width()
        altura_game_over = texto_game_over.get_height()
        pos_x_game_over = self.largura_tela // 2 - largura_game_over // 2
        pos_y_game_over = self.altura_tela // 2 - altura_game_over // 2 - 50  # Centralizado e um pouco mais acima

        # Mensagem de instrução para reiniciar ou sair
        instrucoes_game_over = "aperte enter para reiniciar ou esc para sair"
        texto_instrucoes_game_over = self.fonte_menor.render(instrucoes_game_over, True,
                                                             (255, 255, 255))  # Fonte e cor do texto
        largura_instrucoes_game_over = texto_instrucoes_game_over.get_width()
        altura_instrucoes_game_over = texto_instrucoes_game_over.get_height()
        pos_x_instrucoes_game_over = self.largura_tela // 2 - largura_instrucoes_game_over // 2
        pos_y_instrucoes_game_over = self.altura_tela // 2 + altura_game_over // 2 + 20  # Centralizado e um pouco mais abaixo

        # Desenha o texto na tela
        self.tela.blit(texto_game_over, (pos_x_game_over, pos_y_game_over))
        self.tela.blit(texto_instrucoes_game_over, (pos_x_instrucoes_game_over, pos_y_instrucoes_game_over))

        pygame.display.flip()

    def desenhar_vitoria(self):
        self.tela.blit(self.imagem_fundo_vitoria, (0, 0))  # Desenha o fundo da tela de Vitória

        # Mensagem de Vitória
        vitoria_texto = "Parabéns! Você ganhou"
        texto_vitoria = self.fonte_menu.render(vitoria_texto, True, (0, 255, 0))  # Fonte e cor do texto
        largura_vitoria = texto_vitoria.get_width()
        altura_vitoria = texto_vitoria.get_height()
        pos_x_vitoria = self.largura_tela // 2 - largura_vitoria // 2
        pos_y_vitoria = self.altura_tela // 2 - altura_vitoria // 2 - 50  # Centralizado e um pouco mais acima

        # Mensagem de instrução para reiniciar ou sair
        instrucoes_vitoria = "aperte enter para reiniciar ou esc para sair"
        texto_instrucoes_vitoria = self.fonte_menor.render(instrucoes_vitoria, True,
                                                           (255, 255, 255))  # Fonte e cor do texto
        largura_instrucoes_vitoria = texto_instrucoes_vitoria.get_width()
        altura_instrucoes_vitoria = texto_instrucoes_vitoria.get_height()
        pos_x_instrucoes_vitoria = self.largura_tela // 2 - largura_instrucoes_vitoria // 2
        pos_y_instrucoes_vitoria = self.altura_tela // 2 + altura_vitoria // 2 + 20  # Centralizado e um pouco mais abaixo

        # Desenha o texto na tela
        self.tela.blit(texto_vitoria, (pos_x_vitoria, pos_y_vitoria))
        self.tela.blit(texto_instrucoes_vitoria, (pos_x_instrucoes_vitoria, pos_y_instrucoes_vitoria))

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
        self.tela.blit(self.imagem_rum, self.imagem_rum.get_rect(topleft=(1645 + 20, 50 - 20)))
        self.tela.blit(self.imagem_vida, self.imagem_vida.get_rect(topleft=(1390 + 20, 75 - 20)))
        self.tela.blit(self.imagem_sucata, self.imagem_sucata.get_rect(topleft=(1480 + 20, 65 - 20)))
        self.tela.blit(self.imagem_inimigos_mortos, self.imagem_inimigos_mortos.get_rect(topleft=(1750 + 20, 70 - 20)))
        self.tela.blit(self.imagem_moedas, self.imagem_moedas.get_rect(topleft=(1580 + 20, 65 - 20)))

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
                        self.inimigos_vivos -= 1
                        self.contador_inimigos_mortos += 1  # Incrementar contador
                        morte_inimigo_som = pygame.mixer.Sound('morte_inimigo_som.wav')
                        morte_inimigo_som.set_volume(0.2)
                        morte_inimigo_som.play()

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
                        self.inimigos_vivos -= 1
                        self.contador_inimigos_mortos += 1  # Incrementar contador
                        self.matou = True

                        for explosao in self.explosoes[:]:
                            explosao.update()
                            self.tela.blit(explosao.image, explosao.rect)
                            explosao_som = pygame.mixer.Sound('explosão_som.wav')
                            explosao_som.play()
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
                self.inimigos_por_nivel -= 1
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
                dano_som = pygame.mixer.Sound('dano_som.wav')
                dano_som.play()

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
                    up_som = pygame.mixer.Sound('up_som.wav')
                    up_som.play()
                elif coletavel.tipo == 'canhao':
                    self.player.canhao = True
                    self.player.evolucao_canhao(self.player.canhao)
                    self.já_evoluiu2 = True
                    self.player.level_up_2()
                    up_som = pygame.mixer.Sound('up_som.wav')
                    up_som.play()
                elif coletavel.tipo == 'moeda':
                    print("Moeda coletada")
                    self.contador_moedas += 1
                    moeda_som = pygame.mixer.Sound('moeda_som.wav')
                    moeda_som.play()
                elif coletavel.tipo == 'sucata':
                    print("Sucata coletada")
                    self.contador_sucata += 1
                    self.player.receber_dano(1)
                    sucata_som = pygame.mixer.Sound('sucata_som.wav')
                    sucata_som.play()
                elif coletavel.tipo == 'rum':
                    print('Rum coletado')
                    self.contador_rum += 1
                    self.player.velocidade += 0.25
                    rum_som = pygame.mixer.Sound('rum_som.wav')
                    rum_som.play()
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
                            self.player = Player(self.tela, self.largura_tela // 2 - 50, self.altura_tela - 350,
                                                 self.largura_tela)
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
                            self.player = Player(self.tela, self.largura_tela // 2 - 50, self.altura_tela - 350,
                                                 self.largura_tela)
                            self.inimigo_principal = Inimigos(0, 0, self.tela, self.velocidade_inimigo,
                                                              self.imagem_inimigo)
                            self.inimigos.append(self.inimigo_principal)
                            self.fase = 'fase_1'
                            self.inimigos_por_nivel = 19
                            self.inimigos_vivos = 20
                            self.intervalo_tempo = 2000
                            self.velocidade_tiro_inimigo = 8
                            self.boss = Boss(0, 0)
                            self.tiro_eespecial = False
                            self.lista_tiro_especial = []
                            self.explosoes = []

            if self.menu:
                self.desenhar_menu()

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
                            if teclas[pygame.K_z] and self.contador_moedas >= 12:
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
                        self.boss.movimento(self.largura_tela)
                        self.boss.atirar()

                    if self.boss.shoot:
                        laser_central = Laser(self.boss.rect.center, 10, 0, 'fogo')
                        laser_esquerdo = Laser(self.boss.rect.center, 10, -2, 'fogo')
                        laser_direito = Laser(self.boss.rect.center, 10, 2, 'fogo')
                        self.lista_lasers_inimigo.append(laser_central)
                        self.lista_lasers_inimigo.append(laser_esquerdo)
                        self.lista_lasers_inimigo.append(laser_direito)

                    if self.boss.inimigo:
                        novo_inimigo = self.inimigo_principal.gerar_novo_inimigo(self.velocidade_inimigo,
                                                                                 self.imagem_inimigo)
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

                #pygame.mixer.music.stop()

            elif self.vitoria:
                self.jogo = False
                self.desenhar_vitoria()
            elif not self.jogo:
                self.desenhar_perda()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
