# ₊˚⊹🐇₊˚⊹  ENTRADA  ₊˚⊹🐇₊˚⊹
from game.game import Game


def main():
    """Cria a janela do Buni e inicia o loop do jogo."""
    game = Game(800, 480, title="Buni")
    game.run()


if __name__ == "__main__":
    main()
