import pygame
from sys import exit
from inimigo import Inimigos
from player import Player
from obstaculos import Objeto
from laser import Laser
from coletavel import Coletavel  # Importa a nova classe Coletavel
from random import randint

pygame.init()

matou = False
já_evoluiu1 = False
já_evoluiu2 = False
largura_tela = 1920
altura_tela = 1080
tela = pygame.display.set_mode((largura_tela, altura_tela))
print(tela)
fps = pygame.time.Clock()
inimigos = []
inimigo_principal = Inimigos(0, 0, tela)
inimigos.append(inimigo_principal)
player = Player(tela, largura_tela // 2 - 50, altura_tela - 350, largura_tela)

tempo_ultimo_inimigo = pygame.time.get_ticks()
ultimo_tempo = pygame.time.get_ticks()
ultimo_tiro = 0
ultimo_tiro_inimigo = 0

lista_lasers = []
lista_lasers_inimigo = []
lista_objetos = []
lista_coletaveis = []  # Lista para armazenar os coletáveis

# Contadores de itens coletados
contador_moedas = 0
contador_sucata = 0

def desenhar_menu(mensagem):
    tela.fill((0, 0, 0))
    fonte = pygame.font.SysFont(None, 74)
    texto = fonte.render(mensagem, True, (255, 255, 255))
    tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))
    pygame.display.flip()

def desenhar_contadores():
    fonte = pygame.font.SysFont(None, 36)
    texto_vida = fonte.render(f"Vida: {player.vida}", True, (255, 0, 0))
    texto_moeda = fonte.render(f"Moedas: {contador_moedas}", True, (255, 255, 0))
    texto_sucata = fonte.render(f"Sucata: {contador_sucata}", True, (128, 128, 128))
    
    # Desenha o contador de vida no canto superior esquerdo
    tela.blit(texto_vida, (10, 10))
    # Desenha o contador de moedas abaixo do contador de vida
    tela.blit(texto_moeda, (10, 50))
    # Desenha o contador de sucata abaixo do contador de moedas
    tela.blit(texto_sucata, (10, 90))

