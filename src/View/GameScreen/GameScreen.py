import pygame
from Template.BaseScreen import BaseScreen
from Model.Level import Level
from View.GameScreen.GameScreenRenderer import GameScreenRenderer

class GameScreen(BaseScreen):
    def __init__(self):
        super().__init__()

        self.current_level = None

        Level.inicializar_mapa()

        # Estado da tela
        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

        # Botões específicos desta tela
        self.add_rect = pygame.Rect(50, 20, 120, 40)
        self.pause_rect = pygame.Rect(200, 20, 120, 40)
        self.back_rect = pygame.Rect(350, 20, 150, 40)

        # Fonte
        self.font = pygame.font.SysFont(None, 24)

        # Cria o renderer desta tela
        self.renderer = GameScreenRenderer(self)
    
    def reiniciar_jogo(self):
        from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo, guaranas_grupo
        caiporas_grupo.empty()
        inimigos_grupo.empty()
        projeteis_grupo.empty()
        guaranas_grupo.empty()
        
        Level.inicializar_mapa()
        
        self.state_vars['MODO_COLOCACAO_ATIVO'] = False
        self.state_vars['GAME_PAUSED'] = False
        
        self.renderer.coins = 0
        self.renderer._tempo_proximo_spawn = 0
        
        print(f"Jogo reiniciado para: {self.current_level.name if self.current_level else 'Nível padrão'}")

    def handle_event(self, event):
        self.renderer.handle_event(event)

    def update(self):
        self.renderer.update()

    def draw(self, surface):
        self.renderer.draw(surface)
