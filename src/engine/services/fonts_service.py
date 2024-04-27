import pygame.font


class FontsService:
    def __init__(self):
        self.fonts = {}

    def get(self, path: str, size:int):
        font_name = path + str(size)
        if font_name not in self.fonts:
            self.fonts[font_name] = pygame.font.Font(path, size)

        return self.fonts[font_name]