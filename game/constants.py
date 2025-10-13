from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"

GRAVITY     = 1200
JUMP_SPEED  = -420
H_SPEED     = 120
FRAME_RATE  = 0.10

GROUND_Y       = 400
PLAYER_START_X = 80

# câmera
CAM_LEFT         = 70     # px
CAM_RIGHT_RATIO  = 0.20   # 20% da largura

# HUD (corações)
HEART_SCALE = 1.5   # 1.0 = tamanho original; aumente/diminua a gosto
HEART_GAP   = 22    # espaçamento horizontal entre corações, em pixels (já pensando no scale)

# Proteção contra picos de dt (evita teleporte ao arrastar a janela)
MAX_DT = 1.0 / 30.0   # nenhum frame vai simular mais que 1/30s