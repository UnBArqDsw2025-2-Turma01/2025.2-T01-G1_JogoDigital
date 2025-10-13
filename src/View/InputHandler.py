# View/InputHandler.py

# REMOVA ESTA LINHA: from Core.EventManager import EventManager 
from Template.UIConfigs import *
from Model.Level import Level
from View.ViewRenderer import ViewRenderer
import pygame # Necessário para MOUSEBUTTONDOWN

class InputHandler:
    # Mudamos o método para aceitar o 'evento' de Pygame
    @classmethod
    def handle_event(cls, evento, state_vars):
        """Processa eventos específicos (mouse, teclado, etc.)."""
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = evento.pos
            
            # O resto da sua lógica de handle_mouse_click vem para cá.
            # (Mantendo o conteúdo anterior para brevidade, mas garantindo que use evento.pos)
            
            MODO_COLOCACAO_ATIVO = state_vars['MODO_COLOCACAO_ATIVO']
            GAME_PAUSED = state_vars['GAME_PAUSED']
            
            # Renderiza primeiro para obter os rects dos botões
            ui_rects = ViewRenderer.renderizar(MODO_COLOCACAO_ATIVO, GAME_PAUSED) 
            add_rect, pause_rect = ui_rects

            # 1. Clique no botão ADICIONAR
            if add_rect.collidepoint(mouse_x, mouse_y):
                state_vars['MODO_COLOCACAO_ATIVO'] = not MODO_COLOCACAO_ATIVO
                print(f"Modo Colocação: {'ATIVO' if state_vars['MODO_COLOCACAO_ATIVO'] else 'INATIVO'}")
                
            # 2. Clique no botão PAUSE/RESUME
            elif pause_rect.collidepoint(mouse_x, mouse_y):
                state_vars['GAME_PAUSED'] = not GAME_PAUSED
                print(f"Jogo: {'PAUSADO' if state_vars['GAME_PAUSED'] else 'RODANDO'}")
                
            # 3. Clique no grid
            elif MODO_COLOCACAO_ATIVO:
                grid_area_x_min = GRID_OFFSET_X
                grid_area_x_max = GRID_OFFSET_X + NUM_COLUNAS * TAMANHO_QUADRADO
                grid_area_y_min = GRID_OFFSET_Y
                grid_area_y_max = GRID_OFFSET_Y + NUM_LINHAS * TAMANHO_QUADRADO
                
                if (grid_area_x_min <= mouse_x < grid_area_x_max and
                    grid_area_y_min <= mouse_y < grid_area_y_max):
                    
                    coluna = (mouse_x - GRID_OFFSET_X) // TAMANHO_QUADRADO
                    linha = (mouse_y - GRID_OFFSET_Y) // TAMANHO_QUADRADO
                    
                    if Level.adicionar_entidade(linha, coluna, 'Caipora'):
                        state_vars['MODO_COLOCACAO_ATIVO'] = False 
                        print(f"Caipora adicionado em: ({linha}, {coluna})")
            
        return state_vars