# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  CLOUD MANAGER (spawn/colisão)  ₊˚⊹🐇₊˚⊹
from __future__ import annotations

import random
from pygame.surface import Surface

from .cloud import Cloud
from .constants import (
    CLOUD_Y_MIN, CLOUD_Y_MAX,
    CLOUD_GAP_X_MIN, CLOUD_GAP_X_MAX,
    FIRST_CLOUD_GAP, FIRST_CLOUD_MIN_Y, FIRST_CLOUD_MAX_Y,
    MAX_CLOUD_STEP,
    CLOUD_BANDS, CLOUD_BAND_JITTER,
    SPAWN_BUFFER,
    MIN_LOCAL_SPACING_X, REACH_X_MAX,
)


class CloudManager:
    # cuida de criar as nuvens, remover as velhas e checar colisão com o buni
    def __init__(self, world_start_x: float, screen_width: int):
        """Inicia a lista de nuvens e parâmetros de geração/limpeza."""
        self.clouds: list[Cloud] = []
        self.screen_width = screen_width
        self.rightmost_world_x = world_start_x
        self._last_bands: list[int] = []   # memória curtinha pra não repetir banda
        self._prev_y = (CLOUD_Y_MIN + CLOUD_Y_MAX) // 2
        self._prev_route_x: int | None = None  # “rota” aproximada do player
        self._first = True

    def reset(self, world_start_x: float):
        """Limpa tudo e recomeça a gerar a partir de world_start_x."""
        self.clouds.clear()
        self.rightmost_world_x = world_start_x
        self._prev_y = (CLOUD_Y_MIN + CLOUD_Y_MAX) // 2
        self._prev_route_x = None
        self._first = True

    def _next_gap(self) -> int:
        """Decide o próximo gap horizontal (o primeiro é menor pra ser alcançável)."""
        if self._first:
            self._first = False
            return FIRST_CLOUD_GAP
        return random.randint(CLOUD_GAP_X_MIN, CLOUD_GAP_X_MAX)

    def _spawn_one(self) -> None:
        """Cria uma nuvem respeitando alcance em X e degrau máximo em Y."""
        gap = self._next_gap()
        x = max(self.rightmost_world_x + gap, self.rightmost_world_x + MIN_LOCAL_SPACING_X)
        if self._prev_route_x is not None:
            x = min(x, self._prev_route_x + REACH_X_MAX)

        # Y por bandas (pra variar altura) com um jitterzinho
        band_span = (CLOUD_Y_MAX - CLOUD_Y_MIN)
        band_height = band_span / (CLOUD_BANDS - 1) if CLOUD_BANDS > 1 else (band_span or 1)

        # tento não repetir a mesma banda toda hora
        candidates = list(range(CLOUD_BANDS))
        if len(self._last_bands) >= 2 and self._last_bands[-1] == self._last_bands[-2]:
            rep = self._last_bands[-1]
            if rep in candidates and len(candidates) > 1:
                candidates.remove(rep)

        band = random.choice(candidates)
        y_center = CLOUD_Y_MIN + band * band_height
        y = int(y_center + random.randint(-CLOUD_BAND_JITTER, CLOUD_BAND_JITTER))

        # primeira nuvem precisa ser alcançável de início
        if not self.clouds:
            y = max(y, FIRST_CLOUD_MIN_Y)
            y = min(y, FIRST_CLOUD_MAX_Y)

        # limita o degrau vertical entre nuvens pra não ficar impossível
        if self.clouds:
            low  = max(CLOUD_Y_MIN, self._prev_y - MAX_CLOUD_STEP)
            high = min(CLOUD_Y_MAX, self._prev_y + MAX_CLOUD_STEP)
            y = max(low, min(high, y))

        y = max(min(y, CLOUD_Y_MAX), CLOUD_Y_MIN)  # clamp final

        c = Cloud(x, y)
        self.clouds.append(c)
        self.rightmost_world_x = x + c.rect.width

        # atualiza memória pra próxima geração
        self._prev_y = y
        self._prev_route_x = x
        self._last_bands.append(band)
        if len(self._last_bands) > 2:
            self._last_bands.pop(0)

    def ensure_to_fill(self, scroll_x: float):
        while self.rightmost_world_x < scroll_x + self.screen_width + SPAWN_BUFFER:
            self._spawn_one()

    def cull_left(self, scroll_x: float):
        left_limit = scroll_x - (SPAWN_BUFFER + 200)
        self.clouds = [c for c in self.clouds if c.x + c.rect.width > left_limit]

    def update(self, dt: float, scroll_x: float):
        self.ensure_to_fill(scroll_x)
        self.cull_left(scroll_x)

    def draw(self, win: Surface, scroll_x: float):
        for c in self.clouds:
            c.draw(win, scroll_x)

    def collide_player(self, player, scroll_x: float):
        """Resolve colisões do Buni com as nuvens (topo e laterais)."""
        prect = player.rect
        for c in self.clouds:
            r = c.screen_rect(scroll_x)
            if prect.colliderect(r):
                # topo (aterrissagem) — só se estiver caindo
                if player.vel_y >= 0 and prect.bottom <= r.top + 10:
                    prect.bottom = r.top
                    player.vel_y = 0
                    player.on_ground = True
                # laterais (empurra pra fora)
                elif prect.right > r.left and prect.centerx < r.centerx:
                    prect.right = r.left
                elif prect.left < r.right and prect.centerx > r.centerx:
                    prect.left = r.right
