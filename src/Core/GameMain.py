import pygame
from Core.ScreenManager import ScreenManager
from Model.Level import Level
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Template.PhysicsEngine import PhysicsEngine
from View.ViewRenderer import ViewRenderer
from View.InputHandler import InputHandler
from Template.UIConfigs import FPS

class GameMain:
    def __init__(self):
        # 1. Inicializa Pygame e carrega Assets
        ScreenManager.inicializar_pygame()
        
        # 2. Inicializa o ViewRenderer Hub (fontes e recursos)
        ViewRenderer.inicializar()
        
        # 3. Inicializa o InputHandler Hub (gerenciamento de inputs)
        InputHandler.inicializar()
        InputHandler.registrar_atalhos_padrao()
        
        # 4. Inicializa o Mapa e as Entidades Iniciais
        Level.inicializar_mapa()
        
        # Variáveis de Estado do Jogo (centralizadas aqui)
        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

        # Registra nomes de screens (ViewRenderer cria as instâncias automaticamente)
        ScreenManager.registrar_screens_via_hub(["menu", "jogo"])
        ScreenManager.set_tela("menu")

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
            rodando = ScreenManager.handle_events()  # já captura e repassa eventos
            ScreenManager.update()
            ScreenManager.draw()
            relogio.tick(FPS)
            
        pygame.quit()
