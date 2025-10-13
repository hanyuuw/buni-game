# 🤍 buni

₍˶ˊᵕˋ˵₎💭

**pt-br 🇧🇷**  
> Um joguinho de plataforma fofinho feito em **Python (Pygame)**

**en-us 🇺🇸**  
> A cozy little platformer made with **Python (Pygame)**

---

## 🤍 Sobre o jogo / About the game

**pt-br 🇧🇷**  
Você controla um coelhinho pulando entre nuvens!! ☁️  
Colete estrelas ✨, evite nuvens perigosas ⚡ e tente fazer a maior pontuação possível.  
Com o tempo, o jogo vai ficando um pouquinho mais rápido, mas ainda tentei manter a vibe *cozy* e tranquila 🌙.

**en-us 🇺🇸**  
You control a small bunny jumping between clouds!! ☁️  
Collect shiny stars ✨, avoid dangerous clouds ⚡, and try to reach the highest score.  
Over time, the game speeds up a little, but keeps its calm and cozy atmosphere 🌙.

---

## 🎮 Controles / Controls

| Ação (pt-br) | Tecla | Action (en-us) |
|---------------|--------|----------------|
| Pular | **Espaço / ↑** | Jump |
| Mover | **← / →** | Move |
| Pausar | **P** | Pause |
| Reiniciar | **R** | Restart |
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
buni-project/
│
├─ main.py                # ponto de entrada / main entry
├─ requirements.txt
├─ .gitignore
├─ README.md
│
├─ buni/                  # pacote do jogo / main package
│  ├─ __init__.py
│  ├─ game.py
│  ├─ player.py
│  ├─ hud.py
│  ├─ cloud.py
│  ├─ cloudManager.py
│  ├─ safeCloud.py
│  ├─ dangerCloud.py
│  ├─ crackOverlay.py
│  ├─ parallaxBackground.py
│  └─ platformStart.py
│
└─ assets/                # sprites, sons, fontes / sprites, sounds, fonts
 ```

---

## 💾 Tecnologias e aprendizado / Technologies & learning

Este projeto foi desenvolvido como parte da disciplina **Linguagem de Programação Aplicada** do curso de **Análise e Desenvolvimento de Sistemas (ADS)** da **Uninter**, com foco em:

- 🎮 **Pygame** — desenvolvimento do jogo principal e controle de física 2D.  
- 🧱 **UML (Diagrama de Classes)** — modelagem estrutural do sistema antes da implementação.  
- 🧩 **StarUML** — ferramenta usada para desenhar e gerar o código base em Python a partir do diagrama.  
- 💾 **Banco de Dados (EntityScore)** — armazenamento local das pontuações e nomes dos jogadores.  
- 🐍 **Python 3.10+** — linguagem principal do projeto.  
- 🧠 **Programação Orientada a Objetos (POO)** — organização do código em classes e métodos.  
- 🧵 **Git + GitHub** — controle de versão e publicação do projeto.  

---

This project was developed as part of the **Applied Programming Language** course in the **Systems Analysis and Development (ADS)** program at **Uninter**, focusing on:

- 🎮 **Pygame** — main game development and 2D physics handling.  
- 🧱 **UML (Class Diagram)** — structural modeling before implementation.  
- 🧩 **StarUML** — used to design and generate Python base code from the diagram.  
- 💾 **Database (EntityScore)** — local storage for player names and scores.  
- 🐍 **Python 3.10+** — main programming language.  
- 🧠 **Object-Oriented Programming (OOP)** — class-based game architecture.  
- 🧵 **Git + GitHub** — version control and project publishing.

---

## 🌤️ Mecânicas / Mechanics

**pt-br 🇧🇷**

- Coelhinho pula em nuvens seguras ☁️

- Evite nuvens perigosas ⚡

- Colete estrelas ✨ para aumentar a pontuação

- A dificuldade aumenta conforme o score sobe

- Efeitos visuais calmos e dreamcore 💫

**en-us 🇺🇸**

- Bunny jumps on safe clouds ☁️

- Avoid dangerous ones ⚡

- Collect stars ✨ to increase your score

- Game difficulty scales gradually with your progress

- Dreamcore & cozy atmosphere 💫

---

## 🎀 Créditos e arte / Art & Credits

- 🐰 **Personagem principal (Buni)** — usado com modificações de cor, a partir dos assets de [Givty](https://givty.itch.io/).  
  *Licença:* uso permitido em projetos comerciais e não comerciais, com atribuição opcional.  
  *(Arte original por Givty)*  


- 🌤️ **Céu e background** — criados por Bianca R.  
- ⭐ **Estrela e demais elementos** — em desenvolvimento por Bianca R.  

---

- 🐰 **Main character (Buni)** — used with color modifications, from assets by [Givty](https://givty.itch.io/).  
  *License:* allowed for commercial and non-commercial projects, credit appreciated but not required.  
  *(Original art by Givty)*  


- 🌤️ **Sky and background** — created by Bianca R.  
- ⭐ **Star and other elements** — in development by Bianca R.

---

---

<p align="center">
  🐇 ( ˶ˆᗜˆ˵ )ﾉ☆  
  <br><br>
  <strong>“A cada salto, o coelhinho sonha mais alto.”</strong>  
  <br>
  <em>“With each jump, the bunny dreams higher.” 🌙</em>
</p>
