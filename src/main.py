import sys
import os

try:
    from Core.GameMain import GameMain
except ImportError as e:
    print(f"Erro ao importar GameMain: {e}")
    print("Tentando adicionar o diretório atual ao sys.path para resolver importações.")
    # Adiciona o diretório atual ao sys.path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from Core.GameMain import GameMain


if __name__ == "__main__":
    # Cria uma instância e inicia o loop do jogo
    game = GameMain()
    game.loop()
