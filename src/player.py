import pygame
import math
import os

import utilities as utils
import constants as c

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.radius = 25
        self.height = self.radius * 2
        self.width = self.radius // 1.25 * 2

        self.x = (c.WIDTH + self.radius) / 2
        self.y = (c.HEIGHT + self.radius) / 2

        self.direction = "S"

        self.moving = False
        self.jumping = False
        self.invincible = 0

        # Load sprites
        directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
        self.walking_animations = {}
        for direction in directions:
            animation_folder = f'./assets/sprites/player/{direction}'
            self.walking_animations[direction] = utils.preload_images(animation_folder)

        self.jumping_frames = utils.preload_images('./assets/sprites/player/jump')
        self.shadow_frames = utils.preload_images('./assets/sprites/player/shadow')
        self.static_shadow = pygame.image.load(os.path.join('./assets/sprites/player/shadow', f'1.png'))
        self.walking_start_tick = None
        self.jumping_start_tick = None
        self.shadow_start_tick = None


    def update_direction(self):
        # Get mouse and player positions, calculate angle (same as before)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = self.x, self.y
        dx, dy = mouse_x - player_x, player_y - mouse_y
        radians = math.atan2(-dy, dx)
        angle = math.degrees(radians)
        angle = (angle + 90) % 360

        # Define direction ranges and corresponding directions
        direction_ranges = {
            45: 'NE',
            90: 'E',
            135: 'SE',
            180: 'S',
            225: 'SW',
            270: 'W',
            315: 'NW'
        }

        # Find the closest direction based on the calculated angle
        closest_direction = min(direction_ranges.keys(), key=lambda x: abs(x - angle))

        # Direction buffer (same as before)
        direction_buffer = 22.5

        # Update direction if within the buffer range
        if abs(angle - closest_direction) <= direction_buffer:
            self.direction = direction_ranges[closest_direction]
        else:
            self.direction = 'N' 
    
    def move_toward_mouse(self, frame_height, current_mouse_pos):
        # Setup circular boundary for player
        circle_radius = frame_height / 2
        circle_center = (circle_radius, circle_radius)

        target_x, target_y = current_mouse_pos
        # Player should take 2.5 seconds to go from top to bottom of frame
        frame_speed = frame_height / 3.5 / c.FPS
        distance = math.hypot(target_x - self.x, target_y - self.y)
        # distance is compared against frame height to account for any variance
        # in movement when the frame is larger.
        if distance > math.floor(frame_height / 200):
            self.moving = True
            self.x += (target_x - self.x) * frame_speed / distance
            self.y += (target_y - self.y) * frame_speed / distance
        else:
            self.moving = False
        # Check if the player is outside the circle
        player_distance = math.hypot(self.x - circle_center[0], self.y - circle_center[1])
        if player_distance > circle_radius:
            # Move the player back towards the circle
            self.x -= (self.x - circle_center[0]) * (player_distance - circle_radius) / player_distance
            self.y -= (self.y - circle_center[1]) * (player_distance - circle_radius) / player_distance
    
    def play_shadow_animation(self, ticks):
        if self.shadow_start_tick:
            # The animation is 1 seconds long
            animation_duration = 0.75 * c.FPS
            image = utils.get_animation_frame(self.shadow_frames, ticks, self.shadow_start_tick, animation_duration)
            #print(image)
            if image is None:
                #self.shadow_starting_tick = None
                print('image is none')
            else:
                size = self.radius * 2.75
                image = pygame.transform.smoothscale(image, (size, size))
                self.screen.blit(image, (int(self.x - (size/2)), int(self.y - (size/2))))

    def play_jump_animation(self, ticks):
        animation_duration = 0.75 * c.FPS
        # Setup image
        image = utils.get_animation_frame(self.jumping_frames, ticks, self.jumping_start_tick, animation_duration)
        if image is None:
            print('jump image is none')
        else:
            image = pygame.transform.smoothscale(image, (self.width * 2.25, self.height * 2.25))
            self.screen.blit(image, (int(self.x - self.width * 1.125), int(self.y - self.height * 1.525)))

    def play_walking_animation(self, ticks):
        # Render Shadow
        size = self.radius * 2.75
        self.static_shadow = pygame.transform.smoothscale(self.static_shadow, (size, size))
        self.screen.blit(self.static_shadow, (int(self.x - (size/2)), int(self.y - (size/2))))

        # Render walking animation
        animation_duration = 0.75 * c.FPS
        image = utils.get_animation_frame_looped(self.walking_animations[self.direction], ticks, self.walking_start_tick, animation_duration)
        image = pygame.transform.smoothscale(image, (self.width, self.height))

        self.screen.blit(image, (int(self.x - self.width / 2), int(self.y - self.height / 2)))
        

    def animation(self):
        ticks = math.floor(pygame.time.get_ticks() / 1000 * 60)

        # Handle jumping and shadow animation
        if self.jumping:
            self.shadow_start_tick = ticks if self.shadow_start_tick is None else self.shadow_start_tick
            self.jumping_start_tick = ticks if self.jumping_start_tick is None else self.jumping_start_tick
            self.play_shadow_animation(ticks)
            self.play_jump_animation(ticks)
        else:
            self.shadow_start_tick = None
            self.jumping_start_tick = None

        # Handle walking animation
        if not self.jumping:
            self.walking_start_tick = ticks if self.walking_start_tick is None else self.walking_start_tick
            if not self.moving:
                self.walking_start_tick = ticks
            self.play_walking_animation(ticks)
        else:
            self.walking_start_tick = None

    def draw(self):
        flashing_seconds = 3
        flashing_frames = flashing_seconds * c.FPS
        flashing_interval = 3
        # If the player is invincible, flash every 3 frames for 3 seconds
        if self.invincible and self.invincible < flashing_frames:
            if self.invincible % flashing_interval == 0:  
                self.animation()
            self.invincible += 1
        else:
            self.invincible = 0
            self.animation()