import pygame
from settings import TREE_SIZE, TREE_MAX_HP


class TreeBase:

    def __init__(self, center):
        self.hp = TREE_MAX_HP
        self.rect = pygame.Rect(0, 0, TREE_SIZE[0], TREE_SIZE[1])
        self.rect.center = center
        self.image = None

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

    def draw(self, screen):
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            screen.blit(self.image, image_rect.topleft)

        else:
            pygame.draw.rect(screen, (40, 170, 70), self.rect, border_radius=12)
            pygame.draw.rect(screen, (20, 110, 45), self.rect, 3, border_radius=12)