import pygame
from Template.BaseScreen import BaseScreen
from Model.Level import Level
from View.GameScreen.GameScreenRenderer import GameScreenRenderer

class GameScreen(BaseScreen):
    def __init__(self):
        super().__init__()

        Level.inicializar_mapa()

        # Estado da tela
        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

        # Botões específicos desta tela
        self.add_rect = pygame.Rect(50, 20, 120, 40)
        self.pause_rect = pygame.Rect(200, 20, 120, 40)
        self.coins_rect = pygame.Rect(350, 20, 120, 40)

        # Fonte
        self.font = pygame.font.SysFont(None, 24)

        # Cria o renderer desta tela
        self.renderer = GameScreenRenderer(self)

    def handle_event(self, event):
        self.renderer.handle_event(event)

    def update(self):
        self.renderer.update()

    def draw(self, surface):
        self.renderer.draw(surface)
