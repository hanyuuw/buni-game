import pygame, os

class SafeCloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        base_path = os.path.join("assets", "clouds")
        self.image = pygame.image.load(os.path.join(base_path, "safe_cloud.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, win, scroll_x):
        win.blit(self.image, (self.x - scroll_x, self.y))

    def screen_rect(self, scroll_x):
        return pygame.Rect(self.x - scroll_x, self.y, self.rect.width, self.rect.height)

    def is_danger(self):
        return False
