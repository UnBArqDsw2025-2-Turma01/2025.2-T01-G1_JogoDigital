# Template/TemplateRenderer.py

import pygame
from Template.UIConfigs import *
from Asset.AssetProvider import AssetProvider

class TemplateRenderer:
    @classmethod
    def desenhar_mapa(cls, tela):
        """Desenha o grid 9x5 com o padrão xadrez."""
        grass_claro = AssetProvider.get('grass_claro')
        grass_escuro = AssetProvider.get('grass_escuro')
        
        for linha in range(NUM_LINHAS):
            for coluna in range(NUM_COLUNAS):
                pos_x = GRID_OFFSET_X + coluna * TAMANHO_QUADRADO
                pos_y = GRID_OFFSET_Y + linha * TAMANHO_QUADRADO
                asset_mapa = grass_claro if (linha + coluna) % 2 == 0 else grass_escuro
                tela.blit(asset_mapa, (pos_x, pos_y))