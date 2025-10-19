# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  CONSTANTES (ajustes do jogo)  ₊˚⊹🐇₊˚⊹
from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)  # type: ignore[attr-defined]
else:
    BASE_DIR = Path(__file__).resolve().parents[1]

ASSETS_DIR = BASE_DIR / "assets"

# física e movimento do buni
GRAVITY    = 1200     # quanto o buni "pesa" caindo
JUMP_SPEED = -470     # força do pulo (negativo = pra cima)
H_SPEED    = 120      # velocidade andando (A/D ou setinhas)
FRAME_RATE = 0.10     # tempo entre frames da animação

# mundo e câmera
GROUND_Y        = 400        # altura do chão "base" (referência)
PLAYER_START_X  = 80         # onde o buni começa em X
CAM_LEFT        = 70         # limite esquerdo da dead-zone
CAM_RIGHT_RATIO = 0.20       # % da tela que é o limite direito da dead-zone
AUTO_SCROLL     = 140        # px/s (0 = desliga auto-scroll)

# HUD
HEART_SCALE = 1.4
HEART_GAP   = 24
MAX_DT      = 1.0 / 15.0     # trava o dt quando dá travadinhas, pra não “teleportar”

# nuvens (altura mínima e máxima onde podem nascer)
CLOUD_Y_MIN = GROUND_Y - 130
CLOUD_Y_MAX = GROUND_Y - 55

# espaçamento horizontal entre nuvens (base)
CLOUD_GAP_X_MIN = 120
CLOUD_GAP_X_MAX = 155

# alcance do pulo / limites de geração (pra não nascer impossível)
MIN_LOCAL_SPACING_X = 96
REACH_X_MAX         = 280

# primeira nuvem (tem que ser alcançável de início)
FIRST_CLOUD_GAP   = 100
FIRST_CLOUD_MIN_Y = GROUND_Y - 95
FIRST_CLOUD_MAX_Y = GROUND_Y - 10

# variação por bandas + jitter (só pra dar uma variada boa nas alturas)
CLOUD_BANDS       = 6
CLOUD_BAND_JITTER = 22

# degrau máximo entre plataformas (pra pulo atual)
MAX_CLOUD_STEP = 90

# quanto eu gero alééeeem da borda direita (buffer pra não ficar aparecendo do nada)
SPAWN_BUFFER = 180

# ₊˚⊹🐇₊˚⊹  SCORE & DIFICULDADE  ₊˚⊹🐇₊˚⊹
SCORE_PER_PIXEL   = 0.10
SPEED_STEP_SCORE  = 100
SPEED_STEP_DELTA  = 20
SPEED_MAX         = 300
