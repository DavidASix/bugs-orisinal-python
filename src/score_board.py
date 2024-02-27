import pygame

class ScoreBoard:
    def __init__(self, font, screen_width):
        self.font = pygame.font.Font(font, 25)
        self.screen_width = screen_width
        self.score = 0

    def increase(self):
        self.score += 1

    def draw(self, screen):
        text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(text, (self.screen_width - text.get_width(), 0))