import pygame
import os
from Template.UIConfigs import *
from Asset.AssetProvider import AssetProvider

class ScreenManager:
    TELA = None
    RELOGIO = None
    _telas = {}
    _tela_atual = None
    _modals = []  # pilha de modais/overlays

    # --- 1. Inicialização global ---
    @classmethod
    def inicializar_pygame(cls):
        """Inicializa Pygame, relógio e carrega assets."""
        pygame.init()
        pygame.mixer.init()
        song_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Asset', 'songs', 'forest.wav'))
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(-1)

        if not pygame.font.get_init():
            pygame.font.init() 
            
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        cls.TELA = pygame.display.set_mode((LARGURA_TELA_JANELA, ALTURA_TELA_JANELA))
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
            # Eventos vão primeiro para o modal no topo (se houver)
            if cls._modals:
                top = cls._modals[-1]
                res = top.handle_event(event)
                # se modal indicar fechar com 'close', desempilha
                if res == 'close':
                    cls.pop_modal()
                continue
            if cls._tela_atual:
                cls._tela_atual.handle_event(event)
        return True

    @classmethod
    def update(cls):
        # atualiza tela base apenas se não houver modal que bloqueie
        if cls._tela_atual:
            if not cls._modals:
                cls._tela_atual.update()
            else:
                # atualiza apenas o topo das modais
                top = cls._modals[-1]
                if hasattr(top, 'update'):
                    top.update()

    @classmethod
    def draw(cls):
        if cls._tela_atual:
            cls._tela_atual.draw(cls.TELA)
            # desenha modais em ordem
            for modal in cls._modals:
                modal.draw(cls.TELA)
            pygame.display.flip()

    @classmethod
    def push_modal(cls, modal):
        cls._modals.append(modal)

    @classmethod
    def pop_modal(cls):
        if cls._modals:
            cls._modals.pop()
