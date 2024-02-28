import pygame
import math
import utilities as utils
import os
import sys

from player import Player
from bubble import Bubble
from bug import Bug
from health import Health
from score_board import ScoreBoard

import constants as c

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.last_mouse_pos = None
        self.play_field = pygame.Surface(screen.get_size())
        self.overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        current_dir = os.path.dirname(__file__)
        background_path = os.path.join(current_dir, f'assets/sprites/background.png')
        overlay_path = os.path.join(current_dir, f'assets/sprites/overlay.png')
        self.background_image = pygame.image.load(background_path)
        self.overlay_image = pygame.image.load(overlay_path)


    def game_loop(self):
        width, height = self.screen.get_size()
        player = Player()
        bubble = None
        bugs = []
        health = Health(3)
        score_board = ScoreBoard(None, width)
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                # Handle user inputs
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bubble is None:
                        bubble = Bubble()
                elif event.type == pygame.MOUSEBUTTONUP:
                        # A bubble could have been popped before the user let go of the mouse
                        # If not, increase the bubble size, start it flashing, and check if it intersects any bugs
                        # If it does, remove that bug
                        if bubble is not None:
                            bubble.player_jumping = True

            while len(bugs) < 20:
                bugs.append(Bug(width, height))

            # Fill the background with white
            self.screen.fill(c.WHITE)
            # Draw the clipping mask overlay
            pygame.draw.ellipse(self.overlay, (255, 255, 255, 255), (0, 0, *self.screen.get_size()))

            # Fill the play field (which will be drawn below clipping mask)
            # This is done to hide the previous frames
            self.play_field.fill((250, 250, 250))
            background_image = pygame.transform.smoothscale(self.background_image, self.screen.get_size())
            self.play_field.blit(background_image, (0,0))

            ## BUGLOGIC
            for bug in bugs:
                bug.move()
                bug.draw(self.play_field)
                
            # Player Logic
            player.jumping = bubble.player_jumping if bubble else False
            # Get the mouse position and update player facing direction
            current_mouse_pos = pygame.mouse.get_pos()
            player.update_direction(self.last_mouse_pos, current_mouse_pos)
            self.last_mouse_pos = pygame.mouse.get_pos()
            player.move_toward_mouse(height, current_mouse_pos)

            # Bubble drawing logic
            if bubble is not None:
                bubble.grow_circle_on_click()
                bubble.update_position(player.x, player.y)
                bubble.draw(self.play_field)
                if bubble.destroy_bubble:
                    bubble = None

            # Handle bubble bug intersection
            if bubble is not None:
                if bubble.player_jumping:
                    squished_bugs = bubble.handle_bubble_pop(bugs)
                    if squished_bugs is not None:
                        for bug in squished_bugs:
                            bugs.remove(bug)
                            score_board.increase()
                            #bug = None
                # Damage calculation for bug bubble interaction
                # Only calculate damage if the bubble is not popping (player not jumping)
                # and bubble is not flashing (bubble has not burst yet)
                if not bubble.player_jumping and bubble.flash is None:
                    for bug in bugs:
                        if utils.distance_between(bubble, bug) <= (bubble.size + bug.size) and not bubble.jump_time:
                            # TODO: on bug interaction
                            # Play scratch anim at bug location
                            # Play ouch jump anim at player location
                            # make player invincible for 2 seconds
                            bubble.destroy_bubble = True
                            health.lose_life()
                            self.running = health.current_health > 0
                            break
                    
            player.draw(self.play_field)
            overlay_image = pygame.transform.smoothscale(self.overlay_image, self.screen.get_size())
            self.play_field.blit(overlay_image, (0,0))
            # Blit the play_field onto the overlay (below clipping mask)
            self.overlay.blit(self.play_field, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

            # Blit the overlay onto the screen
            self.screen.blit(self.overlay, (0,0))
            # Draw the UI
            health.draw(self.screen)
            score_board.draw(self.screen)

            # Update the display
            pygame.display.flip()
            self.clock.tick(c.FPS)
        return score_board.score