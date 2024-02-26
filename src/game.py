import pygame
import math

from player import Player
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
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Handle user inputs
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                player.handle_events(event)

            player.grow_circle_on_click()
            player.show_flash_on_release()
                        
            # Get the mouse position and update player facing direction
            current_mouse_pos = pygame.mouse.get_pos()
            player.update_direction(self.last_mouse_pos, current_mouse_pos)
            self.last_mouse_pos = pygame.mouse.get_pos()

            player.move_toward_mouse(height, current_mouse_pos)

            # Draw the game
            self.screen.fill(c.WHITE)
            player.draw(self.screen)
            # Update the display
            pygame.display.flip()
            self.clock.tick(c.FPS)