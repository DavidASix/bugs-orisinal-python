import pygame
import math

import constants as c

class Player:
    def __init__(self):
        self.size = 20
        self.x = (c.WIDTH + self.size) / 2
        self.y = (c.HEIGHT + self.size) / 2
        self.color = c.GREEN
        self.direction = "S"

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
        # distance is compared against frame height to account for any variance
        # in movement when the frame is larger.
        if distance > math.floor(frame_height / 200):
            self.x += (target_x - self.x) * frame_speed / distance
            self.y += (target_y - self.y) * frame_speed / distance

    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)