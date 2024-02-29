import pygame
import sys
import pickle
import os
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

        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, f'assets/frames/start.png')
        self.start_bg = pygame.image.load(image_path)
        image_path = os.path.join(current_dir, f'assets/frames/score.png')
        self.score_bg = pygame.image.load(image_path)

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

    def btn_color(self, btn):
        if self.hover_button == btn:
            return (50, 50, 50)
        else:
            return (40, 40, 40)
    
    def draw_start_menu(self):
        self.screen.fill((255, 255, 255))
        start_bg = pygame.transform.smoothscale(self.start_bg, self.screen.get_size())
        self.screen.blit(start_bg, (0,0))


        btn_font = pygame.font.Font(None, 26)

        # Draw the new game button
        self.start_button = pygame.Rect(self.screen_width / 2 - self.screen_width / 6, self.screen_height / 2, self.screen_width / 3, 50)
        pygame.draw.rect(self.screen, self.btn_color(self.start_button), self.start_button)
        new_game_text = btn_font.render("New Game", True, (255, 255, 255))
        new_game_rect = new_game_text.get_rect(center=self.start_button.center)
        self.screen.blit(new_game_text, new_game_rect)

        # Draw the exit button
        self.exit_button = pygame.Rect(self.screen_width / 2 - self.screen_width / 6, self.screen_height / 2 + 70, self.screen_width / 3, 50)
        pygame.draw.rect(self.screen, self.btn_color(self.exit_button), self.exit_button)
        exit_text = btn_font.render("Exit", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=self.exit_button.center)
        self.screen.blit(exit_text, exit_rect)


    def draw_score_menu(self):
        self.screen.fill((255, 255, 255))
        score_bg = pygame.transform.smoothscale(self.score_bg, self.screen.get_size())
        self.screen.blit(score_bg, (0,0))

        text_color = (40, 40, 40)
        # Draw the title
        title_font = pygame.font.Font(None, 72)
        score_font = pygame.font.Font(None, 36)
        btn_font = pygame.font.Font(None, 26)

        title_text = title_font.render("Bug Game", True, text_color)
        title_rect = title_text.get_rect(center=(self.screen_width / 2, self.screen_height / 4))
        self.screen.blit(title_text, title_rect)

        # Draw the final score
        score_text = score_font.render(f"Final Score: {self.final_score}", True, text_color)
        score_rect = score_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 50))
        self.screen.blit(score_text, score_rect)

        # Draw the top score
        top_score_text = score_font.render(f"Top Score: {self.high_score}", True, text_color)
        top_score_rect = top_score_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(top_score_text, top_score_rect)

        # Draw the new game button
        self.start_button = pygame.Rect(self.screen_width / 2 - self.screen_width / 6, self.screen_height / 2 + 50, self.screen_width / 3, 50)
        pygame.draw.rect(self.screen, self.btn_color(self.start_button), self.start_button)
        new_game_text = btn_font.render("New Game", True, (255, 255, 255))
        new_game_rect = new_game_text.get_rect(center=self.start_button.center)
        self.screen.blit(new_game_text, new_game_rect)

        # Draw the exit button
        self.exit_button = pygame.Rect(self.screen_width / 2 - self.screen_width / 6, self.screen_height / 2 + 120, self.screen_width / 3, 50)
        pygame.draw.rect(self.screen, self.btn_color(self.exit_button), self.exit_button)
        exit_text = btn_font.render("Exit", True, (255, 255, 255))
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