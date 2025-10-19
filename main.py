# -*- coding: utf-8 -*-
# ₊˚⊹🐇₊˚⊹  ENTRADA  ₊˚⊹🐇₊˚⊹
import pygame

def main() -> None:
    """Cria a janela do Buni"""
    # menos atraso no som
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    from game.game import Game

    game = Game(800, 480, title="Buni")
    game.run()

if __name__ == "__main__":
    main()
