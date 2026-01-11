import random
import pygame
import settings

from audio import AudioManager
from settings import WIDTH, HEIGHT, FPS, ASSETS_DIR, PLAYER_SIZE, ENEMY_SIZE, TREE_SIZE, ENEMY_SPEED, PROJECTILE_SIZE
from utils import load_image
from entities.player import Player
from entities.enemy import Enemy
from entities.tree import TreeBase


class Spawner:
    
    def __init__(self):
        self.last_spawn_time = 0
        self.spawn_interval_ms = 1200

        self.min_interval_ms = 350
        self.interval_decay = 0.98

        self.enemy_speed = ENEMY_SPEED
        self.enemy_hp = 5
        self.enemy_damage = 10

        self.last_difficulty_time = 0
        self.difficulty_every_ms = 8000

    def random_edge_position(self):
        corners = [(-30, -30), (WIDTH + 30, -30), (-30, HEIGHT + 30), (WIDTH + 30, HEIGHT + 30)]
        if random.random() < 0.35:
            return random.choice(corners)
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return random.randint(0, WIDTH), -30
        if side == "bottom":
            return random.randint(0, WIDTH), HEIGHT + 30
        if side == "left":
            return -30, random.randint(0, HEIGHT)
        return WIDTH + 30, random.randint(0, HEIGHT)

    def update_difficulty(self):
        now = pygame.time.get_ticks()
        if now - self.last_difficulty_time >= self.difficulty_every_ms:
            self.last_difficulty_time = now

            self.spawn_interval_ms = max(
                self.min_interval_ms, int(self.spawn_interval_ms * self.interval_decay)
            )

            self.enemy_speed += 0.15
            self.enemy_hp += 5

    def maybe_spawn_enemy(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_interval_ms:
            self.last_spawn_time = now
            return Enemy(
                pos=self.random_edge_position(),
                speed=self.enemy_speed,
                hp=self.enemy_hp,
                damage=self.enemy_damage,
            )
        return None


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)


        pygame.display.set_caption("Forest Defender (Cute Fantasy)")
        self.clock = pygame.time.Clock()

        self.audio = AudioManager(music_volume = 0.35, sfx_volume = 0.15)
        
        self.audio.load_sfx("shoot", "sfx_shoot.mp3")
        self.audio.load_sfx("lose", "sfx_lose.wav")

        self.audio.play_music("music_game.mp3", loop=True)

        self.font = pygame.font.SysFont(None, 32)
        self.big_font = pygame.font.SysFont(None, 64)

        self.bg = load_image(f"{ASSETS_DIR}/bg.png", (WIDTH, HEIGHT), alpha=False)
        self.player_img = load_image(f"{ASSETS_DIR}/player.png", PLAYER_SIZE, alpha=True)
        self.enemy_img = load_image(f"{ASSETS_DIR}/enemy.png", ENEMY_SIZE, alpha=True)
        self.tree_img = load_image(f"{ASSETS_DIR}/tree.png", TREE_SIZE, alpha=True)
        PROJECTILE_IMAGE_SIZE = (36,20)
        self.projectile_img = load_image(f"{ASSETS_DIR}/projectile.png", PROJECTILE_IMAGE_SIZE, alpha=True)
        self.game_over = False
        self.reset()

    def reset(self):
        self.game_over = False
        self.tree = TreeBase(center=(WIDTH // 2, HEIGHT // 2))
        self.tree.image = self.tree_img

        self.player = Player(pos=(WIDTH // 2, HEIGHT // 2 + 170))
        self.player.image = self.player_img

        self.spawner = Spawner()

        self.enemies = []
        self.projectiles = []

        self.score = 0
        self.game_over = False
        self.audio.play_music("music_game.mp3", loop=True)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if self.game_over and event.key == pygame.K_r:
                        self.reset()

                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over):
                        projectile = self.player.shoot(pygame.mouse.get_pos())
                        if projectile:
                            self.audio.play_sfx("shoot")
                            projectile.image = self.projectile_img
                            self.projectiles.append(projectile)

            if not self.game_over:
                self.update()

            self.draw()

            

        pygame.quit()

    def update(self):

        if self.game_over:
            return
        
        self.player.handle_movement()

        self.spawner.update_difficulty()
        new_enemy = self.spawner.maybe_spawn_enemy()
        if new_enemy:
            new_enemy.image = self.enemy_img
            self.enemies.append(new_enemy)

        for enemy in self.enemies:
            enemy.update(self.tree.rect.center)

        for proj in self.projectiles:
            proj.update()

        for proj in self.projectiles[:]:
            for enemy in self.enemies[:]:
                if proj.rect.colliderect(enemy.rect):
                    enemy.take_damage(proj.damage)
                    self.projectiles.remove(proj)
                    if enemy.is_dead():
                        self.enemies.remove(enemy)
                        self.score += 10
                        break

        for enemy in self.enemies[:]:
            if enemy.rect.colliderect(self.tree.rect):
                self.tree.take_damage(enemy.damage)
                self.enemies.remove(enemy)

            if self.tree.hp <= 0:
                self.game_over = True
                self.audio.stop_music()
                self.audio.play_lose_sfx("lose")
                return

        self.projectiles = [p for p in self.projectiles if not p.offscreen()]

    def draw(self):
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((35, 40, 55))

        # draw objects
        self.tree.draw(self.screen)
        for proj in self.projectiles:
            proj.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.player.draw(self.screen)

        hp_text = self.font.render(f"Tree HP: {self.tree.hp}", True, (255, 120, 180))
        score_text = self.font.render(f"Score: {self.score}", True, (120, 255, 200))
        self.screen.blit(hp_text, (15, 12))
        self.screen.blit(score_text, (15, 42))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            title = self.big_font.render("GAME OVER", True, (255, 80, 80))
            info = self.font.render(f"Final Score: {self.score}", True, (240, 240, 240))
            hint = self.font.render("Press R to Restart", True, (240, 240, 240))

            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
            self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 - 10))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 30))

        pygame.display.flip()
