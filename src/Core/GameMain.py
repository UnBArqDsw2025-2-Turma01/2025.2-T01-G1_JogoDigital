import pygame
from Core.ScreenManager import ScreenManager
from Model.Level import Level
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Template.PhysicsEngine import PhysicsEngine
from View.ViewRenderer import ViewRenderer
from Template.UIConfigs import FPS
from View.MenuScreen.MenuScreen import MenuScreen
from View.GameScreen.GameScreen import GameScreen

"""
COMENTÁRIOS PARA ENTENDER A NOVA ESTRUTURA DO CÓDIGO:
1. Inicialização:
    - Pygame é inicializado pelo ScreenManager.
    - Todas as telas são registradas no ScreenManager.
    - A tela inicial (MenuScreen) é definida e a partir dela outras são acessadas.

2. Loop Principal:
    Enquanto o jogo estiver rodando:
        a) Eventos:
            - Captura eventos do Pygame (teclado, mouse, quit).
            - Encaminha os eventos para a tela atual.
            - Cada tela trata seus próprios eventos (ex: cliques, teclas de atalho).
            - (OU SEJA, CADA TELA LIDA COM OS PRÓPRIOS EVENTOS - Input Handler).
        
        b) Atualização (Update):
            - A tela atual atualiza seu estado (ex: movimentação, física, colisões).
            - Lógica de jogo é SEPARADA da renderização.

        c) Renderização (Draw):
            - A tela atual desenha todos os elementos visuais (mapa, sprites, UI).
            - UI global ou específica da tela é desenhada via renderer.
            - O display é atualizado (pygame.display.flip()).
"""

class GameMain:
    def __init__(self):
        # 1. Inicializa Pygame e carrega Assets
        ScreenManager.inicializar_pygame()
        
        # 2. Inicializa as fontes APÓS o Pyga estar pronto
        ViewRenderer.inicializar_fontes() 
        
        # 3. Inicializa o Mapa e as Entidades Iniciais
        Level.inicializar_mapa()
        
        # Variáveis de Estado do Jogo (centralizadas aqui)
        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

        telas = {
            "menu": MenuScreen(),
            "jogo": GameScreen()
        }

        ScreenManager.registrar_telas(telas)
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
