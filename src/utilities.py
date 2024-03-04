import math
import pygame
import os

def distance_between(object_1, object_2):
    dx = object_1.x - object_2.x
    dy = object_1.y - object_2.y
    return math.sqrt(dx**2 + dy**2)

def preload_images(folder_path):
    images = []
    num_images = len([filename for filename in os.listdir(folder_path) if filename.endswith('.png')])
    for frame in range(1, num_images + 1):
        image = pygame.image.load(os.path.join(folder_path, f'{frame}.png'))
        images.append(image)
    return images

def get_animation_frame(sprites, game_ticks, start_tick, animation_duration):
    current_tick = game_ticks - start_tick
    if current_tick < 0 or current_tick > animation_duration:
        print('return none')
        return None
    frame_duration = animation_duration / (len(sprites))

    current_frame = round(current_tick / frame_duration)
    return sprites[current_frame]

def get_animation_frame_looped(sprites, game_ticks, start_tick, animation_loop_time):
    current_tick = game_ticks - start_tick
    frame_duration = animation_loop_time / (len(sprites))
    current_frame = (round(current_tick / frame_duration)  % len(sprites))
    return sprites[current_frame]