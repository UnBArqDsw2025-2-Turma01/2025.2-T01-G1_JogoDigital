import pygame
from Core.ScreenManager import ScreenManager

class BaseScreen:
    """
    Classe base para telas.
    Fornece interface padrão + hooks opcionais de ciclo de vida.
    """

    def __init__(self):
        # tela e relógio do jogo, se quiser usar
        self.surface = ScreenManager.get_tela()
        self.relogio = ScreenManager.get_relogio()
        self.assets = None

    def handle_event(self, event: pygame.event.Event):
        """Trata eventos da tela."""
        pass

    def update(self):
        """Atualiza lógica e estado da tela."""
        pass

    def draw(self, surface: pygame.Surface):
        """Desenha conteúdo da tela."""
        pass

    def on_enter(self, **kwargs):
        """Chamado quando a tela se torna ativa."""
        pass

    def on_exit(self):
        """Chamado quando a tela deixa de estar ativa."""
        pass

    @classmethod
    def set_tela(cls, nome_tela):
        """Troca a tela atual."""
        if nome_tela in cls._telas:
            if cls._tela_atual:
                cls._tela_atual.on_exit()

            cls._tela_atual = cls._telas[nome_tela]
            cls._tela_atual.on_enter()
