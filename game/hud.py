# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  HUD (vidas / fps / pause / score)  ₊˚⊹🐇₊˚⊹
from __future__ import annotations

import pygame
from pygame.surface import Surface

from .constants import ASSETS_DIR, HEART_SCALE, HEART_GAP


def _load_image(*relpath: str) -> Surface | None:
    """Carrega uma imagem do /assets; se não achar, devolve None."""
    path = ASSETS_DIR.joinpath(*relpath)
    try:
        return pygame.image.load(str(path)).convert_alpha()
    except FileNotFoundError:
        return None


class HUD:
    # desenha os corações, o FPS, o "PAUSED" e o SCORE
    def __init__(self, pos: tuple[int, int] = (10, 30), gap: int = HEART_GAP):
        """Prepara o HUD (imagem do coração, fonte e posições)."""
        self.heart: Surface | None = _load_image("hud", "heart_full.png")
        if self.heart and HEART_SCALE != 1.0:
            w, h = self.heart.get_width(), self.heart.get_height()
            self.heart = pygame.transform.smoothscale(
                self.heart, (int(w * HEART_SCALE), int(h * HEART_SCALE))
            )
        self.pos = pos
        self.gap = gap
        self.font = pygame.font.SysFont("consolas", 14)
        self.font_score = pygame.font.SysFont("consolas", 18, bold=True)

    def draw(self, win: Surface, lives: int, fps: float, paused: bool, score: int | None = None) -> None:
        """Desenha vidas, FPS, PAUSE e (se tiver) o SCORE no canto direito."""
        # corações (vidas) — canto esquerdo
        if self.heart and lives > 0:
            x, y = self.pos
            for i in range(lives):
                win.blit(self.heart, (x + i * self.gap, y))

        # FPS
        fps_text = self.font.render(f"FPS: {int(fps)}", True, (180, 180, 180))
        win.blit(fps_text, (10, 10))

        # SCORE
        if score is not None:
            text = self.font_score.render(f"SCORE: {score}", True, (235, 235, 235))
            pad = 10
            x = win.get_width() - text.get_width() - pad
            y = 10
            win.blit(text, (x, y))

        # PAUSE
        if paused:
            pause_txt = self.font.render("PAUSED (P)", True, (200, 200, 200))
            win.blit(pause_txt, (10, 26))
