import pygame
import math
from settings import WIDTH, HEIGHT, PLAYER_SIZE, PLAYER_SPEED
from utils import clamp, unit_vector_towards
from entities.projectile import Projectile


class Player:
   

    def __init__(self, pos):
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE[0], PLAYER_SIZE[1])
        self.rect.center = pos
        
        self.speed = PLAYER_SPEED

        self.cooldown_ms = 180
        self.last_shot_time = 0

        self.image = None
    
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        self.rect.left = clamp(self.rect.left, 0, WIDTH - self.rect.width)
        self.rect.top = clamp(self.rect.top, 0, HEIGHT - self.rect.height)

    def can_shoot(self) -> bool:
        now = pygame.time.get_ticks()
        return now - self.last_shot_time >= self.cooldown_ms

    def shoot(self, mouse_pos):
        if not self.can_shoot():
            return None
        
        mx, my = mouse_pos
        px, py = self.rect.center

        dx = mx - px
        dy = my - py
        dist = math.hypot(dx, dy)

        if dist == 0:
            return None
        
        direction = (dx / dist, dy / dist)

        self.last_shot_time = pygame.time.get_ticks()
        direction = unit_vector_towards(self.rect.center, mouse_pos)
        return Projectile((px, py), direction)
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, (60, 120, 220), self.rect, border_radius=10)
            pygame.draw.rect(screen, (25, 60, 140), self.rect, 3, border_radius=10)
