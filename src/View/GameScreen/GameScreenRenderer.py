# View/GameScreen/GameScreenRenderer.py

import pygame
import random
from Model.sprite_groups import sprite_manager
from Model.Items.guarana import Guarana
from Template.PhysicsEngine import PhysicsEngine
from Template.TemplateRenderer import TemplateRenderer
from View.UIRenderer import UIRenderer
from Template.UIConfigs import *
from Core.ScreenManager import ScreenManager
from Model.Level import Level
from View.Modal.PauseModal import PauseModal
from Asset.AssetProvider import AssetProvider

class GameScreenRenderer:
    """Renderer específico da GameScreen, cuidando de mapa, entidades e UI."""

    def __init__(self, screen):
        self.screen = screen
        self.state_vars = screen.state_vars
        self.add_rect = screen.add_rect
        self.pause_rect = screen.pause_rect
        self.coins_rect = screen.coins_rect
        self.font = screen.font
        self._tempo_proximo_spawn = 0
        self.coins = 0
        self.score_board = AssetProvider.get('scoreboard')
        self.score_board_slot = AssetProvider.get('scoreboard_slot')
        self.font_scoreboard = AssetProvider.get('font_press_start_2P')
        self.caipora_icon = AssetProvider.get('caipora_icon')

    def update(self):
        """Atualiza a lógica do jogo e entidades."""
        if not self.state_vars['GAME_PAUSED']:
            PhysicsEngine.processar_colisoes()
            sprite_manager.update()

            now = pygame.time.get_ticks()
            if now >= self._tempo_proximo_spawn:
                intervalo = random.randint(2000, 5000)
                self._tempo_proximo_spawn = now + intervalo
                self.spawn_guarana()

    def spawn_guarana(self):
        """Cria um guaraná em posição aleatória no topo do mapa."""
        grid_x_min = GRID_OFFSET_X
        grid_x_max = GRID_OFFSET_X + NUM_COLUNAS * TAMANHO_QUADRADO
        x = random.randint(grid_x_min + 20, grid_x_max - 20)
        y = GRID_OFFSET_Y - 30
        Guarana(x, y, value=1, speed=random.randint(2, 5))

    def draw(self, surface):
        """Renderiza todos os elementos visuais da GameScreen."""
        surface.fill((0, 0, 0))
        TemplateRenderer.desenhar_mapa(surface)

        # Desenha todos os grupos de sprites
        sprite_manager.draw(surface)

        # --- UI ---
        scoreboard_pos_x = LARGURA_TELA_JANELA // 2 - self.score_board.get_width() // 2
        surface.blit(self.score_board, (scoreboard_pos_x, 0))
        coins_text = self.font_scoreboard.render(f"{self.coins:03d}", True, (241, 245, 48))
        surface.blit(coins_text, (scoreboard_pos_x + TAMANHO_QUADRADO - 45, (TAMANHO_QUADRADO * 1.3) // 2))

        sb_slot_pos_x_init = scoreboard_pos_x + TAMANHO_QUADRADO * 1.5
        slot_gap = 10
        for i in range(5):
            x_slot = sb_slot_pos_x_init + i * (TAMANHO_QUADRADO / 2 + slot_gap)
            surface.blit(self.score_board_slot, (x_slot, (TAMANHO_QUADRADO - slot_gap) / 2))

        cor_add = (0, 200, 0) if self.state_vars['MODO_COLOCACAO_ATIVO'] else (100, 100, 100)
        cor_pause = (200, 0, 0) if self.state_vars['GAME_PAUSED'] else (50, 50, 50)
        UIRenderer.desenhar_botao(surface, self.add_rect, cor_add, "ADICIONAR", self.font)
        UIRenderer.desenhar_botao(surface, self.pause_rect, cor_pause, "PAUSE", self.font)

        if self.state_vars['GAME_PAUSED']:
            pausa_texto = self.font.render("JOGO PAUSADO", True, (255, 255, 255))
            surface.blit(pausa_texto, pausa_texto.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))
