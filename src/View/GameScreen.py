import pygame
from Template.BaseScreen import BaseScreen
from Core.EventManager import EventManager
from Model.Level import Level
from Model.Entities import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Template.PhysicsEngine import PhysicsEngine
from View.ViewRenderer import ViewRenderer
from Template.UIConfigs import FPS

class GameScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        Level.inicializar_mapa()
        ViewRenderer.inicializar_fontes()

        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state_vars['GAME_PAUSED'] = not self.state_vars['GAME_PAUSED']
            elif event.key == pygame.K_m:
                from Core.ScreenManager import ScreenManager
                ScreenManager.set_tela("menu")  # volta ao menu

    def update(self):
        if not self.state_vars['GAME_PAUSED']:
            PhysicsEngine.processar_colisoes()
            caiporas_grupo.update()
            inimigos_grupo.update()
            projeteis_grupo.update()

    def draw(self, surface):
        ViewRenderer.renderizar(
            self.state_vars['MODO_COLOCACAO_ATIVO'],
            self.state_vars['GAME_PAUSED']
        )