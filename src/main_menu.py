import pygame
import sys
from game import Game

class MainMenu:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.start_button = pygame.Rect(200, 200, int(self.screen.get_width() / 3), 50)
        self.exit_button = pygame.Rect(200, 300, int(self.screen.get_width() / 3), 50)
        self.game = Game(screen)
        self.hover_button = False

    def draw(self):
        self.screen.fill((20, 20, 20))
        title = pygame.font.Font(None, 72).render("BUG GAME", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

        def btn_color(btn):
            if self.hover_button == btn:
                return (50, 50, 50)
            else:
                return (40, 40, 40)
        
        pygame.draw.rect(self.screen, btn_color(self.start_button), self.start_button)
        start_text = pygame.font.Font(None, 26).render("Start Game", True, (255, 255, 255))
        self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2, self.start_button.centery - start_text.get_height() // 2))

        pygame.draw.rect(self.screen, btn_color(self.exit_button), self.exit_button)
        exit_text = pygame.font.Font(None, 26).render("Exit", True, (255, 255, 255))
        self.screen.blit(exit_text, (self.exit_button.centerx - exit_text.get_width() // 2, self.exit_button.centery - exit_text.get_height() // 2))

        pygame.display.update()

    def handle_hovers(self):
        hover = False
        hover_button = False
        mouse_pos = pygame.mouse.get_pos()
        buttons = [
            self.start_button,
            self.exit_button
        ]

        for btn in buttons:
            if btn.collidepoint(mouse_pos):
                hover = True
                hover_button = btn

        if hover:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
            self.hover_button = hover_button
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.hover_button = False



    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    self.game.game_loop()
                elif self.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    def start(self):
        while True:
            self.draw()
            self.handle_events()
            self.handle_hovers()