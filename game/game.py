# -*- coding: utf-8 -*-
from __future__ import annotations

import pygame
from pygame.surface import Surface

from .constants import (
    ASSETS_DIR, GROUND_Y,
    CAM_LEFT, CAM_RIGHT_RATIO,
)
from .player import Player


def try_load_image(*relpath: str) -> Surface | None:
    """Carrega imagem do assets/ ou retorna None se não existir."""
    path = ASSETS_DIR.joinpath(*relpath)
    try:
        return pygame.image.load(str(path)).convert_alpha()
    except FileNotFoundError:
        return None


class Game:
    def __init__(self, width: int, height: int, title: str = "Buni"):
        pygame.init()
        pygame.display.set_caption(title)

        # janela/clock/estado
        self.width, self.height = width, height
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False  # ← novo (pause)

        # câmera (dead-zone)
        self.cam_left  = CAM_LEFT
        self.cam_right = int(self.width * CAM_RIGHT_RATIO)

        # fundo
        self.bg = try_load_image("background", "bg.png")
        self.bg_scroll_x = 0.0

        # player
        self.player = Player()

        # plataforma inicial (posição de "mundo", rola junto com o fundo)
        self.platform_start: Surface | None = try_load_image("background", "platform_start.png")
        self.platform_rect: pygame.Rect | None = None
        self.platform_world_x: float | None = None

        if self.platform_start:
            r = self.platform_start.get_rect()
            self.platform_world_x = 40
            r.top = GROUND_Y - self.platform_start.get_height() + 10
            self.platform_rect = r

        # posiciona o Buni
        if self.platform_rect and self.platform_world_x is not None:
            self.player.rect.bottom = self.platform_rect.top
            self.player.rect.left   = int(self.platform_world_x) + 20
            self.player.vel_y = 0
            self.player.on_ground = True
        else:
            self.player.rect.bottom = GROUND_Y
            self.player.rect.x = max(self.player.rect.x, self.cam_left)

        # HUD (vidas)
        self.ui_heart = try_load_image("hud", "heart_full.png")
        # HUD (vidas)
        self.ui_heart = try_load_image("hud", "heart_full.png")
        self.ui_heart_pos = (10, 30)

        # aplica escala vinda das constantes
        from .constants import HEART_SCALE, HEART_GAP
        self.ui_heart_gap = HEART_GAP
        if self.ui_heart and HEART_SCALE != 1.0:
            w, h = self.ui_heart.get_width(), self.ui_heart.get_height()
            w2, h2 = int(w * HEART_SCALE), int(h * HEART_SCALE)
            # smoothscale deixa bonitinho em pixel art com pouco serrilhado.
            self.ui_heart = pygame.transform.smoothscale(self.ui_heart, (w2, h2))
        self.ui_heart_pos = (10, 30)   # canto superior-esquerdo
        self.ui_heart_gap = 25        # espaçamento entre corações

        # debug FPS
        self.font = pygame.font.SysFont("consolas", 14)

    # ──────────────────────────────────────────────────────────────────────────────
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    # restart leve (reusa a janela e re-inicializa o estado)
                    title = pygame.display.get_caption()[0] or "Buni"
                    self.__init__(self.width, self.height, title)
                    return

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        # movimento do Buni
        prev_x = self.player.rect.x
        self.player.update(dt, keys)
        dx = self.player.rect.x - prev_x

        # câmera: trava o Buni dentro da dead-zone e desloca o fundo
        if self.player.rect.x > self.cam_right and dx > 0:
            shift = self.player.rect.x - self.cam_right
            self.bg_scroll_x += shift
            self.player.rect.x = self.cam_right
        elif self.player.rect.x < self.cam_left and dx < 0:
            shift_needed = self.cam_left - self.player.rect.x
            allowed = min(shift_needed, self.bg_scroll_x)  # só volta se já scrollou
            self.bg_scroll_x -= allowed
            self.player.rect.x = self.cam_left
            if self.bg_scroll_x <= 0:
                self.bg_scroll_x = 0
                self.player.rect.x = self.cam_left

        # colisão com plataforma inicial (topo e laterais)
        self._collide_with_start_platform()

        # higiene do scroll
        if self.bg_scroll_x > 1e6 or self.bg_scroll_x < -1e6:
            self.bg_scroll_x = 0.0

    def _collide_with_start_platform(self) -> None:
        """Pisar e não atravessar a plataforma inicial."""
        if not (self.platform_start and self.platform_rect and self.platform_world_x is not None):
            return

        plat_rect = self.platform_rect.copy()
        plat_rect.left = int(self.platform_world_x - int(self.bg_scroll_x))

        p = self.player
        if p.rect.colliderect(plat_rect):
            # topo (caindo)
            if p.vel_y >= 0 and p.rect.bottom <= plat_rect.top + 10:
                p.rect.bottom = plat_rect.top
                p.vel_y = 0
                p.on_ground = True
            # lateral esquerda
            elif p.rect.right > plat_rect.left and p.rect.centerx < plat_rect.centerx:
                p.rect.right = plat_rect.left
            # lateral direita
            elif p.rect.left < plat_rect.right and p.rect.centerx > plat_rect.centerx:
                p.rect.left = plat_rect.right

    def draw_background(self, win: Surface) -> None:
        if not self.bg:
            win.fill((32, 34, 44))
            return
        w = self.bg.get_width()
        x = -int(self.bg_scroll_x) % w
        win.blit(self.bg, (x - w, 0))
        win.blit(self.bg, (x, 0))
        if x + w < self.width:
            win.blit(self.bg, (x + w, 0))

    def draw(self) -> None:
        self.draw_background(self.window)

        # plataforma inicial (com scroll)
        if self.platform_start and self.platform_rect and self.platform_world_x is not None:
            screen_x = int(self.platform_world_x - int(self.bg_scroll_x))
            if screen_x < self.width and screen_x + self.platform_rect.width > 0:
                dst = self.platform_rect.copy()
                dst.left = screen_x
                self.window.blit(self.platform_start, dst)

        # player
        self.player.draw(self.window)

        # HUD: vidas
        if self.ui_heart and getattr(self.player, "lives", 3) > 0:
            x, y = self.ui_heart_pos
            for i in range(self.player.lives):
                self.window.blit(self.ui_heart, (x + i * self.ui_heart_gap, y))

        # FPS + indicador de pause
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (180, 180, 180))
        self.window.blit(fps_text, (10, 10))
        if self.paused:
            pause_txt = self.font.render("PAUSED (P)", True, (200, 200, 200))
            self.window.blit(pause_txt, (10, 26))

        pygame.display.flip()

    def run(self) -> None:
        from .constants import MAX_DT
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            # 1) se a janela estiver sem foco (arrastando/minimizada), não atualiza a simulação
            if not pygame.display.get_active():
                # ainda processa eventos e redesenha para não travar a janela
                self.handle_events()
                self.draw()
                continue

            # 2) limita dt para evitar teleporte ao voltar do arrasto
            if dt > MAX_DT:
                dt = MAX_DT

            self.handle_events()
            if not self.paused:
                self.update(dt)
            self.draw()
        pygame.quit()
