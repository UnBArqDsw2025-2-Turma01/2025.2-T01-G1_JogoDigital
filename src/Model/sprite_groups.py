import pygame
from Template.UIConfigs import *

class SpriteComposite:
    """Gerenciador unificado de todos os grupos de sprites do jogo."""
    def __init__(self):
        self.caiporas = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.projeteis = pygame.sprite.Group()
        self.guaranas = pygame.sprite.Group()

        # Lista usada para atualização/desenho em sequência
        self._all_groups = [
            self.projeteis,   # projéteis primeiro (passam por cima)
            self.caiporas,
            self.inimigos,
            self.guaranas
        ]

    def update(self):
        """Atualiza todos os grupos de sprites."""
        for group in self._all_groups:
            group.update()

    def draw(self, surface):
        """Desenha todos os grupos de sprites na tela."""
        for group in self._all_groups:
            group.draw(surface)

    def reset(self):
        """Esvazia todos os grupos (ex: ao reiniciar o jogo)."""
        for group in self._all_groups:
            group.empty()

# Instância global única do composite (substitui os antigos *_grupo)
sprite_manager = SpriteComposite()


def get_posicao_tela(col, lin):
    """Converte coordenadas do grid para posição na tela."""
    x = GRID_OFFSET_X + col * TAMANHO_QUADRADO
    y = GRID_OFFSET_Y + lin * TAMANHO_QUADRADO
    return x, y