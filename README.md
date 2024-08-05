Sea Monsters
## DESCRIÇÃO DO JOGO
Sea Monsters é um jogo inspirado no clássico Space Invaders, mas com uma temática diferente: o jogador controla um navio que deve, assim como no jogo clássico, matar inimigos(monstros do mar), tentando sobreviver. Simulando um ambiente marítimo, na perspectiva 2D e com um tamanho de tela igual à 1920x1080, Sea Monsters foi desenvolvido como trabalho final da disciplina de Introdução à Computação, da Universidade Federal de Pernambuco(UFPE).

## INTEGRANTES DO GRUPO E PARTICIPAÇÃO NO PROJETO
Henrique Xavier - Desenvolveu a estrutura e lógica do player – o objeto controlado pelo jogador – e também realizou contribuições para o jogo base e coletáveis e redação do README.md do projeto.
Ian Monteiro - Escreveu a classe dos itens coletáveis, com todo o seu funcionamento, e estruturação da classe dos inimigos, além de criar um menu para o jogo, bem como uma tela de fim de jogo(“Game Over”) e uma de vitória.
João Pedro Barbosa - Estruturou a lógica dos projéteis atirados pelo player, com todo o seu funcionamento e características secundárias, como aumento do número de tiros disparados – decorrente da evolução do jogador – e criação de um raio de explosão(“Dano em Área”). 
Manoel Villarim - Responsável pela estrutura base do jogo, assim como o funcionamento dos inimigos e seus atributos. Também desenvolveu a lógica das colisões presentes no projeto. Organizou a apresentação de slides e corrigiu bugs do jogo.
Ronaldo Felipe - Responsável pela organização das sprites utilizadas no decorrer do código e desenvolvimento dos obstáculos, além de introduzir efeitos sonoros ao jogo.
Thiago Moraes - Ajudou na programação e lógica do menu do jogo, bem como contribuiu para a implementação dos efeitos sonoros.

## FUNCIONAMENTO DO JOGO
Em Sea Monsters, o jogador controla um navio, com o desafio de eliminar os monstros que aparecem pelo caminho para, enfim, derrotar o boss que o espera no final. Para realizar isso, o player dispõe de um canhão, que pode ser melhorado durante o jogo.
	Para auxiliá-lo em sua jornada, itens coletáveis podem ser coletados ao derrotar inimigos. Eles consistem em: Moedas, que podem comprar um tiro especial; Rum, que aumenta a velocidade do navio, e canhões diferentes, que melhoram a jogabilidade, facilitando a eliminação dos monstros. Porém, os inimigos também podem liberar Sucata, coletável que infringe dano ao player.
Dessa maneira, mate o máximo de inimigos que conseguir e, no final, derrote o Boss que o espera!  

## CONTROLES DO JOGO
No menu inicial:
Tecla retorno(Enter) - Ao ser pressionada, ela dá início ao jogo, momento em que ocorre a mudança de tela para o jogo principal.
No jogo principal:
Tecla seta para a esquerda -  Esta tecla, ao ser pressionada, faz com que o player se desloque para a esquerda até chegar ao ponto onde a coordenada x do personagem, que está na posição (x,y) do plano, seja igual à 0.
Tecla seta para a direita - Esta tecla, ao ser pressionada, faz com que o player se desloque para a esquerda até chegar ao ponto onde a coordenada x do personagem, que está na posição (x,y) do plano, seja igual ao tamanho máximo da tela no respectivo eixo(1920) subtraído do comprimento do objeto player.
Tecla space(Espaço) - Ao ser pressionada, o player dispara um projétil(bala de canhão), que, ao colidir com um inimigo, mata-o e gera um derramamento de item.
Tecla z - Ao ser pressionada, o player pode disparar um tiro especial, mas apenas se o jogador possuir mais que um certo número de moedas(12).
No Game Over:
Tecla escape(Esc) - Quando Esc é pressionado, o jogo automaticamente é finalizado. Basicamente, o jogador decide parar de jogar o jogo.
Tecla return(Enter) - Ao pressionar Enter, o jogo é reiniciado, ou seja, o jogador perde e decide recomeçar a jogar.
ESTRUTURA DO PROJETO
jogo.py - É o arquivo principal do trabalho. Nele, encontram-se tanto o código central de funcionamento do jogo, dentro da classe Jogo, como as importações e lógica de organização das classes presentes em outros arquivos dentro da pasta.
player.py - Neste arquivo, encontra-se a lógica e o código de funcionamento do player, objeto controlado pelo jogador. É nele que são realizadas as evoluções citadas anteriormente, bem como a movimentação do objeto.
inimigo.py - É neste módulo que está armazenada a classe Inimigos, classe em que os inimigos são estruturados, com todas as suas características, iniciando o combate.
laser.py - Neste arquivo, é desenhado o projétil disparado pelo jogador, com diferentes níveis de acordo com o decorrer do jogo. É aqui que o player é possibilitado a eliminar os inimigos.
obstaculos.py - Neste módulo, encontra-se a classe Obstáculos, que consiste em barreiras(troncos), que incrementam o nível de dificuldade do jogo. 
coletavel.py - É aqui que há a classe dos Itens Coletáveis, constituindo um dos requisitos para o desenvolvimento do jogo. Aqui, o player pode visualizar o derramamento de moedas, sucata, rum e novos canhões, apenas desenhando os elementos.
boss.py - Neste módulo, encontra-se a estrutura que constrói a Classe Boss, que é o inimigo final do jogo. Derrotando-o, o jogador vence o jogo.

