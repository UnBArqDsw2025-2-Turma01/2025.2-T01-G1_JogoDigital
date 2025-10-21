import pygame
from Template.BaseScreen import BaseScreen
from Model.Level import Level
from View.GameScreen.GameScreenRenderer import GameScreenRenderer
from Core.ScreenManager import ScreenManager
from View.Modal.PauseModal import PauseModal
from Template.UIConfigs import *

class GameScreen(BaseScreen):
    def __init__(self):
        super().__init__()

        Level.inicializar_mapa()

        self.current_level = None

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
        """Processa eventos específicos da GameScreen."""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                from View.ViewRenderer import ViewRenderer
                ViewRenderer.transition_to("level_select")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Botão PAUSE
            if self.pause_rect.collidepoint(x, y):
                ScreenManager.push_modal(PauseModal())

            # Botão ADICIONAR
            elif self.add_rect.collidepoint(x, y):
                self.state_vars['MODO_COLOCACAO_ATIVO'] = not self.state_vars['MODO_COLOCACAO_ATIVO']

            # Grid para colocar Caipora
            elif self.state_vars['MODO_COLOCACAO_ATIVO']:
                self._handle_grid_click(x, y)

            # Clique em guaraná (coletar)
            else:
                self._handle_guarana_click(x, y)
    
    def _handle_grid_click(self, x: int, y: int):
        """Processa clique no grid para colocar Caipora."""
        grid_x_min = GRID_OFFSET_X
        grid_x_max = GRID_OFFSET_X + NUM_COLUNAS * TAMANHO_QUADRADO
        grid_y_min = GRID_OFFSET_Y
        grid_y_max = GRID_OFFSET_Y + NUM_LINHAS * TAMANHO_QUADRADO

        if grid_x_min <= x < grid_x_max and grid_y_min <= y < grid_y_max:
            coluna = (x - GRID_OFFSET_X) // TAMANHO_QUADRADO
            linha = (y - GRID_OFFSET_Y) // TAMANHO_QUADRADO
            if Level.adicionar_entidade(linha, coluna, 'Caipora'):
                self.state_vars['MODO_COLOCACAO_ATIVO'] = False
    
    def _handle_guarana_click(self, x: int, y: int):
        """Processa clique em guaranás para coletar."""
        from Model.sprite_groups import guaranas_grupo
        
        for guarana in list(guaranas_grupo):
            if guarana.rect.collidepoint(x, y):
                guarana.collect()
                self.renderer.coins += guarana.value
                print(f"Guaraná coletado! Coins: {self.renderer.coins}")
                break

    def set_current_level(self, level):
        self.current_level = level
        print(f"Nível configurado: {level.name}")
        Level.inicializar_mapa()

    def update(self):
        self.state_vars['GAME_PAUSED'] = bool(ScreenManager._modals)
        self.renderer.update()

    def draw(self, surface):
        self.renderer.draw(surface)
