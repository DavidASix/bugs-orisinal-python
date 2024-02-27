import math

def distance_between(object_1, object_2):
    dx = object_1.x - object_2.x
    dy = object_1.y - object_2.y
    return math.sqrt(dx**2 + dy**2)