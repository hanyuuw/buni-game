# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  MENU (título / botões / scores / pause overlay)  ₊˚⊹🐇₊˚⊹
from __future__ import annotations

import pygame
from pygame.surface import Surface

from .constants import ASSETS_DIR

# ₊˚⊹🐇₊˚⊹  CARREGAMENTO DE FONTE  ₊˚⊹🐇₊˚⊹
def load_font(size: int, bold: bool = False) -> pygame.font.Font:
    """Tenta usar Tiny5-Regular.ttf; se não achar, cai pra sysfont."""
    font_path = ASSETS_DIR / "fonts" / "Tiny5-Regular.ttf"
    if font_path.is_file():
        return pygame.font.Font(str(font_path), size)
    return pygame.font.SysFont("consolas", size, bold=bold)

# ₊˚⊹🐇₊˚⊹  BOTÃO EM “CÁPSULA” PIXEL  ₊˚⊹🐇₊˚⊹
class Button:
    """Botão estilo cápsula (pixel vibe, sem PNG)."""
    def __init__(self, text: str, center: tuple[int, int], width: int = 200, height: int = 40):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.font = load_font(22, bold=True)

        # paleta fria / melancólica
        self.col_bg      = (54, 58, 70)
        self.col_bg_hov  = (68, 72, 86)
        self.col_border  = (104, 109, 124)
        self.col_inner   = (138, 142, 159)
        self.col_text    = (232, 234, 240)

    def draw(self, win: Surface, hovered: bool = False):
        btn = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        r = btn.get_rect()
        br = r.height // 2

        # base + contornos (limpo)
        bg = self.col_bg_hov if hovered else self.col_bg
        pygame.draw.rect(btn, self.col_border, r, width=2, border_radius=br)
        inner = r.inflate(-4, -4)
        pygame.draw.rect(btn, self.col_inner, inner, width=1, border_radius=inner.height // 2)
        pygame.draw.rect(btn, bg, r.inflate(-2, -2), border_radius=br)

        win.blit(btn, self.rect.topleft)

        # texto central
        label = self.font.render(self.text, True, self.col_text)
        tx = self.rect.centerx - label.get_width() // 2
        ty = self.rect.centery - label.get_height() // 2 + (-1 if hovered else 0)
        win.blit(label, (tx, ty))

    def is_hover(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)


# ₊˚⊹🐇₊˚⊹  MENU UI  ₊˚⊹🐇₊˚⊹
class Menu:
    """Desenha telas de menu, scores e o overlay do pause; lida com cliques."""
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height

        # fontes
        self.title_font = load_font(52, bold=True)  # “maiorzinho”, não gigante
        self.sub_font   = load_font(20)
        self.score_font = load_font(22, bold=True)

        # fundo do menu (opcional)
        self.menu_bg: Surface | None = None
        bg_path = ASSETS_DIR / "background" / "menu_bg.png"
        if bg_path.is_file():
            try:
                self.menu_bg = pygame.image.load(str(bg_path)).convert_alpha()
            except Exception:
                self.menu_bg = None

        # layout dos botões (Start / Score lado a lado; Exit abaixo)
        cy = self.height // 2 - 10
        self.btn_start = Button("Start",  (self.width // 2 - 110, cy), width=180, height=42)
        self.btn_score = Button("Score",  (self.width // 2 + 110, cy), width=180, height=42)
        self.btn_exit  = Button("Exit",   (self.width // 2,        cy + 64), width=160, height=40)

        # botão do pause
        self.btn_pause_menu = Button("Voltar ao menu", (self.width // 2, self.height // 2 + 90), width=260, height=40)

        # botão Back da tela de scores
        self.btn_scores_back = Button("Back", (self.width // 2, self.height - 80), width=160, height=40)

    # ₊˚⊹🐇₊˚⊹  DESENHO: MENU PRINCIPAL  ₊˚⊹🐇₊˚⊹
    def draw_menu(self, win: Surface, draw_game_bg_fallback: callable) -> None:
        """Desenha o menu inicial (usa menu_bg se existir; senão, o bg do jogo)."""
        if self.menu_bg:
            bg = self.menu_bg
            if bg.get_size() != win.get_size():
                bg = pygame.transform.smoothscale(bg, win.get_size())
            win.blit(bg, (0, 0))
        else:
            draw_game_bg_fallback(win)

        title = self.title_font.render("BUNI", True, (235, 235, 240))
        sub   = self.sub_font.render("Press ENTER or click Start", True, (200, 200, 205))
        win.blit(title, (self.width // 2 - title.get_width() // 2, 110))
        win.blit(sub,   (self.width // 2 - sub.get_width() // 2,   165))

        mx, my = pygame.mouse.get_pos()
        self.btn_start.draw(win, self.btn_start.is_hover((mx, my)))
        self.btn_score.draw(win, self.btn_score.is_hover((mx, my)))
        self.btn_exit.draw(win,  self.btn_exit.is_hover((mx, my)))

        pygame.display.flip()

    # ₊˚⊹🐇₊˚⊹  DESENHO: SCORES  ₊˚⊹🐇₊˚⊹
    def draw_scores(self, win: Surface, draw_game_bg_fallback: callable,
                    best_score: int, score_history: list[int]) -> None:
        """Tela de ranking simples da sessão, com botão Back."""
        if self.menu_bg:
            bg = self.menu_bg
            if bg.get_size() != win.get_size():
                bg = pygame.transform.smoothscale(bg, win.get_size())
            win.blit(bg, (0, 0))
        else:
            draw_game_bg_fallback(win)

        title = self.title_font.render("SCORES", True, (245, 245, 245))
        win.blit(title, (self.width // 2 - title.get_width() // 2, 80))

        best = self.score_font.render(f"Best (session): {best_score}", True, (240, 240, 240))
        win.blit(best, (self.width // 2 - best.get_width() // 2, 140))

        y = 190
        if score_history:
            last5 = score_history[-5:][::-1]
            for idx, sc in enumerate(last5, start=1):
                line = self.sub_font.render(f"{idx}. {sc}", True, (225, 225, 225))
                win.blit(line, (self.width // 2 - line.get_width() // 2, y))
                y += 26
        else:
            msg = self.sub_font.render("Sem partidas ainda :)", True, (220, 220, 220))
            win.blit(msg, (self.width // 2 - msg.get_width() // 2, y))

        # botão Back (no lugar do ENTER)
        mx, my = pygame.mouse.get_pos()
        self.btn_scores_back.draw(win, self.btn_scores_back.is_hover((mx, my)))

        pygame.display.flip()

    # ₊˚⊹🐇₊˚⊹  DESENHO: PAUSE OVERLAY  ₊˚⊹🐇₊˚⊹
    def draw_pause_overlay(self, win: Surface) -> None:
        """Overlay do pause com espaçamento confortável."""
        overlay = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        win.blit(overlay, (0, 0))

        txt  = self.title_font.render("PAUSED", True, (240, 240, 240))
        hint1 = self.sub_font.render("P para continuar", True, (220, 220, 220))
        hint2 = self.sub_font.render("ESC para sair", True, (220, 220, 220))

        center_x = self.width // 2
        cy = self.height // 2
        win.blit(txt,  (center_x - txt.get_width() // 2,  cy - 88))
        win.blit(hint1,(center_x - hint1.get_width() // 2, cy - 36))
        win.blit(hint2,(center_x - hint2.get_width() // 2, cy - 12))

        mx, my = pygame.mouse.get_pos()
        self.btn_pause_menu.draw(win, self.btn_pause_menu.is_hover((mx, my)))

        pygame.display.flip()

    # ₊˚⊹🐇₊˚⊹  CLIQUES: MENU  ₊˚⊹🐇₊˚⊹
    def handle_menu_click(self, pos: tuple[int, int]) -> str | None:
        """Retorna 'start' | 'scores' | 'exit' conforme o botão clicado."""
        if self.btn_start.is_hover(pos):
            return "start"
        if self.btn_score.is_hover(pos):
            return "scores"
        if self.btn_exit.is_hover(pos):
            return "exit"
        return None

    # ₊˚⊹🐇₊˚⊹  CLIQUES: SCORES  ₊˚⊹🐇₊˚⊹
    def handle_scores_click(self, pos: tuple[int, int]) -> bool:
        """True se clicou em 'Back'."""
        return self.btn_scores_back.is_hover(pos)

    # ₊˚⊹🐇₊˚⊹  CLIQUES: PAUSE  ₊˚⊹🐇₊˚⊹
    def handle_pause_click(self, pos: tuple[int, int]) -> bool:
        """True se clicou em 'Voltar ao menu'."""
        return self.btn_pause_menu.is_hover(pos)
