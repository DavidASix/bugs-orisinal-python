import pygame
import math
import constants as c

class Bubble:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 30
        self.color = c.LIGHT_PINK
        self.flash_counter = 0
        self.size = 20
        self.destroy_bubble = False

    # Handle growth of circle
    def grow_circle_on_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.size = min(self.size + c.INCREMENT_SIZE, c.MAX_CIRCLE_SIZE)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

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
        if (self.flash_counter > 0):
            flashing_time = c.FPS * 0.5 # Flash for 1 second
            flashes = 5
            colors = [c.PINK if i % 2 == 0 else c.LIGHT_PINK for i in range(flashes)]
            flash_interval = flashing_time / flashes
            current_color_index = math.floor((self.flash_counter-1)/flash_interval)
            #print(flash_interval, current_color_index)
            # Reset or increment flash counter
            circle_color = colors[current_color_index]
            self.flash_counter = 0 if self.flash_counter >= flashing_time else self.flash_counter + 1
            self.destroy_bubble = True if self.flash_counter == 0 else False
        self.color = circle_color