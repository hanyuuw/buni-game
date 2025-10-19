# 🤍 Buni

₍˶ˊᵕˋ˵₎💭

**pt-br 🇧🇷**  
> Um joguinho de plataforma fofinho feito em **Python (Pygame)**

**en-us 🇺🇸**  
> A cozy little platformer made with **Python (Pygame)**

---

## 🤍 Sobre o jogo / About the game

**pt-br 🇧🇷**  
Você controla um coelhinho pulando entre nuvens ☁️  
O **score** sobe conforme você avança e, de tempos em tempos, o mundo fica um pouquinho mais rápido
O placar (melhor pontuação e histórico) é salvo localmente.

**en-us 🇺🇸**  
You control a tiny bunny jumping across clouds ☁️  
Your **score** increases as you progress and the world speeds up slightly over time  
The scoreboard (best and history) is saved locally.

---

## 🎮 Controles / Controls

| Ação (pt-br) | Tecla | Action (en-us) |
|---|---|---|
| Pular | **Espaço / ↑** | Jump |
| Mover | **← / →** | Move |
| Pausar / Retomar | **P** | Pause / Resume |
| Reiniciar partida | **R** | Restart |
| Sair do jogo | **Esc** | Quit |

---

## ⚙️ Como rodar o jogo / How to run the game

**pt-br 🇧🇷**
1. Verifique se você tem o **Python 3.10+** instalado!! 
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o jogo:
   ```bash
   python main.py
   ```
   
**en-us 🇺🇸**
1. Make sure you have Python 3.10+ installed!! 
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the game:
   ```bash
   python main.py
   ```
   
---

## 🧩 Estrutura do projeto / Project structure

```text
buni/
├─ main.py
├─ requirements.txt
├─ README.md
│
├─ game/
│  ├─ __init__.py
│  ├─ constants.py
│  ├─ game.py
│  ├─ player.py
│  ├─ cloud.py
│  ├─ cloudManager.py
│  ├─ hud.py
│  └─ menu.py
│
└─ assets/
   ├─ background/
   ├─ buni/
   ├─ clouds/
   ├─ fonts/           # Tiny5-Regular.ttf
   ├─ hud/
   └─ sfx/             # click.wav, jump.wav
 ```

---

## 🌤️ Mecânicas / Mechanics

**pt-br 🇧🇷**

- Pulo entre nuvens (colisão suave) ☁️

- Score por distância percorrida 

- A velocidade do mundo sobe em marcos de pontuação 📈

**en-us 🇺🇸**

- Cloud-to-cloud platforming with soft collisions ☁️

- Score increases with distance

- World speed steps up at score milestones 📈

---

## 💾 Tecnologias e aprendizado / Technologies & learning

Este projetinho foi desenvolvido como parte da disciplina **Linguagem de Programação Aplicada** do curso de **Análise e Desenvolvimento de Sistemas (ADS)** da **Uninter**, com foco em:

- **Python + Pygame** — estrutura básica de jogo, loop, eventos e desenho.
- **Sprites** do buni (idle/run/jump) com troca de frames simples.
- **Física** rápida: gravidade, pulo e “coyote time” (pulo perdoa 1 tiquinho).
- **Nuvens** com espaçamento e colisão suave.
- **Câmera** com dead-zone e scroll do fundo.
- **Score** por distância + leves aumentos de velocidade.
- **SQLite** pra salvar **best** e **histórico** no `~/.buni/buni.db`.
- **Build** com PyInstaller (onedir/onefile) e assets empacotados.

> Ideias que deixei pra depois: crack overlay, dano, estrelinhas/colecionáveis, efeitos sonoros extras.

---

This little project was developed as part of the **Applied Programming Language** course in the **Systems Analysis and Development (ADS)** program at **Uninter**, focusing on:

- **Python + Pygame** — game loop, events and rendering basics.
- **Sprite animation** (idle/run/jump).
- **Simple physics**: gravity, jump and a small coyote time.
- **Clouds** spacing + soft collisions.
- **Camera** dead-zone with background scrolling.
- **Score** by distance + gentle speed steps.
- **SQLite** for all-time best & history at `~/.buni/buni.db`.
- **Packaging** with PyInstaller (onedir/onefile).

> Future ideas: crack overlay, damage, collectibles, extra SFX.

---

## 🎀 Créditos e arte / Art & Credits

- 🐰 **Personagem principal (Buni)** — usado com modificações de cor, a partir dos assets de [Givty](https://givty.itch.io/).  
  *Licença:* uso permitido em projetos comerciais e não comerciais, com atribuição opcional.  
  *(Arte original por Givty)*  


- 🔤 **Fonte** — [Tiny5](https://fonts.google.com/specimen/Tiny5) por [Stefan Schmidt](https://github.com/Gissio)                    
Licença: [SIL Open Font License 1.1](https://openfontlicense.org/)


- 🌤️ **Céu e background** — criados por mim!!  

---

- 🐰 **Main character (Buni)** — used with color modifications, from assets by [Givty](https://givty.itch.io/).  
  *License:* allowed for commercial and non-commercial projects, credit appreciated but not required.  
  *(Original art by Givty)*


- 🔤 **Font** — [Tiny5](https://fonts.google.com/specimen/Tiny5) by [Stefan Schmidt](https://github.com/Gissio)                    
License: [SIL Open Font License 1.1](https://openfontlicense.org/)


- 🌤️ **Sky and background** — created by me!!

---

---

<p align="center">
  🐇 ( ˶ˆᗜˆ˵ )ﾉ☆
</p>

---

---
