import pygame
from Template.UIConfigs import *

caiporas_grupo = pygame.sprite.Group()
inimigos_grupo = pygame.sprite.Group()
projeteis_grupo = pygame.sprite.Group()
guaranas_grupo = pygame.sprite.Group()

def get_posicao_tela(col, lin):
    """Converte coordenadas do grid para posição na tela."""
    x = GRID_OFFSET_X + col * TAMANHO_QUADRADO
    y = GRID_OFFSET_Y + lin * TAMANHO_QUADRADO
    return x, y