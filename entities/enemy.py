# entities/enemy.py
import pygame
import math
from settings import ENEMY_SIZE
from utils import unit_vector_towards


class Enemy:
 
    def __init__(self, pos, speed: float, hp: int, damage: int):
        self.rect = pygame.Rect(0, 0, ENEMY_SIZE[0], ENEMY_SIZE[1])
        self.rect.center = pos
        
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.speed = speed
        self.hp = hp
        self.damage = damage

        self.image = None

    def update(self, target_pos):
        tx, ty = target_pos
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)

        if dist == 0:
            return
        
        dx /= dist
        dy /= dist

        self.x += dx * self.speed
        self.y += dy * self.speed

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
    def take_damage(self, amount: int):
        self.hp -= amount

    def is_dead(self) -> bool:
        return self.hp <= 0

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, (220, 70, 70), self.rect, border_radius=10)
            pygame.draw.rect(screen, (140, 25, 25), self.rect, 3, border_radius=10)
