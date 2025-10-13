# Core/ScreenManager.py

import pygame
from Template.UIConfigs import *
from Asset.AssetProvider import AssetProvider

class ScreenManager:
    TELA = None
    RELOGIO = None
    
    @classmethod
    def inicializar_pygame(cls):
        """Inicializa Pygame, relógio e carrega assets."""
        pygame.init()
        
        if not pygame.font.get_init():
            pygame.font.init() 
            
        # 1. INICIALIZA A TELA ANTES DE CARREGAR AS IMAGENS
        cls.TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        
        # 2. CHAMA O CARREGAMENTO DE ASSETS (Agora é seguro)
        AssetProvider.carregar_assets()
        
        cls.RELOGIO = pygame.time.Clock() # Relógio não precisa de ordem específica
        
    @classmethod
    def get_tela(cls):
        return cls.TELA

    @classmethod
    def get_relogio(cls):
        return cls.RELOGIO