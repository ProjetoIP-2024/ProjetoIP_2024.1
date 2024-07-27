import pygame
from sys import exit
from inimigo import Inimigos
from player import Player
from obstaculos import Objeto
from laser import Laser
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

lista_lasers = []  # Lista para armazenar os lasers disparados pelo jogador
lista_lasers_inimigo = []
lista_objetos = []  # Lista para armazenar objetos

def desenhar_menu(mensagem):
    tela.fill((0, 0, 0))  # Cor de fundo do menu
    fonte = pygame.font.SysFont(None, 74)
    texto = fonte.render(mensagem, True, (255, 255, 255))
    tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))
    pygame.display.flip()

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
                    elif not jogo:
                        jogo = True
                        menu = False
                        inimigos = [Inimigos(0, 0, tela)]  # Cria um novo inimigo principal e adiciona à lista
                        player = Player(tela, largura_tela // 2 - 50, altura_tela - 350, largura_tela)
                        lista_lasers = []
                        lista_objetos = []
                        lista_lasers_inimigo = []
                        tempo_ultimo_inimigo = pygame.time.get_ticks()
                        ultimo_tempo = pygame.time.get_ticks()
                        ultimo_tiro = 0
                        ultimo_tiro_inimigo = 0
        
    if menu:
        desenhar_menu("BEM VINDO! APERTE ENTER PARA COMEÇAR")
    
    elif jogo:
        tela.fill('Blue')

        player.control()  # Controla o jogador e dispara lasers
        player.desenhar_vida()

        if player.shoot:  # Se o jogador estiver atirando
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - ultimo_tiro >= 300:
                player.shoot = False  # Reinicia o flag de tiro do jogador
                laser = Laser(player.rect.midtop, -8, 'canhao')  # Cria um laser na posição do jogador
                lista_lasers.append(laser)  # Adiciona o laser à lista de lasers
                ultimo_tiro = tempo_atual

        # Atualiza os lasers disparados pelo jogador e verifica colisão com inimigos
        for laser in lista_lasers[:]:
            laser.update()
            # Verifica colisão com inimigos
            for inimigo in inimigos[:]:
                if pygame.sprite.collide_rect(laser, inimigo):
                    inimigos.remove(inimigo)  # Remove o inimigo do grupo
                    # Verifica se o laser está na lista antes de tentar removê-lo
                    if laser in lista_lasers:
                        lista_lasers.remove(laser)  # Remove o laser da lista
                    num_aleatorio = randint(1, 100)
                    matou = True
            # Verifica colisão com objetos
            for objeto in lista_objetos[:]:
                if pygame.sprite.collide_rect(laser, objeto):
                    lista_lasers.remove(laser)  # Remove o laser da lista

        for inimigo in inimigos[:]:
            inimigo.mover()
            inimigo.gerar_inimigos()
            if inimigo.atirar():
                laser = Laser(inimigo.rect.midbottom, 8, 'fogo')  # Cria um laser que se move para baixo
                lista_lasers_inimigo.append(laser)  # Adiciona o laser à lista de lasers

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
        
        for laser in lista_lasers_inimigo[:]:
            laser.update()
            tela.blit(laser.sprite, laser.rect)
            if laser.rect.y > tela.get_height():  # Remove lasers que saem da tela
                lista_lasers_inimigo.remove(laser)
            elif pygame.sprite.collide_rect(laser, player):
                player.receber_dano(1)
                lista_lasers_inimigo.remove(laser)
                
        for objeto in lista_objetos:
            objeto.draw()

        for laser in lista_lasers:
            tela.blit(laser.sprite, laser.rect)  # Desenha os lasers na tela

        if matou:
            if 1 == num_aleatorio and not já_evoluiu1:#Item de maior raridade, garante o melho canhão disponível ao player
                player.canhao_melhor = True
                player.evolucao_canhao_melhor(player.canhao_melhor)
                já_evoluiu1 = True
            elif 1 < num_aleatorio <= 5 and not já_evoluiu2 and not já_evoluiu1:#Se já tiver a evolução melhor, não evolui para esse
                player.canhao = True#Itens raros, que garantem canhões melhores do que o inicial
                player.evolucao_canhao(player.canhao)
                já_evoluiu2 = True
            elif 5 < num_aleatorio <= 50:#Drop de moedas, para desbloquear outras coisas
                print(f"Moedas = {num_aleatorio}")
            elif 50 < num_aleatorio <= 100:#Drop de sucata, um coletável extra que não tem tanta importância
                print(f"Sucata = {num_aleatorio}") 
            num_aleatorio = 0
            matou = False


        player.draw()  # Desenha o jogador na tela

        player.shoot = False

        if not player.receber_dano(0):
            jogo = False

        pygame.display.flip()
        fps.tick(60)
    elif not jogo:
        desenhar_menu('VOCÊ PERDEU! APERTE ENTER PARA REINICIAR OU ESC PARA FECHAR')
