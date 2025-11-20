# Core/GameMain.py

import pygame
from Core.ScreenManager import ScreenManager
from Model.Level import Level
from Model.sprite_groups import sprite_manager
from Template.PhysicsEngine import PhysicsEngine
from View.ViewRenderer import ViewRenderer
from View.InputHandler import InputHandler
from View.MenuScreen.MenuScreen import MenuScreen
from View.GameScreen.GameScreen import GameScreen
from View.LevelSelectScreen.LevelSelectScreen import LevelSelectScreen
from View.DifficultScreen.DifficultScreen import DifficultScreen
from Model.Enemies.EnemyPrototype import initialize_enemy_prototypes
from Template.UIConfigs import FPS

class GameMain:
    def __init__(self):
        ScreenManager.inicializar_pygame()
        ViewRenderer.inicializar()
        InputHandler.inicializar()
        InputHandler.setup_default_shortcuts()
        
        initialize_enemy_prototypes()
        Level.inicializar_mapa()

        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

        ViewRenderer.add_screen("menu", MenuScreen())
        ViewRenderer.add_screen("level_select", LevelSelectScreen())
        ViewRenderer.add_screen("difficulty", DifficultScreen())
        ViewRenderer.add_screen("jogo", GameScreen())

        ViewRenderer.init_screens("menu")

    def update(self):
        """Atualização geral do jogo."""
        PhysicsEngine.processar_colisoes()
        sprite_manager.update()

    def loop(self):
        """Loop principal do jogo."""
        rodando = True
        relogio = ScreenManager.get_relogio()

        while rodando:
            rodando = InputHandler.process_events()
            ViewRenderer.update()
            ViewRenderer.render(ScreenManager.get_tela())
            pygame.display.flip()
            relogio.tick(FPS)

        pygame.quit()
