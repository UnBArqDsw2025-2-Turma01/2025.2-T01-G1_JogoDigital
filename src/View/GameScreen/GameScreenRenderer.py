import pygame
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Template.PhysicsEngine import PhysicsEngine
from Template.TemplateRenderer import TemplateRenderer
from View.UIRenderer import UIRenderer
from Template.UIConfigs import GRID_OFFSET_X, GRID_OFFSET_Y, NUM_LINHAS, NUM_COLUNAS, TAMANHO_QUADRADO
from Core.ScreenManager import ScreenManager
from Model.Level import Level

class GameScreenRenderer:
    """Renderer específico da GameScreen, cuidando de mapa, entidades e UI."""

    def __init__(self, screen):
        self.screen = screen
        self.state_vars = screen.state_vars
        self.add_rect = screen.add_rect
        self.pause_rect = screen.pause_rect
        self.font = screen.font

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state_vars['GAME_PAUSED'] = not self.state_vars['GAME_PAUSED']
            elif event.key == pygame.K_m:
                ScreenManager.set_tela("menu")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Botão ADICIONAR
            if self.add_rect.collidepoint(x, y):
                self.state_vars['MODO_COLOCACAO_ATIVO'] = not self.state_vars['MODO_COLOCACAO_ATIVO']

            # Botão PAUSE
            elif self.pause_rect.collidepoint(x, y):
                self.state_vars['GAME_PAUSED'] = not self.state_vars['GAME_PAUSED']

            # Grid para colocar Caipora
            elif self.state_vars['MODO_COLOCACAO_ATIVO']:
                grid_x_min = GRID_OFFSET_X
                grid_x_max = GRID_OFFSET_X + NUM_COLUNAS * TAMANHO_QUADRADO
                grid_y_min = GRID_OFFSET_Y
                grid_y_max = GRID_OFFSET_Y + NUM_LINHAS * TAMANHO_QUADRADO

                if grid_x_min <= x < grid_x_max and grid_y_min <= y < grid_y_max:
                    coluna = (x - GRID_OFFSET_X) // TAMANHO_QUADRADO
                    linha = (y - GRID_OFFSET_Y) // TAMANHO_QUADRADO
                    if Level.adicionar_entidade(linha, coluna, 'Caipora'):
                        self.state_vars['MODO_COLOCACAO_ATIVO'] = False

    def update(self):
        if not self.state_vars['GAME_PAUSED']:
            PhysicsEngine.processar_colisoes()
            caiporas_grupo.update()
            inimigos_grupo.update()
            projeteis_grupo.update()

    def draw(self, surface):
        # Fundo
        surface.fill((0, 0, 0))

        # Mapa
        TemplateRenderer.desenhar_mapa(surface)

        # Entidades
        projeteis_grupo.draw(surface)
        caiporas_grupo.draw(surface)
        inimigos_grupo.draw(surface)

        # UI (botões)
        cor_add = (0, 200, 0) if self.state_vars['MODO_COLOCACAO_ATIVO'] else (100, 100, 100)
        cor_pause = (200, 0, 0) if self.state_vars['GAME_PAUSED'] else (50, 50, 50)
        UIRenderer.desenhar_botao(surface, self.add_rect, cor_add, "ADICIONAR", self.font)
        UIRenderer.desenhar_botao(surface, self.pause_rect, cor_pause, "PAUSE", self.font)

        # Texto centralizado de pausa
        if self.state_vars['GAME_PAUSED']:
            pausa_texto = self.font.render("JOGO PAUSADO", True, (255, 255, 255))
            surface.blit(pausa_texto, pausa_texto.get_rect(center=(surface.get_width()//2, surface.get_height()//2)))

        pygame.display.flip()
