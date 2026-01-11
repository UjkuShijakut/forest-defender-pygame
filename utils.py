import math
import pygame


def load_image(path: str, size=None, alpha=True):
    try:
        img = pygame.image.load(path)
        img = img.convert_alpha() if alpha else img.convert()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except Exception:
        return None

def clamp(value, lo, hi):
     return max(lo, min(hi, value))


def unit_vector_towards(src, dst):
    dx = dst[0] - src[0]
    dy = dst[1] - src[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return 0.0, 0.0
    return dx / dist, dy / dist
