# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  PLAYER (Buni)  ₊˚⊹🐇₊˚⊹
import pygame
from pygame.surface import Surface
from pygame.rect import Rect

# coisas que uso aqui: paths, física e posições
from .constants import (
    ASSETS_DIR,
    GRAVITY, JUMP_SPEED,
    H_SPEED, FRAME_RATE,
    GROUND_Y, PLAYER_START_X,
)


class Player:
    # ₊˚⊹🐇₊˚⊹  ESTADO INICIAL  ₊˚⊹🐇₊˚⊹
    # aqui eu guardo tudo que o buni precisa pra existir (sprite, caixa, vel, etc)
    def __init__(self) -> None:
        """Cria o Buni com sprite, caixa de colisão e estados iniciais."""
        self.image: Surface | None = None
        self.rect: Rect | None = None

        # velocidade vertical e status de chão
        self.vel_y: float = 0.0
        self.on_ground: bool = False

        # vidinhas e direção (1 = direita, -1 = esquerda)
        self.lives: int = 3
        self.facing = 1

        # animações básicas
        self.animations: dict[str, list[Surface]] = {}
        self.state: str = "idle"      # idle | run | jump | hurt | death
        self.frame: int = 0
        self.frame_timer: float = 0.0
        self.frame_rate: float = FRAME_RATE

        # coyote time = janelinha pra pular logo depois de sair da nuvem
        self.coyote_max = 0.25  # ~250ms
        self.coyote_timer = 0.0

        # sprites do buni (se faltar, eu deixo um quadradinho magenta pra lembrar)
        self._load_all_animations()

        # caixa e posição inicial
        self.rect = self.image.get_rect() if self.image else pygame.Rect(0, 0, 32, 32)
        self.rect.x = PLAYER_START_X
        self.rect.bottom = GROUND_Y
        self.on_ground = True

    # ₊˚⊹🐇₊˚⊹  CARREGAMENTO DE SPRITES  ₊˚⊹🐇₊˚⊹
    # lê os frames em assets/buni/<pasta>/<base>_i.png
    def _load_strip(self, folder: str, base: str, count: int) -> list[Surface]:
        """Carrega uma sequência de frames de uma pasta específica do Buni."""
        frames: list[Surface] = []
        subdir = ASSETS_DIR / "buni" / folder

        for i in range(count):
            path = subdir / f"{base}_{i}.png"
            if path.is_file():
                frames.append(pygame.image.load(str(path)).convert_alpha())
            else:
                print(f"[aviso] sprite não encontrado: {path}")

        if not frames:
            # placeholder visível só pra eu lembrar que faltou arquivo
            print(f"[erro] nenhum sprite em {subdir} pra base '{base}'")
            ph = pygame.Surface((32, 32), pygame.SRCALPHA)
            ph.fill((255, 0, 255, 180))
            frames = [ph]
        return frames

    # carrega tudo de uma vez (idle/run/jump/hurt/death)
    def _load_all_animations(self) -> None:
        """Carrega todas as animações do Buni (e um fallback pra death)."""
        self.animations["idle"] = self._load_strip("idle", "idle", 3)
        self.animations["run"]  = self._load_strip("run", "run", 5)
        self.animations["jump"] = self._load_strip("jump", "jump", 3)
        self.animations["hurt"] = self._load_strip("hurt", "hurt", 3)

        death_frames = self._load_strip("death", "death", 2)
        # se "death" não existir, usa "hurt" como quebra-galho
        self.animations["death"] = death_frames if death_frames else self.animations["hurt"]
        self.image = self.animations[self.state][0]

    # ₊˚⊹🐇₊˚⊹  INPUT / MOVIMENTO HORIZONTAL  ₊˚⊹🐇₊˚⊹
    # aqui cuido do A/D/←/→ e também chamo o pulo
    def handle_input(self, keys, dt: float) -> None:
        """Lê teclado, move em X e decide estado de animação."""
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

        # aplica o deslocamento horizontal
        self.rect.x += int(dx)

        # tecla de pulo (usa coyote time se tiver)
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()

        # escolhe o estado pra animar
        if not self.on_ground:
            self._set_state("jump")
        else:
            self._set_state("run" if moving else "idle")

    # ₊˚⊹🐇₊˚⊹  PULO (com coyote)  ₊˚⊹🐇₊˚⊹
    # se estiver no chão OU dentro da janelinha do coyote, pode pular
    def jump(self) -> None:
        """Faz o Buni pular, respeitando a janelinha do coyote time."""
        if self.on_ground or self.coyote_timer > 0.0:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
            self.coyote_timer = 0.0  # consumiu a janela do coyote
            self._set_state("jump")

    # ₊˚⊹🐇₊˚⊹  FÍSICA VERTICAL  ₊˚⊹🐇₊˚⊹
    # gravidade + integração da posição; o pouso real acontece nas colisões com as nuvens
    def apply_gravity(self, dt: float) -> None:
        """Aplica gravidade e atualiza a posição vertical do Buni."""
        self.vel_y += GRAVITY * dt
        self.rect.y += int(self.vel_y * dt)

        # não "cola" no GROUND_Y aqui porque as plataformas que mandam
        if self.rect.bottom >= GROUND_Y:
            self.on_ground = False

    # ₊˚⊹🐇₊˚⊹  DANO (efeito visual)  ₊˚⊹🐇₊˚⊹
    def take_damage(self) -> None:
        """Troca animação pra 'hurt' (efeito visual)."""
        self._set_state("hurt")

    # ₊˚⊹🐇₊˚⊹  UPDATE GERAL  ₊˚⊹🐇₊˚⊹
    # orquestra input, física e animação; também atualiza o timer do coyote
    def update(self, dt: float, keys) -> None:
        """Atualiza input, física, animação e o timer do coyote time."""
        self.handle_input(keys, dt)
        self.apply_gravity(dt)
        self._animate(dt)

        # coyote: se no chão, recarrega; se no ar, conta pra baixo
        if self.on_ground:
            self.coyote_timer = self.coyote_max
        else:
            if self.coyote_timer > 0.0:
                self.coyote_timer = max(0.0, self.coyote_timer - dt)

    # ₊˚⊹🐇₊˚⊹  ANIMAÇÃO  ₊˚⊹🐇₊˚⊹
    # troca os frames no ritmo certo
    def _animate(self, dt: float) -> None:
        """Avança os frames da animação no ritmo configurado."""
        frames = self.animations.get(self.state, self.animations["idle"])
        if not frames:
            return
        self.frame_timer += dt
        if self.frame_timer >= self.frame_rate:
            self.frame_timer = 0.0
            self.frame = (self.frame + 1) % len(frames)
        self.image = frames[self.frame]

    # ₊˚⊹🐇₊˚⊹  DESENHO  ₊˚⊹🐇₊˚⊹
    # desenha o buni; se estiver olhando pra esquerda, eu dou flip no sprite
    def draw(self, win: Surface) -> None:
        """Desenha o Buni na tela (espelha quando estiver virado pra esquerda)."""
        img = self.image
        if self.facing == -1:
            img = pygame.transform.flip(img, True, False)
        win.blit(img, self.rect.topleft)

    # se ele estiver no chão, força a animação correta imediatamente
    def force_ground_anim(self, moving: bool, world_speed: float) -> None:
        """Se estiver no chão, força run/idle neste frame."""
        if self.on_ground:
            self._set_state("run" if moving else "idle")

    # ₊˚⊹🐇₊˚⊹  HELPER DE ESTADO  ₊˚⊹🐇₊˚⊹
    def _set_state(self, new_state: str) -> None:
        """Troca o estado de animação e reseta o frame timer."""
        if new_state != self.state:
            self.state = new_state
            self.frame = 0
            self.frame_timer = 0.0
            frames = self.animations.get(self.state, [])
            if frames:
                self.image = frames[0]
