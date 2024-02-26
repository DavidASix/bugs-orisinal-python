import pygame
import math

import constants as c

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.flash_counter = 0
        self.size = 20
        self.color = c.GREEN
        self.direction = "S"

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('Mouse Down')
        elif event.type == pygame.MOUSEBUTTONUP:
            print('Mouse Up')
            self.size = c.BASE_CIRCLE_SIZE
            self.flash_counter = 1

    # Handle growth of circle
    def grow_circle_on_click(self):
        if pygame.mouse.get_pressed()[0]:
            self.size = min(self.size + c.INCREMENT_SIZE, c.MAX_CIRCLE_SIZE)

    # Handle flashing on release of MB
    def show_flash_on_release(self):
        circle_color = c.GREEN
        if (self.flash_counter > 0):
            flashing_time = c.FPS * 1 # Flash for 2 seconds
            flashes = 4
            colors = [c.RED if i % 2 == 0 else c.BLUE for i in range(flashes)]
            flash_interval = flashing_time / flashes
            current_color_index = math.floor((self.flash_counter-1)/flash_interval)
            # Reset or increment flash counter
            circle_color = colors[current_color_index]
            self.flash_counter = 0 if self.flash_counter >= flashing_time else self.flash_counter + 1
        self.color = circle_color

    def update_direction(self, last_mouse_pos, current_mouse_pos):
        if (last_mouse_pos and current_mouse_pos):
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            ew = "E" if dx > 0 else "W" if dx < 0 else ""
            ns = "S" if dy > 0 else "N" if dy < 0 else ""
            self.direction = ns + ew

    def move_toward_mouse(self, frame_height, current_mouse_pos):
        target_x, target_y = current_mouse_pos
        # Player should take 2.5 seconds to go from top to bottom of frame
        frame_speed = frame_height / 2.5 / c.FPS
        distance = math.hypot(target_x - self.x, target_y - self.y)
        if distance > 1:
            self.x += (target_x - self.x) * frame_speed / distance
            self.y += (target_y - self.y) * frame_speed / distance

    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)