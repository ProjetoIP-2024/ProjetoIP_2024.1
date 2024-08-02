import pygame
class Explosao(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (1000, 1000), 1000)  # Desenha um círculo vermelho com transparência
        self.rect = self.image.get_rect(center=center)
        self.timer = 30  # Duração da explosão em frames

    def update(self):
        while self.timer > 0:
            self.timer -= 1
            if self.timer <= 0:
                self.kill()