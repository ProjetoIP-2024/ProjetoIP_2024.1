import pygame
from sys import exit
from inimigo import Inimigos
from player import Player
from obstaculos import Objeto
from laser import Laser

pygame.init()

largura_tela = 1920
altura_tela = 1080
tela = pygame.display.set_mode((largura_tela, altura_tela))
print(tela)
fps = pygame.time.Clock()
jogo = True
inimigos = []
inimigo_principal = Inimigos(0, 0, tela)
inimigos.append(inimigo_principal)
player = Player(tela, largura_tela // 2 - 50, altura_tela - 350, largura_tela)

tempo_ultimo_inimigo = pygame.time.get_ticks()
ultimo_tempo = pygame.time.get_ticks()
ultimo_tiro = 0

lista_lasers = []  # Lista para armazenar os lasers disparados pelo jogador
lista_objetos = []  # Lista para armazenar objetos

while jogo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit() 

    tela.fill('Blue')

    player.control()  # Controla o jogador e dispara lasers
    if player.shoot:  # Se o jogador estiver atirando
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tiro >= 300:
            player.shoot = False  # Reinicia o flag de tiro do jogador
            laser = Laser(player.rect.midtop)  # Cria um laser na posição do jogador
            lista_lasers.append(laser)  # Adiciona o laser à lista de lasers
            ultimo_tiro = tempo_atual

    # Atualiza os lasers disparados pelo jogador e verifica colisão com inimigos
    for laser in lista_lasers[:]:
        laser.update()
        # Verifica colisão com inimigos
        for inimigo in inimigos[:]:
            if pygame.sprite.collide_rect(laser, inimigo):
                inimigos.remove(inimigo)  # Remove o inimigo do grupo
                lista_lasers.remove(laser)  # Remove o laser da lista
        # Verifica colisão com objetos
        for objeto in lista_objetos[:]:
            if pygame.sprite.collide_rect(laser, objeto):
                lista_lasers.remove(laser)  # Remove o laser da lista

    for inimigo in inimigos[:]:
        inimigo.mover()
        inimigo.gerar_inimigos()

    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_ultimo_inimigo >= 2000:
        novo_inimigo = inimigo_principal.gerar_novo_inimigo()
        inimigos.append(novo_inimigo)
        tempo_ultimo_inimigo = tempo_atual

    if tempo_atual - ultimo_tempo >= 1200:
        objeto = Objeto(tela, -230, 650, (255, 255, 255))
        lista_objetos.append(objeto)
        ultimo_tempo = tempo_atual

    for objeto in lista_objetos[:]:
        objeto.movimentacao()
        if objeto.rect.x > largura_tela:
            lista_objetos.remove(objeto)

    for objeto in lista_objetos:
        objeto.draw()

    for laser in lista_lasers:
        tela.blit(laser.image, laser.rect)  # Desenha os lasers na tela

    player.draw()  # Desenha o jogador na tela

    player.shoot = False

    pygame.display.flip()
    fps.tick(60)