jogo = False
menu = True
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
                if menu:
                    menu = False
                    jogo = True
                    inimigos = []
                    inimigo_principal = Inimigos(0, 0, tela)
                    inimigos.append(inimigo_principal)
                    lista_lasers = []
                    lista_lasers_inimigo = []
                    lista_objetos = []
                    lista_coletaveis = []  # Limpa a lista de coletáveis
                    contador_moedas = 0
                    contador_sucata = 0
                elif not jogo:
                    jogo = True
                    menu = False
                    inimigos = [Inimigos(0, 0, tela)]
                    player = Player(tela, largura_tela // 2 - 50, altura_tela - 350, largura_tela)
                    lista_lasers = []
                    lista_objetos = []
                    lista_lasers_inimigo = []
                    lista_coletaveis = []
                    tempo_ultimo_inimigo = pygame.time.get_ticks()
                    ultimo_tempo = pygame.time.get_ticks()
                    ultimo_tiro = 0
                    ultimo_tiro_inimigo = 0

    if menu:
        desenhar_menu("BEM VINDO! APERTE ENTER PARA COMEÇAR")

    elif jogo:
        tela.fill('Blue')

        player.control()
        player.desenhar_vida()

        if player.shoot:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - ultimo_tiro >= 300:
                player.shoot = False
                if player.level == 1:
                    laser = Laser(player.rect.midtop, -10, 0,  'bala_canhao')
                    lista_lasers.append(laser)
                elif player.level == 2:
                    laser_central = Laser(player.rect.midtop, -10, 0, 'bala_canhao')
                    laser_esquerdo = Laser(player.rect.midtop, -10, -2, 'bala_canhao')
                    laser_direito = Laser(player.rect.midtop, -10, 2, 'bala_canhao')
                    lista_lasers.append(laser_central)
                    lista_lasers.append(laser_esquerdo)
                    lista_lasers.append(laser_direito)
                elif player.level == 3:
                    laser_central = Laser(player.rect.midtop, -10, 0, 'bala_canhao')
                    laser_esquerdo = Laser(player.rect.midtop, -10, -2, 'bala_canhao')
                    laser_direito = Laser(player.rect.midtop, -10, 2, 'bala_canhao')
                    lista_lasers.append(laser_central)
                    lista_lasers.append(laser_esquerdo)
                    lista_lasers.append(laser_direito)

                ultimo_tiro = tempo_atual

        for laser in lista_lasers[:]:
            laser.update()
            for inimigo in inimigos[:]:
                if pygame.sprite.collide_rect(laser, inimigo):
                    inimigos.remove(inimigo)
                    if laser in lista_lasers:
                        lista_lasers.remove(laser)
                    
                    num_aleatorio = randint(1, 100)
                    matou = True
                    
                    if num_aleatorio == 1 and not já_evoluiu1:
                        tipo_coletavel = 'canhao_melhor'
                    elif 1 < num_aleatorio <= 5 and not já_evoluiu2 and not já_evoluiu1:
                        tipo_coletavel = 'canhao'
                    elif 5 < num_aleatorio <= 50:
                        tipo_coletavel = 'moeda'
                    elif 50 < num_aleatorio <= 100:
                        tipo_coletavel = 'sucata'
                    else:
                        tipo_coletavel = None

                    if tipo_coletavel:
                        coletavel = Coletavel(inimigo.rect.x, inimigo.rect.y, tipo_coletavel)
                        lista_coletaveis.append(coletavel)
    
            for objeto in lista_objetos[:]:
                if pygame.sprite.collide_rect(laser, objeto):
                    lista_lasers.remove(laser)

        for inimigo in inimigos[:]:
            inimigo.mover()
            inimigo.gerar_inimigos()
            if inimigo.atirar():
                laser = Laser(inimigo.rect.midbottom, 8, 0, 'fogo')
                lista_lasers_inimigo.append(laser)

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_inimigo >= 2000:
            novo_inimigo = inimigo_principal.gerar_novo_inimigo()
            inimigos.append(novo_inimigo)
            tempo_ultimo_inimigo = tempo_atual

        if tempo_atual - ultimo_tempo >= 1200:
            objeto = Objeto(-230, 650, tela)
            lista_objetos.append(objeto)
            ultimo_tempo = tempo_atual

        for objeto in lista_objetos[:]:
            objeto.movimentacao()
            if objeto.rect.x > largura_tela:
                lista_objetos.remove(objeto)
        
        for laser in lista_lasers_inimigo[:]:
            laser.update()
            tela.blit(laser.sprite, laser.rect)
            if laser.rect.y > tela.get_height():
                lista_lasers_inimigo.remove(laser)
            elif pygame.sprite.collide_rect(laser, player):
                player.receber_dano(1)
                lista_lasers_inimigo.remove(laser)
                
        for coletavel in lista_coletaveis[:]:
            coletavel.update()
            tela.blit(coletavel.sprite, coletavel.rect)
            if coletavel.rect.y > altura_tela:
                lista_coletaveis.remove(coletavel)
            elif pygame.sprite.collide_rect(coletavel, player):
                if coletavel.tipo == 'canhao_melhor':
                    player.canhao_melhor = True
                    já_evoluiu1 = True
                    player.evolucao_canhao_melhor(player.canhao_melhor)
                    player.level_up_3()
                elif coletavel.tipo == 'canhao':
                    player.canhao = True
                    player.evolucao_canhao(player.canhao)
                    já_evoluiu2 = True
                    player.level_up_2()
                elif coletavel.tipo == 'moeda':
                    print("Moeda coletada")
                    contador_moedas += 1  # Incrementa o contador de moedas
                elif coletavel.tipo == 'sucata':
                    print("Sucata coletada")
                    contador_sucata += 1  # Incrementa o contador de sucata
                    player.receber_dano(1)  # Perde 1 de vida ao coletar sucata
                lista_coletaveis.remove(coletavel)

        for objeto in lista_objetos:
            objeto.draw()

        for laser in lista_lasers:
            tela.blit(laser.sprite, laser.rect)

        player.draw()
        desenhar_contadores()  # Desenha os contadores na tela

        player.shoot = False

        if not player.receber_dano(0):
            jogo = False

        pygame.display.flip()
        fps.tick(60)
    elif not jogo:
        desenhar_menu('VOCÊ PERDEU! APERTE ENTER PARA REINICIAR OU ESC PARA FECHAR')
