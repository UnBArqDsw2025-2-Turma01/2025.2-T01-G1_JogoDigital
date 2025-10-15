import sys
import os
import pygame

try:
    from Core.GameMain import GameMain
except ImportError as e:
    print(f"Erro ao importar GameMain: {e}")
    print("Tentando adicionar o diretório atual ao sys.path para resolver importações.")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from Core.GameMain import GameMain


if __name__ == "__main__":
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h))
    game = GameMain()
    game.loop()
