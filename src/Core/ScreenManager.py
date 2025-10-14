import pygame
from Template.UIConfigs import *
from Asset.AssetProvider import AssetProvider

class ScreenManager:
    TELA = None
    RELOGIO = None
    _telas = {}
    _tela_atual = None

    # --- 1. Inicialização global ---
    @classmethod
    def inicializar_pygame(cls):
        """Inicializa Pygame, relógio e carrega assets."""
        pygame.init()
        
        if not pygame.font.get_init():
            pygame.font.init() 
            
        cls.TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO_JOGO)
        
        AssetProvider.carregar_assets()
        
        cls.RELOGIO = pygame.time.Clock()

    @classmethod
    def get_tela(cls):
        return cls.TELA

    @classmethod
    def get_relogio(cls):
        return cls.RELOGIO

    # --- 2. Sistema de telas ---
    @classmethod
    def registrar_telas(cls, telas_dict):
        """
        Recebe um dicionário com todas as telas do jogo.
        Exemplo: { 'menu': MenuScreen(), 'jogo': GameScreen() }
        """
        cls._telas = telas_dict

    @classmethod
    def set_tela(cls, nome_tela):
        """Troca a tela atual."""
        if nome_tela in cls._telas:
            cls._tela_atual = cls._telas[nome_tela]

    @classmethod
    def get_tela_atual(cls):
        return cls._tela_atual

    @classmethod
    def handle_events(cls):
        """Encaminha eventos para a tela atual."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if cls._tela_atual:
                cls._tela_atual.handle_event(event)
        return True

    @classmethod
    def update(cls):
        if cls._tela_atual:
            cls._tela_atual.update()

    @classmethod
    def draw(cls):
        if cls._tela_atual:
            cls._tela_atual.draw(cls.TELA)
            pygame.display.flip()
