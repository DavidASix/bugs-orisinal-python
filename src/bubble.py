import pygame
import math
import constants as c
import os

class Bubble:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = c.LIGHT_PINK
        self.size = 20
        self.flash_counter = 0
        self.bubble_popping = False
        self.destroy_bubble = False
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

    def draw(self, screen):
        # Load the sprite image        # Load the sprite image
        bubble_size = self.size * 2 - 1
        image = pygame.transform.smoothscale(self.bubble_image, (bubble_size, bubble_size))
        screen.blit(image, (self.x-self.size, self.y-self.size))

        # Draw the glare animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_glare_update > self.glare_delay:
            print('Update Glare')
            self.glare_animation_index = (self.glare_animation_index + 1) % len(self.glare_sprites)
            self.last_glare_update = current_time
        glare_size = bubble_size*0.5
        glare_image = self.glare_sprites[self.glare_animation_index]
        glare_image = pygame.transform.smoothscale(glare_image, (glare_size, glare_size))
        screen.blit(glare_image, (self.x - bubble_size*0.0625, self.y  - bubble_size*0.0625))

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def flash(self):
        if self.flash_count < 4:
            if self.color == c.PINK:
                self.color = c.LIGHT_PINK
            else:
                self.color = c.PINK
            self.flash_count += 1
            self.flash_timer = pygame.time.get_ticks()

# Handle flashing on release of MB
    def show_flash_on_release(self):
        circle_color = c.LIGHT_PINK
        if self.bubble_popping:

            flashing_time = c.FPS * 0.25 # Flash for 1 second
            flashes = 3
            colors = [c.PINK if i % 2 == 0 else c.LIGHT_PINK for i in range(flashes)]
            flash_interval = flashing_time / flashes
            current_color_index = math.floor((self.flash_counter-1)/flash_interval)
            #print(flash_interval, current_color_index)
            # Reset or increment flash counter
            circle_color = colors[current_color_index]
            
            if self.flash_counter >= flashing_time:
                self.flash_counter = 0
                self.bubble_popping = False
                self.destroy_bubble = True
            else:
                self.flash_counter += 1
                
        self.color = circle_color