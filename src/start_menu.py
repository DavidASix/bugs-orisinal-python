import pygame
import sys
import pickle
from game import Game

import constants as c

class StartMenu:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.start_button = pygame.Rect(200, 200, int(self.screen.get_width() / 3), 50)
        self.exit_button = pygame.Rect(200, 300, int(self.screen.get_width() / 3), 50)
        self.hover_button = False
        self.final_score = None
        self.screen_width, self.screen_height = screen.get_size()
        self.high_score = 0
        self.load_high_score()

    def load_high_score(self):
        try:
            with open('high_score.pkl', 'rb') as f:
                self.high_score = pickle.load(f)
        except FileNotFoundError:
            pass

    def save_high_score(self):
        with open('high_score.pkl', 'wb') as f:
            pickle.dump(self.high_score, f)

    def update_high_score(self, final_score):
        if final_score > self.high_score:
            self.high_score = final_score
            self.save_high_score()

    def draw_start_menu(self):
        self.screen.fill((20, 20, 20))
        title = pygame.font.Font(None, 72).render("BUG GAME", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

        def btn_color(btn):
            if self.hover_button == btn:
                return (50, 50, 50)
            else:
                return (40, 40, 40)
        
        self.start_button = pygame.Rect(200, 200, int(self.screen.get_width() / 3), 50)
        pygame.draw.rect(self.screen, btn_color(self.start_button), self.start_button)
        start_text = pygame.font.Font(None, 26).render("Start Game", True, (255, 255, 255))
        self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2, self.start_button.centery - start_text.get_height() // 2))

        self.exit_button = pygame.Rect(200, 300, int(self.screen.get_width() / 3), 50)
        pygame.draw.rect(self.screen, btn_color(self.exit_button), self.exit_button)
        exit_text = pygame.font.Font(None, 26).render("Exit", True, (255, 255, 255))
        self.screen.blit(exit_text, (self.exit_button.centerx - exit_text.get_width() // 2, self.exit_button.centery - exit_text.get_height() // 2))


    def draw_score_menu(self):
        self.screen.fill((0, 0, 0))  # Clear the screen

        # Draw the title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Bug Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width / 2, self.screen_height / 4))
        self.screen.blit(title_text, title_rect)

        # Draw the final score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Final Score: {self.final_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 50))
        self.screen.blit(score_text, score_rect)

        # Draw the top score
        top_score_text = score_font.render(f"Top Score: {self.high_score}", True, (255, 255, 255))
        top_score_rect = top_score_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(top_score_text, top_score_rect)

        # Draw the new game button
        self.start_button = pygame.Rect(self.screen_width / 2 - self.screen_width / 6, self.screen_height / 2 + 50, self.screen_width / 3, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), self.start_button)
        new_game_text = score_font.render("New Game", True, (255, 255, 255))
        new_game_rect = new_game_text.get_rect(center=self.start_button.center)
        self.screen.blit(new_game_text, new_game_rect)

        # Draw the exit button
        self.exit_button = pygame.Rect(self.screen_width / 2 - self.screen_width / 6, self.screen_height / 2 + 120, self.screen_width / 3, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button)
        exit_text = score_font.render("Exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=self.exit_button.center)
        self.screen.blit(exit_text, exit_rect)

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
                    # Run the game and return the final score
                    game = Game(self.screen)
                    self.final_score = game.game_loop()
                    self.update_high_score(self.final_score)
                elif self.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    def start(self):
        while True:
            self.handle_events()
            self.handle_hovers()
            if self.final_score is not None:
                self.draw_score_menu()
            else:
                self.draw_start_menu()
            pygame.display.update()
            self.clock.tick(c.FPS)