## DESAFIOS
Durante o desenvolvimento de Sea Monsters, enfrentamos diversos desafios. Dentre eles, destacamos dois:
Comunicação entre o grupo: Como decidimos trabalhar remotamente, cada um com seu computador e à distância, muitas vezes estivemos em situações em que houve falta de comunicação – um integrante não estava disponível para discutir assuntos relacionados ao projeto – e uma certa descoordenação entre o grupo, já que os códigos, mesmo que com as mesmas diretrizes e lógica, diferiam em alguns aspectos, dificultando o andamento do trabalho.
Sprites: Encontras as sprites certas foi um grande desafio ao grupo. Isso porque, por mais que houvesse diversas opções disponíveis, não foi fácil encontrar as que serviriam ao projeto, uma vez que nem todas atendiam aos requisitos desejados pela equipe.

## FERRAMENTAS DO JOGO
Biblioteca pygame - A biblioteca pygame foi utilizada como base para toda a construção do jogo. Foi através de suas funções pré-definidas que o projeto foi desenvolvido, desde usos delas na interface do projeto ao funcionamento de toda a estrutura interna que foi escrita pelos integrantes do grupo. 
Biblioteca sys - Biblioteca usada apenas para encerrar o jogo.
Biblioteca Random - Esta biblioteca foi utilizada com o objetivo de criar itens com geração aleatória. Para isso, utilizamos a função randint, que retorna um valor qualquer em um certo intervalo numérico definido. Com isso, foi possível utilizar esses valores retornados como método para aleatorizar a criação dos itens coletáveis presentes em Sea Monsters.
É importante ressaltar que também foram utilizados outros mecanismos para auxiliar no desenvolvimento do projeto. Tais mecanismos foram importantíssimos para Sea Monsters, pois, por meio deles, não seria possível adquirir informações extra e exemplos de outros jogos para que o grupo se inspirasse. Essas ferramentas são sites, como Building Space Invaders Using Pygame - Python, Creating Space Invaders in Pygame/Python e a Documentação do Pygame, para ajuda no desenvolvimento do código, OpenGameArt.org e Unscreen para sprites, além de programas de Inteligência Artificial(por exemplo, Chat GPT) e auxílio de monitores e professor.

## CONCEITOS APRENDIDOS NA DISCIPLINA QUE FORAM UTILIZADOS
Comandos condicionais - Os comandos de if, elif e else foram usados diversas vezes em Sea Monsters. Foi através deles que foi possível desenvolver praticamente todo o código.
Laços de Repetição - Os laços de repetição foram constantemente utilizados no projeto. Em especial, destaca-se a utilização do for, responsável pelo percorrimento das listas presentes no jogo.
Listas - As listas estão presentes no código. Por meio delas, foi possível iterar sobre os disparos e os inimigos, permitindo realizar as colisões entre os mesmos, bem como entre os disparos inimigos e o player.
Funções - Funções são essenciais ao desenvolvimento de qualquer código minimamente complexo. É através delas que é possível organizar o código, evitando repetições desnecessárias. Em Sea Monsters, esse mecanismo foi utilizado diversas vezes, seja para atribuir métodos às classes, seja para estruturar e garantir o funcionamento do jogo base, em jogo.py.
Tuplas - Tuplas foram utilizadas na passagem de parâmetros para as funções serem executadas, como valores que dão as características do objeto e funcionamento ao mesmo.
Programação Orientada a Objetos(POO) - A lógica do jogo foi inteiramente pensada com base nos conhecimentos adquiridos no estudo de POO. Com esse modelo de programação, foi possível desenvolver tudo o que foi escrito durante o desenvolvimento do projeto, constituindo a base de tudo o que há presente em Sea Monsters.
Módulos e Pacotes - Utilizamos tais mecanismos com o intuito de organizar melhor a estrutura do código, possibilitando uma melhor visualização das partes distintas que, juntas, formam o código principal. 

## O QUE FOI APRENDIDO
Durante o projeto, o grupo pode aprender diversos novos conceitos e formas de programação. Iniciar um trabalho baseado em Programação Orientada à Objetos, mas sem conhecimentos prévios sobre, foi algo que motivou o grupo à adquirir conhecimentos novos sobre tal área. Além disso, é notório que o grupo pode desenvolver uma visão mais evoluída em relação ao funcionamento de Classes e, principalmente, Funções, utilizadas em todo o código. 	
Ademais, saindo do mundo computacional, é possível afirmar que cada integrante do grupo pôde melhorar suas habilidades de trabalho em equipe e cooperação, realizando um projeto em que todos deveriam participar, com ideias e métodos de resolução distintos.

## REQUISITOS
Python 3.x;
Biblioteca Pygame(é possível instalar utilizando o comando, no terminal, pip install pygame).

## BIBLIOGRAFIA
Building Space Invaders Using Pygame - Python : GeeksforGeeks. (2022, December 6). Building space invaders using pygame - python. https://www.geeksforgeeks.org/building-space-invaders-using-pygame-python/ 
OpenGameArts.org : food_please on 20 February 2024 - 4:19pm, withthelove on 9 June 2023 - 8:54am, MedicineStorm on 6 October 2022 - 8:52pm, MedicineStorm on 6 April 2022 - 9:53am, & MedicineStorm on 30 January 2022 - 9:13am. (n.d.). OpenGameArt.org. https://opengameart.org/ 
Unscreen : Kaleido. (n.d.). Remove video background. Unscreen. https://www.unscreen.com/ 
Creating Space Invaders in Pygame/Python : Creating space invaders in pygame/python. YouTube. (2021, July 29). https://youtu.be/o-6pADy5Mdg?si=d7QFsGwVXoM3S2n3 
Chat GPT : CHATGPT: Get instant answers, find inspiration, learn something new. (n.d.). https://chatgpt.com/ 
Documentação do Pygame : Pygame front page¶. Pygame Front Page - pygame v2.6.0 documentation. (n.d.). https://www.pygame.org/docs/ 



