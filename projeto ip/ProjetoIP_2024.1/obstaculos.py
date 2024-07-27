import pygame as pg

class Objeto:
    def __init__(self, win, x, y, cor):
        self.win = win
        self.largura = 130
        self.altura = 20
        self.vel = 5 
        self.rect = pg.Rect(x, y, self.largura, self.altura)
        self.cor = cor

    def movimentacao(self):
        self.rect.x += self.vel

    def draw(self):
        pg.draw.rect(self.win, self.cor, (self.rect.x, self.rect.y, self.largura, self.altura))