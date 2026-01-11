import os
import pygame
from settings import ASSETS_DIR


class AudioManager:
    def __init__(self, music_volume=0.35, sfx_volume=0.5):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.music_volume = float(music_volume)
        self.sfx_volume = float(sfx_volume)
        self.current_music = None
        self.sfx = {}
        self.lose_channel = pygame.mixer.Channel(2)

    def load_sfx(self, name: str, filename: str, volume=None):
        path = os.path.join(ASSETS_DIR, filename)
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.sfx_volume if volume is None else float(volume))
        self.sfx[name] = sound

    def play_music(self, filename: str, loop=True):
        path = os.path.join(ASSETS_DIR, filename)
        if self.current_music == path:
            return

        self.current_music = path
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def set_music_volume(self, volume: float):
        self.music_volume = max(0.0, min(1.0, float(volume)))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float):
        self.sfx_volume = max(0.0, min(1.0, float(volume)))
        for snd in self.sfx.values():
            snd.set_volume(self.sfx_volume)

    def play_sfx(self, name: str):
        snd = self.sfx.get(name)
        if snd:
            snd.play()

    def play_lose_sfx(self, name: str):
        snd = self.sfx.get(name)
        if snd:
            self.lose_channel.play(snd)
