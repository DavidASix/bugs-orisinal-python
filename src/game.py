import pygame
import math

from player import Player
from bubble import Bubble
from bug import Bug

import constants as c

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.last_mouse_pos = None

    def game_loop(self):
        width, height = self.screen.get_size()
        player = Player()
        bubble = None
        bugs = []
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle user inputs
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bubble is None:
                        bubble = Bubble()
                elif event.type == pygame.MOUSEBUTTONUP:
                        bubble.flash_counter = 1
            while len(bugs) < 20:
                bugs.append(Bug(width, height))

            self.screen.fill(c.WHITE)

            # BUG LOGIC
            for bug in bugs:
                bug.move()
                bug.draw(self.screen)
                
            # Player Logic
            # Get the mouse position and update player facing direction
            current_mouse_pos = pygame.mouse.get_pos()
            player.update_direction(self.last_mouse_pos, current_mouse_pos)
            self.last_mouse_pos = pygame.mouse.get_pos()
            player.move_toward_mouse(height, current_mouse_pos)

            # Bubble Logic
            if bubble is not None:
                bubble.show_flash_on_release()
                bubble.grow_circle_on_click()
                bubble.update_position(player.x, player.y)
                bubble.draw(self.screen)
                if bubble.destroy_bubble:
                    bubble = None
                    
            player.draw(self.screen)


            # Update the display
            pygame.display.flip()
            self.clock.tick(c.FPS)