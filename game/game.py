# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  GAME (loop / câmera / colisões)  ₊˚⊹🐇₊˚⊹
from __future__ import annotations

import pygame
from pygame.surface import Surface

from .constants import (
    ASSETS_DIR, GROUND_Y,
    CAM_LEFT, CAM_RIGHT_RATIO,
    AUTO_SCROLL, PLAYER_START_X, MAX_DT,
    SCORE_PER_PIXEL, SPEED_STEP_SCORE, SPEED_STEP_DELTA, SPEED_MAX,
)
from .player import Player
from .cloudManager import CloudManager
from .hud import HUD
from .menu import Menu  # menus separados


def try_load_image(*relpath: str) -> Surface | None:
    path = ASSETS_DIR.joinpath(*relpath)
    try:
        return pygame.image.load(str(path)).convert_alpha()
    except FileNotFoundError:
        return None


class Game:
    def __init__(self, width: int, height: int, title: str = "Buni"):
        pygame.init()
        pygame.display.set_caption(title)

        self.width, self.height = width, height
        self.window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.state: str = "menu"  # menu | playing | paused | scores

        self.cam_left  = CAM_LEFT
        self.cam_right = int(self.width * CAM_RIGHT_RATIO)

        self.bg = try_load_image("background", "bg.png")
        self.bg_scroll_x = 0.0
        self._prev_scroll_x = 0.0

        self.menu = Menu(self.width, self.height)

        self.player = Player()

        self.platform_start: Surface | None = try_load_image("background", "platform_start.png")
        self.platform_rect: pygame.Rect | None = None
        self.platform_world_x: float | None = None
        if self.platform_start:
            r = self.platform_start.get_rect()
            self.platform_world_x = 40
            r.top = GROUND_Y - self.platform_start.get_height() + 10
            self.platform_rect = r

        if self.platform_rect and self.platform_world_x is not None:
            self.player.rect.bottom = self.platform_rect.top
            self.player.rect.left   = int(self.platform_world_x) + 20
            self.player.vel_y = 0
            self.player.on_ground = True
        else:
            self.player.rect.bottom = GROUND_Y
            self.player.rect.x = max(self.player.rect.x, self.cam_left)

        self._clouds_start_x = (
            (self.platform_world_x + self.platform_rect.width)
            if (self.platform_rect and self.platform_world_x is not None) else 180
        )
        self.clouds = CloudManager(self._clouds_start_x, self.width)

        self.hud = HUD()

        self.score = 0
        self._score_px_acum = 0.0
        self.world_speed = AUTO_SCROLL
        self.next_speed_milestone = SPEED_STEP_SCORE

        self.best_score = 0
        self.score_history: list[int] = []

    def _reset_after_fall(self) -> None:
        self.best_score = max(self.best_score, self.score)
        self.score_history.append(self.score)

        self.score = 0
        self._score_px_acum = 0.0
        self.world_speed = AUTO_SCROLL
        self.next_speed_milestone = SPEED_STEP_SCORE

        self.bg_scroll_x = 0.0
        self._prev_scroll_x = 0.0
        self.clouds.reset(self._clouds_start_x)

        if self.platform_rect and self.platform_world_x is not None:
            self.player.rect.bottom = self.platform_rect.top
            self.player.rect.left   = int(self.platform_world_x) + 20
        else:
            self.player.rect.bottom = GROUND_Y
            self.player.rect.x = PLAYER_START_X

        self.player.vel_y = 0
        self.player.on_ground = True

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return

                if event.key == pygame.K_RETURN:
                    if self.state == "menu":
                        self.state = "playing"
                    elif self.state == "paused":
                        self.state = "playing"
                    # em "scores" não usa ENTER; tem botão Back
                    return

                if event.key == pygame.K_p:
                    if self.state == "playing":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "playing"
                    return

                if event.key == pygame.K_r:
                    title = pygame.display.get_caption()[0] or "Buni"
                    self.__init__(self.width, self.height, title)
                    self.state = "playing"
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.state == "menu":
                    act = self.menu.handle_menu_click((mx, my))
                    if act == "start":
                        self.state = "playing"
                    elif act == "scores":
                        self.state = "scores"
                    elif act == "exit":
                        self.running = False
                elif self.state == "scores":
                    if self.menu.handle_scores_click((mx, my)):
                        self.state = "menu"
                        return
                elif self.state == "paused":
                    if self.menu.handle_pause_click((mx, my)):
                        title = pygame.display.get_caption()[0] or "Buni"
                        self.__init__(self.width, self.height, title)
                        self.state = "menu"
                        return

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if self.world_speed:
            self.bg_scroll_x += self.world_speed * dt

        self.clouds.update(dt, self.bg_scroll_x)
        self.clouds.collide_player(self.player, self.bg_scroll_x)

        prev_x = self.player.rect.x
        self.player.update(dt, keys)
        dx = self.player.rect.x - prev_x

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

        self._collide_with_start_platform()

        delta_scroll = max(0.0, self.bg_scroll_x - self._prev_scroll_x)
        self._score_px_acum += delta_scroll
        points = int(self._score_px_acum * SCORE_PER_PIXEL)
        if points > 0:
            self.score += points
            self._score_px_acum -= points / SCORE_PER_PIXEL

        if self.score >= self.next_speed_milestone:
            self.world_speed = min(self.world_speed + SPEED_STEP_DELTA, SPEED_MAX)
            self.next_speed_milestone += SPEED_STEP_SCORE

        if self.player.rect.top > self.height + 40:
            self._reset_after_fall()

        self._prev_scroll_x = self.bg_scroll_x

    def _collide_with_start_platform(self) -> None:
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

    def draw_background(self, win: Surface) -> None:
        if not self.bg:
            win.fill((32, 34, 44)); return
        w = self.bg.get_width()
        x = -int(self.bg_scroll_x) % w
        win.blit(self.bg, (x - w, 0))
        win.blit(self.bg, (x, 0))
        if x + w < self.width:
            win.blit(self.bg, (x + w, 0))

    def draw_menu(self) -> None:
        self.menu.draw_menu(self.window, self.draw_background)

    def draw_scores(self) -> None:
        self.menu.draw_scores(self.window, self.draw_background, self.best_score, self.score_history)

    def _render_scene(self, paused: bool = False) -> None:
        self.draw_background(self.window)
        if self.platform_start and self.platform_rect and self.platform_world_x is not None:
            screen_x = int(self.platform_world_x - int(self.bg_scroll_x))
            if 0 < screen_x + self.platform_rect.width and screen_x < self.width:
                dst = self.platform_rect.copy()
                dst.left = screen_x
                self.window.blit(self.platform_start, dst)
        self.clouds.draw(self.window, self.bg_scroll_x)
        self.player.draw(self.window)
        self.hud.draw(self.window, self.player.lives, self.clock.get_fps(), paused, self.score)

    def draw(self) -> None:
        self._render_scene(paused=False)
        pygame.display.flip()

    def draw_pause(self) -> None:
        self._render_scene(paused=True)
        self.menu.draw_pause_overlay(self.window)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()

            if self.state == "menu":
                self.draw_menu();   continue
            if self.state == "scores":
                self.draw_scores(); continue
            if self.state == "paused":
                self.draw_pause();  continue

            if dt > MAX_DT:
                dt = MAX_DT
            self.update(dt)
            self.draw()
        pygame.quit()
