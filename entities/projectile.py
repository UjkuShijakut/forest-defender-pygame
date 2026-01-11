import math
import pygame
from settings import WIDTH, HEIGHT, PROJECTILE_SIZE, PROJECTILE_SPEED, PROJECTILE_DMG


class Projectile:

    def __init__(self, start_pos, direction):
        self.rect = pygame.Rect(0, 0, PROJECTILE_SIZE[0], PROJECTILE_SIZE[1])
        self.rect.center = start_pos

        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.dirx, self.diry = direction
        self.angle = math.degrees(math.atan2(-self.diry, self.dirx))

        self.speed = PROJECTILE_SPEED
        self.damage = PROJECTILE_DMG

        self.image = None 

    def update(self):
        self.x += self.dirx * self.speed
        self.y += self.diry * self.speed
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def offscreen(self) -> bool:
        return (
            self.rect.right < 0
            or self.rect.left > WIDTH
            or self.rect.bottom < 0
            or self.rect.top > HEIGHT
        )

    def draw(self, screen):
        if self.image:
            rotated = pygame.transform.rotate(self.image, self.angle)
            rect = rotated.get_rect(center=self.rect.center)
            screen.blit(rotated, rect.topleft)
        else:
            pygame.draw.rect(screen, (245, 235, 120), self.rect, border_radius=3)
