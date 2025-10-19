# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  CLOUD  ₊˚⊹🐇₊˚⊹
import pygame
from pygame.surface import Surface
from pygame.rect import Rect
from .constants import ASSETS_DIR


class Cloud:
    # cada nuvem é uma plataforma onde o buni pode pisar
    def __init__(self, x: int, y: int):
        """Cria uma nuvem segura em (x, y) com sprite do assets"""
        self.x = x
        self.y = y

        # tenta usar a imagem de nuvem do assets; se não tiver, usa um quadradinho
        base_path = ASSETS_DIR / "clouds"
        img_path = base_path / "safe_cloud.png"

        if img_path.is_file():
            self.image: Surface = pygame.image.load(str(img_path)).convert_alpha()
        else:
            ph = pygame.Surface((72, 36), pygame.SRCALPHA)
            ph.fill((200, 200, 255, 180))
            self.image = ph

        self.rect: Rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, win: Surface, scroll_x: float) -> None:
        """Desenha a nuvem já considerando o scroll do mundo."""
        win.blit(self.image, (self.x - scroll_x, self.y))

    def screen_rect(self, scroll_x: float) -> Rect:
        """Retorna o retângulo na tela com o scroll aplicado (pra colisão)."""
        return pygame.Rect(self.x - scroll_x, self.y, self.rect.width, self.rect.height)

    # (pra adicionar depois :c zz)
    def is_danger(self) -> bool:
        """Indica se a nuvem é perigosa (por enquanto, sempre False)."""
        return False
