import pygame
from Core.ScreenManager import ScreenManager

class BaseScreen:
    """
    Classe base para telas.
    Implementa a interface IScreen para o padrão Facade.
    """

    def __init__(self):
        self._is_open = False

    def open_screen(self):
        """Chamado quando a screen é aberta (Facade Pattern)."""
        self._is_open = True
    
    def close_screen(self):
        """Chamado quando a screen é fechada (Facade Pattern)."""
        self._is_open = False
    
    def is_open(self) -> bool:
        """Retorna se a screen está aberta."""
        return self._is_open

    def handle_event(self, event: pygame.event.Event):
        """Trata eventos da tela."""
        pass

    def update(self):
        """Atualiza lógica e estado da tela."""
        pass

    def draw(self, surface: pygame.Surface):
        """Desenha conteúdo da tela."""
        pass