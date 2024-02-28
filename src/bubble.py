import pygame
import os

import constants as c
import utilities as utils

class Bubble:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 20
        # Indicates if player is current jumping. Occurs on mouse buton release and bubble pop 
        self.player_jumping = False
        # Counts the frames during players jump animation
        self.jump_time = 0
        self.flash = None
        # Slates bubble for destruction this game tick
        self.destroy_bubble = False
        # Sprite information
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, f'assets/sprites/bubble/pink.png')
        self.bubble_image = pygame.image.load(image_path).convert_alpha()
        self.glare_sprites = []
        for i in range(1, 6):
            image = pygame.image.load(os.path.join(current_dir, f'./assets/sprites/bubble_glare/{i}.png'))
            self.glare_sprites.append(image)
        self.glare_animation_index = 0
        self.glare_delay = 100  # milliseconds
        self.last_glare_update = pygame.time.get_ticks()

    # Handle growth of circle
    def grow_circle_on_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.size = min(self.size + c.INCREMENT_SIZE, c.MAX_CIRCLE_SIZE)

    def render_glare(self, screen):
        bubble_size = self.size * 2
        # Draw the glare animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_glare_update > self.glare_delay:
            self.glare_animation_index = (self.glare_animation_index + 1) % len(self.glare_sprites)
            self.last_glare_update = current_time
        glare_size = bubble_size*0.5
        glare_image = self.glare_sprites[self.glare_animation_index]
        glare_image = pygame.transform.smoothscale(glare_image, (glare_size, glare_size))
        screen.blit(glare_image, (self.x - bubble_size*0.0625, self.y  - bubble_size*0.0625))

    def draw(self, screen):  # Pass in your game clock object (c)
        if self.player_jumping:
            return None
    
        diameter = self.size * 2
        image = pygame.transform.smoothscale(self.bubble_image, (diameter, diameter))

        if self.flash is not None:
            self.flash_animation(screen)
        else:  # Normal drawing if not flashing
            screen.blit(image, (self.x - self.size, self.y - self.size))
            self.render_glare(screen)

    def flash_animation(self, screen):
        flash_duration_seconds = 0.25 
        total_flash_frames = c.FPS * flash_duration_seconds
        flash_interval = total_flash_frames / 8

        flash_index = int(self.flash / flash_interval) % 2  # Determine on/off based on frame count

        if flash_index == 0:  # Draw the visible circle
            pygame.draw.circle(screen, c.WHITE, (self.x, self.y), self.size)

        self.flash += 1  # Increment the flash counter

        if self.flash >= total_flash_frames:  # Flashing complete
            self.flash = None
            self.destroy_bubble = True

    def update_position(self, x, y):
        self.x = x
        self.y = y

    # Handle flashing on release of MB
    def handle_bubble_pop(self, bugs):
        if not self.player_jumping:
            return None
        squished_bugs = None
        total_jump_length = c.FPS * 0.75
        # A 1 second JUMP animation occurs after releasing the mouse
        # During this time, the user can reposition their character and they are invincible
        if self.jump_time < total_jump_length:
            self.jump_time += 1
        else:
            # When the jump animation is complete reset the state, increase bubble size,
            # and start the flashing animation. Player cannot take bubble bug interaction damage
            # while self.flashing is not none.
            self.player_jumping = False
            self.size *= 2
            self.jump_time = 0
            self.flash = 0
            # Find the bugs that would be squished and return them for deletion
            squished_bugs = []
            for bug in bugs:
                if utils.distance_between(self, bug) <= (self.size + bug.size):
                    squished_bugs.append(bug)
        return squished_bugs