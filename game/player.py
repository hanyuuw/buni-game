# -*- coding: utf-8 -*-
import pygame
from pygame.surface import Surface
from pygame.rect import Rect

# Constantes e caminho dos assets (vem do constants)
from .constants import (
    ASSETS_DIR,            # assets/
    GRAVITY, JUMP_SPEED,   # física
    H_SPEED, FRAME_RATE,   # movimento/anima
    GROUND_Y, PLAYER_START_X,
)


class Player:
    def __init__(self) -> None:
        # estado base
        self.image: Surface | None = None
        self.rect: Rect | None = None
        self.vel_y: float = 0.0
        self.on_ground: bool = False
        self.lives: int = 3
        self.facing = 1  # 1=dir, -1=esq

        # animação
        self.animations: dict[str, list[Surface]] = {}
        self.state: str = "idle"      # idle | run | jump | hurt | death
        self.frame: int = 0
        self.frame_timer: float = 0.0
        self.frame_rate: float = FRAME_RATE

        # sprites
        self._load_all_animations()

        # caixa inicial
        self.rect = self.image.get_rect() if self.image else pygame.Rect(0, 0, 32, 32)
        self.rect.x = PLAYER_START_X
        self.rect.bottom = GROUND_Y
        self.on_ground = True

    # ────────────────────────── CARREGAMENTO ──────────────────────────
    def _load_strip(self, folder: str, base: str, count: int) -> list[Surface]:
        """
        Lê frames em assets/buni/<folder>/<base>_i.png, i=[0..count-1].
        Ex.: folder='idle', base='idle', count=3 → idle_0.png, idle_1.png, idle_2.png
        """
        frames: list[Surface] = []
        subdir = ASSETS_DIR / "buni" / folder

        for i in range(count):
            path = subdir / f"{base}_{i}.png"
            if path.is_file():
                frames.append(pygame.image.load(str(path)).convert_alpha())
            else:
                print(f"[AVISO] sprite não encontrado: {path}")

        if not frames:
            print(f"[ERRO] Nenhum sprite encontrado em {subdir} para base '{base}'!")
            # placeholder para evitar IndexError
            ph = pygame.Surface((32, 32), pygame.SRCALPHA)
            ph.fill((255, 0, 255, 180))
            frames = [ph]
        return frames

    def _load_all_animations(self) -> None:
        self.animations["idle"]  = self._load_strip("idle",  "idle",  3)
        self.animations["run"]   = self._load_strip("run",   "run",   5)  # até run_4.png
        self.animations["jump"]  = self._load_strip("jump",  "jump",  3)
        self.animations["hurt"]  = self._load_strip("hurt",  "hurt",  3)

        death_frames = self._load_strip("death", "death", 2)
        # se não existir death, usa hurt
        if len(death_frames) == 1 and death_frames[0].get_at((0, 0)) == (255, 0, 255, 180):
            self.animations["death"] = self.animations["hurt"]
        else:
            self.animations["death"] = death_frames

        self.image = self.animations[self.state][0]

    # ────────────────────────── CONTROLES ──────────────────────────
    def handle_input(self, keys, dt: float) -> None:
        """Atualiza estado + deslocamento horizontal."""
        moving = False
        dx = 0.0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            moving = True
            self.facing = 1
            dx += H_SPEED * dt

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            moving = True
            self.facing = -1
            dx -= H_SPEED * dt

        # aplica X (inteiro para evitar jitter)
        self.rect.x += int(dx)

        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()

        # estado visual
        if not self.on_ground:
            self._set_state("jump")
        else:
            self._set_state("run" if moving else "idle")

    # ────────────────────────── FÍSICA ──────────────────────────
    def apply_gravity(self, dt: float) -> None:
        self.vel_y += GRAVITY * dt
        self.rect.y += int(self.vel_y * dt)

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

    def jump(self) -> None:
        if self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
            self._set_state("jump")

    def take_damage(self) -> None:
        self._set_state("hurt")

    # ───────────────────── ATUALIZAÇÃO / DESENHO ────────────────────
    def update(self, dt: float, keys) -> None:
        self.handle_input(keys, dt)
        self.apply_gravity(dt)
        self._animate(dt)

    def _animate(self, dt: float) -> None:
        frames = self.animations.get(self.state, self.animations["idle"])
        if not frames:
            return
        self.frame_timer += dt
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0.0
            self.frame = (self.frame + 1) % len(frames)
        self.image = frames[self.frame]

    def draw(self, win: Surface) -> None:
        img = self.image
        if self.facing == -1:
            img = pygame.transform.flip(img, True, False)
        win.blit(img, self.rect.topleft)

    # ─────────────────────────── UTILS ───────────────────────────
    def _set_state(self, new_state: str) -> None:
        if new_state != self.state:
            self.state = new_state
            self.frame = 0
            self.frame_timer = 0.0
            frames = self.animations.get(self.state, [])
            if frames:
                self.image = frames[0]
