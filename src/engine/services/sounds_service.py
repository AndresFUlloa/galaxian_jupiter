import pygame.mixer


class SoundsService:
    def __init__(self):
        self.sounds = {}

    def play(self, path: str):
        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(path)
        self.sounds[path].play()
