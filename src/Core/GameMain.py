import pygame
from Core.ScreenManager import ScreenManager
from Model.Level import Level
from View.ViewRenderer import ViewRenderer
from View.InputHandler import InputHandler
from View.MenuScreen.MenuScreen import MenuScreen
from View.GameScreen.GameScreen import GameScreen
from Template.UIConfigs import FPS
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Model.concrete import IterableSpriteGroup
from Model.Defense.caipora import Caipora
from Model.Enemies.enemy import Enemy
from Model.Items.arrow import Arrow

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

        # Criação dos iteráveis usando o adaptador
        self.iterable_caiporas = IterableSpriteGroup[Caipora](caiporas_grupo)
        self.iterable_inimigos = IterableSpriteGroup[Enemy](inimigos_grupo)
        self.iterable_projeteis = IterableSpriteGroup[Arrow](projeteis_grupo)
        
        ViewRenderer.add_screen("menu", MenuScreen())

        # Adiciona a GameScreen com os iteráveis
        ViewRenderer.add_screen("jogo", GameScreen(
            self.iterable_caiporas,
            self.iterable_inimigos,
            self.iterable_projeteis
        ))

        ViewRenderer.init_screens("menu")
        
    def loop(self):
        """Loop principal do jogo."""
        rodando = True
        relogio = ScreenManager.get_relogio()
        
        while rodando:
            rodando = InputHandler.process_events()

            ViewRenderer.update() # Isso chama o update do GameScreenRenderer
            ViewRenderer.render(ScreenManager.get_tela())
            
            pygame.display.flip()
            relogio.tick(FPS)
            
        pygame.quit()
        import sys
        sys.exit()