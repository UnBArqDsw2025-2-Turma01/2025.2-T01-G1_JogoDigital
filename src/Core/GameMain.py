import pygame
from Core.ScreenManager import ScreenManager
from Model.Level import Level
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Template.PhysicsEngine import PhysicsEngine
from View.ViewRenderer import ViewRenderer
from View.InputHandler import InputHandler
from View.MenuScreen.MenuScreen import MenuScreen
from View.GameScreen.GameScreen import GameScreen
from View.LevelSelectScreen.LevelSelectScreen import LevelSelectScreen
from Template.UIConfigs import FPS

class GameMain:
    def __init__(self):
        ScreenManager.inicializar_pygame()

        ViewRenderer.inicializar()

        InputHandler.inicializar()
        InputHandler.setup_default_shortcuts()

        Level.inicializar_mapa()

        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

        ViewRenderer.add_screen("menu", MenuScreen())
        ViewRenderer.add_screen("level_select", LevelSelectScreen())
        ViewRenderer.add_screen("jogo", GameScreen())

        ViewRenderer.init_screens("menu")

    def update(self):
        """Lógica de atualização do jogo."""
        
        PhysicsEngine.processar_colisoes()
        
        caiporas_grupo.update()
        inimigos_grupo.update()
        projeteis_grupo.update()
        
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
