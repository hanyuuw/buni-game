# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  HUD  ₊˚⊹🐇₊˚⊹
from __future__ import annotations

import pygame
from pygame.surface import Surface

from .constants import ASSETS_DIR

# ₊˚⊹🐇₊˚⊹  FONTE  ₊˚⊹🐇₊˚⊹
def load_font(size: int, bold: bool = False) -> pygame.font.Font:
    font_path = ASSETS_DIR / "fonts" / "Tiny5-Regular.ttf"
    if font_path.is_file():
        return pygame.font.Font(str(font_path), size)
    return pygame.font.SysFont("consolas", size, bold=bold)


class HUD:
    def __init__(self) -> None:
        self.font = load_font(18, bold=True)
        self.font_small = load_font(14)
        self.col_text = (235, 235, 240)
        self.col_shadow = (0, 0, 0)

    # ₊˚⊹🐇₊˚⊹  TEXTINHO COM SOMBRA  ₊˚⊹🐇₊˚⊹
    def _blit_text(self, win: Surface, text: str, x: int, y: int, align: str = "left") -> None:
        label = self.font.render(text, True, self.col_text)
        shadow = self.font.render(text, True, self.col_shadow)
        if align == "right":
            x = x - label.get_width()
        win.blit(shadow, (x + 1, y + 1))
        win.blit(label, (x, y))

    # ₊˚⊹🐇₊˚⊹  DESENHO  ₊˚⊹🐇₊˚⊹
    def draw(self, win: Surface, lives: int, fps: float, paused: bool, score: int) -> None:
        # FPS
        self._blit_text(win, f"FPS {int(fps)}", 8, 6, align="left")
        # SCORE
        self._blit_text(win, f"SCORE {score}", win.get_width() - 8, 6, align="right")
