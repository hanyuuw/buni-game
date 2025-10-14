# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  GAME (loop / câmera / colisões)  ₊˚⊹🐇₊˚⊹
from __future__ import annotations

import pygame
from pygame.surface import Surface

from .constants import (
    ASSETS_DIR, GROUND_Y,
    CAM_LEFT, CAM_RIGHT_RATIO,
    AUTO_SCROLL, PLAYER_START_X, MAX_DT,
)
from .player import Player
from .cloudManager import CloudManager  # gerencia spawn/remoção de nuvens e colisão com o player
from .hud import HUD


# ₊˚⊹🐇₊˚⊹  CARREGAR IMAGEM (assets)  ₊˚⊹🐇₊˚⊹
def try_load_image(*relpath: str) -> Surface | None:
    """Tenta carregar uma imagem de /assets; se não existir, retorna None."""
    path = ASSETS_DIR.joinpath(*relpath)
    try:
        return pygame.image.load(str(path)).convert_alpha()
    except FileNotFoundError:
        return None


class Game:
    # ₊˚⊹🐇₊˚⊹  INÍCIO (janela, player, mundo)  ₊˚⊹🐇₊˚⊹
    def __init__(self, width: int, height: int, title: str = "Buni"):
        """Cria janela, configura câmera, carrega fundo, player, nuvens e HUD."""
        pygame.init()
        pygame.display.set_caption(title)

        self.width, self.height = width, height
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused  = False

        # dead-zone da câmera (o buni pode andar um pouco sem puxar o mundo)
        self.cam_left  = CAM_LEFT
        self.cam_right = int(self.width * CAM_RIGHT_RATIO)

        # fundo e scroll horizontal do mundo
        self.bg = try_load_image("background", "bg.png")
        self.bg_scroll_x = 0.0

        # player
        self.player = Player()

        # plataforma inicial (se o arquivo existir)
        self.platform_start: Surface | None = try_load_image("background", "platform_start.png")
        self.platform_rect: pygame.Rect | None = None
        self.platform_world_x: float | None = None
        if self.platform_start:
            r = self.platform_start.get_rect()
            self.platform_world_x = 40
            r.top = GROUND_Y - self.platform_start.get_height() + 10
            self.platform_rect = r

        # posiciono o buni em cima da plataforma (ou no chão)
        if self.platform_rect and self.platform_world_x is not None:
            self.player.rect.bottom = self.platform_rect.top
            self.player.rect.left   = int(self.platform_world_x) + 20
            self.player.vel_y = 0
            self.player.on_ground = True
        else:
            self.player.rect.bottom = GROUND_Y
            self.player.rect.x = max(self.player.rect.x, self.cam_left)

        # nuvens (começam um pouco à frente da plataforma)
        self._clouds_start_x = (
            (self.platform_world_x + self.platform_rect.width)
            if (self.platform_rect and self.platform_world_x is not None) else 180
        )
        self.clouds = CloudManager(self._clouds_start_x, self.width)

        # HUD (vidinhas / fps / pause)
        self.hud = HUD()

    # ₊˚⊹🐇₊˚⊹  QUEDA / RESET SUAVE  ₊˚⊹🐇₊˚⊹
    def _reset_after_fall(self) -> None:
        """Remove 1 vida e volta pro começo quando o Buni cai da tela."""
        self.player.lives = max(0, self.player.lives - 1)

        # volta câmera e nuvens
        self.bg_scroll_x = 0
        self.clouds.reset(self._clouds_start_x)

        # tenta respawn na plataforma, se tiver
        if self.platform_rect and self.platform_world_x is not None:
            self.player.rect.bottom = self.platform_rect.top
            self.player.rect.left   = int(self.platform_world_x) + 20
        else:
            self.player.rect.bottom = GROUND_Y
            self.player.rect.x = PLAYER_START_X

        self.player.vel_y = 0
        self.player.on_ground = True

    # ₊˚⊹🐇₊˚⊹  EVENTOS  ₊˚⊹🐇₊˚⊹
    def handle_events(self) -> None:
        """Atalhos: ESC sai, P pausa, R reinicia a cena."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    title = pygame.display.get_caption()[0] or "Buni"
                    self.__init__(self.width, self.height, title)
                    return

    # ₊˚⊹🐇₊˚⊹  UPDATE (mundo + player + câmera)  ₊˚⊹🐇₊˚⊹
    def update(self, dt: float) -> None:
        """Atualiza auto-scroll, nuvens, player e movimentação da câmera."""
        keys = pygame.key.get_pressed()

        # auto-scroll (se quiser estilo T-Rex)
        if AUTO_SCROLL:
            self.bg_scroll_x += AUTO_SCROLL * dt

        # nuvens (spawn/limpa) + colisão com o buni
        self.clouds.update(dt, self.bg_scroll_x)
        self.clouds.collide_player(self.player, self.bg_scroll_x)

        # movimento do buni (A/D são opcionais)
        prev_x = self.player.rect.x
        self.player.update(dt, keys)
        dx = self.player.rect.x - prev_x

        # câmera com dead-zone: só puxa o mundo se passar do limite
        if self.player.rect.x > self.cam_right and dx > 0:
            shift = self.player.rect.x - self.cam_right
            self.bg_scroll_x += shift
            self.player.rect.x = self.cam_right
        elif self.player.rect.x < self.cam_left and dx < 0:
            shift_needed = self.cam_left - self.player.rect.x
            allowed = min(shift_needed, self.bg_scroll_x)
            self.bg_scroll_x -= allowed
            self.player.rect.x = self.cam_left
            if self.bg_scroll_x <= 0:
                self.bg_scroll_x = 0
                self.player.rect.x = self.cam_left

        # colisão com a plataforma inicial (se existir)
        self._collide_with_start_platform()

        # higiene: evita valores doidos no scroll
        if self.bg_scroll_x > 1e6 or self.bg_scroll_x < -1e6:
            self.bg_scroll_x = 0.0

        # caiu da tela?
        if self.player.rect.top > self.height + 40:
            self._reset_after_fall()

    def _collide_with_start_platform(self) -> None:
        """Colisão simples com a plataforma inicial (topo/lado), se existir."""
        if not (self.platform_start and self.platform_rect and self.platform_world_x is not None):
            return
        plat_rect = self.platform_rect.copy()
        plat_rect.left = int(self.platform_world_x - int(self.bg_scroll_x))
        p = self.player
        if p.rect.colliderect(plat_rect):
            if p.vel_y >= 0 and p.rect.bottom <= plat_rect.top + 10:
                p.rect.bottom = plat_rect.top
                p.vel_y = 0
                p.on_ground = True
            elif p.rect.right > plat_rect.left and p.rect.centerx < plat_rect.centerx:
                p.rect.right = plat_rect.left
            elif p.rect.left < plat_rect.right and p.rect.centerx > plat_rect.centerx:
                p.rect.left = plat_rect.right

    # ₊˚⊹🐇₊˚⊹  DESENHO  ₊˚⊹🐇₊˚⊹
    def draw_background(self, win: Surface) -> None:
        """Desenha o fundo em “tile” horizontal de acordo com o scroll."""
        if not self.bg:
            win.fill((32, 34, 44)); return
        w = self.bg.get_width()
        x = -int(self.bg_scroll_x) % w
        win.blit(self.bg, (x - w, 0))
        win.blit(self.bg, (x, 0))
        if x + w < self.width:
            win.blit(self.bg, (x + w, 0))

    def draw(self) -> None:
        """Desenha: fundo, plataforma (se visível), nuvens, buni e HUD."""
        self.draw_background(self.window)

        # plataforma inicial (só se estiver visível na tela)
        if self.platform_start and self.platform_rect and self.platform_world_x is not None:
            screen_x = int(self.platform_world_x - int(self.bg_scroll_x))
            if 0 < screen_x + self.platform_rect.width and screen_x < self.width:
                dst = self.platform_rect.copy()
                dst.left = screen_x
                self.window.blit(self.platform_start, dst)

        # nuvens + player + HUD
        self.clouds.draw(self.window, self.bg_scroll_x)
        self.player.draw(self.window)
        self.hud.draw(self.window, self.player.lives, self.clock.get_fps(), self.paused)

        pygame.display.flip()

    # ₊˚⊹🐇₊˚⊹  LOOP PRINCIPAL  ₊˚⊹🐇₊˚⊹
    def run(self) -> None:
        """Loop principal do jogo (60fps alvo) com clamp de dt."""
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            # se a janela não está ativa, só mantém desenhando e ouvindo eventos
            if not pygame.display.get_active():
                self.handle_events()
                self.draw()
                continue

            if dt > MAX_DT:  # evita “teleporte” quando a janela trava
                dt = MAX_DT

            self.handle_events()
            if not self.paused:
                self.update(dt)
            self.draw()
        pygame.quit()
