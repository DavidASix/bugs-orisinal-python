import pygame
import math
import constants as c

class Health:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health
        self.dot_radius = 10
        self.dot_spacing = 2

    def draw(self, screen):
        for i in range(self.max_health):
            color = (0, 255, 0) if i < self.current_health else (150, 150, 150)
            x = (self.dot_radius * 2 + self.dot_spacing) * i + 10
            pygame.draw.circle(screen, color, (x, 10), self.dot_radius)

    def lose_life(self):
        if self.current_health > 0:
            self.current_health -= 1
            sound = pygame.mixer.Sound('./assets/sounds/hit.mp3')
            sound.play()