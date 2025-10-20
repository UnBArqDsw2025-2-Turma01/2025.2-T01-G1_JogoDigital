import pygame
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo, guaranas_grupo
from Model.Items.guarana import Guarana
from Template.PhysicsEngine import PhysicsEngine
from Template.TemplateRenderer import TemplateRenderer
from View.UIRenderer import UIRenderer
from Template.UIConfigs import GRID_OFFSET_X, GRID_OFFSET_Y, NUM_LINHAS, NUM_COLUNAS, TAMANHO_QUADRADO
from Core.ScreenManager import ScreenManager
from Model.Level import Level
from View.Modal.PauseModal import PauseModal
import random


class GameScreenRenderer:
    """Renderer específico da GameScreen, cuidando de mapa, entidades e UI."""

    def __init__(self, screen):
        self.screen = screen
        self.state_vars = screen.state_vars
        self.add_rect = screen.add_rect
        self.pause_rect = screen.pause_rect
        self.font = screen.font
        # Tempo para o próximo spawn (ms)
        self._tempo_proximo_spawn = 0
        # Contador de moedas coletadas (temporário, pode ser movido para player)
        self.coins = 0

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                ScreenManager.set_tela("menu")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if self.pause_rect.collidepoint(event.pos):
                ScreenManager.push_modal(PauseModal())
                self.state_vars['GAME_PAUSED'] = True

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

            # Clique em guaraná (coletar)
            else:
                # percorre os guaranás e verifica clique
                for guarana in list(guaranas_grupo):
                    if guarana.rect.collidepoint(x, y):
                        guarana.collect()
                        self.coins += guarana.value
                        print(f"Guaraná coletado! Coins: {self.coins}")
                        break

    def update(self):
        if not self.state_vars['GAME_PAUSED']:
            PhysicsEngine.processar_colisoes()
            caiporas_grupo.update()
            inimigos_grupo.update()
            projeteis_grupo.update()
            # Atualiza guaranás
            guaranas_grupo.update()

            # Spawn periódico de guaranás (caindo)
            now = pygame.time.get_ticks()
            if now >= self._tempo_proximo_spawn:
                # próximo spawn em 2-5 segundos aleatório
                intervalo = random.randint(2000, 5000)
                self._tempo_proximo_spawn = now + intervalo
                self.spawn_guarana()

    def spawn_guarana(self):
        """Cria um guaraná na parte superior da área do mapa em x aleatória."""
        # limita spawn à área do grid (para ficar sobre o mapa)
        grid_x_min = GRID_OFFSET_X
        grid_x_max = GRID_OFFSET_X + NUM_COLUNAS * TAMANHO_QUADRADO
        x = random.randint(grid_x_min + 20, grid_x_max - 20)
        y = GRID_OFFSET_Y - 30  # aparece um pouco acima do grid
        Guarana(x, y, value=1, speed=random.randint(2, 5))

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

        # Desenha guaranás por cima de tudo
        guaranas_grupo.draw(surface)

        # Texto centralizado de pausa
        if self.state_vars['GAME_PAUSED']:
            pausa_texto = self.font.render("JOGO PAUSADO", True, (255, 255, 255))
            surface.blit(pausa_texto, pausa_texto.get_rect(center=(surface.get_width()//2, surface.get_height()//2)))