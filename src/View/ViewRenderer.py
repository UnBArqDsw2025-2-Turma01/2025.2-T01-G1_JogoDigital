# View/ViewRenderer.py

import pygame
from Template.UIConfigs import *
from Template.TemplateRenderer import TemplateRenderer
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Core.ScreenManager import ScreenManager

class ViewRenderer:
    # Fontes inicializadas como None
    FONTE = None
    FONTE_PEQUENA = None
    
    @classmethod
    def inicializar_fontes(cls):
        """Cria os objetos de fonte APÓS Pygame ter sido inicializado (no ScreenManager)."""
        if cls.FONTE is None:
            # Agora é seguro criar a fonte.
            cls.FONTE = pygame.font.SysFont('Arial', 30)
            cls.FONTE_PEQUENA = pygame.font.SysFont('Arial', 20)
    
    @classmethod
    def desenhar_ui(cls, MODO_COLOCACAO_ATIVO, GAME_PAUSED):
        """Desenha os botões ADICIONAR e PAUSE/RESUME."""
        tela = ScreenManager.get_tela()
        BOTAO_RECT = pygame.Rect(GRID_OFFSET_X, 50, LARGURA_BOTAO_ADD, ALTURA_BOTAO)
        PAUSE_RECT = pygame.Rect(BOTAO_PAUSE_X, 50, BOTAO_PAUSE_LARGURA, ALTURA_BOTAO)
        
        # Botão ADICIONAR
        cor_botao = VERDE_ATIVO if MODO_COLOCACAO_ATIVO else VERMELHO
        pygame.draw.rect(tela, cor_botao, BOTAO_RECT)
        # Usa a fonte já criada
        texto_surface = cls.FONTE_PEQUENA.render("ADD CAIPORA (Modo)", True, BRANCO)
        tela.blit(texto_surface, texto_surface.get_rect(center=BOTAO_RECT.center))
        
        # Botão PAUSE
        cor_pause = VERMELHO if GAME_PAUSED else (50, 50, 50)
        pygame.draw.rect(tela, cor_pause, PAUSE_RECT)
        # Usa a fonte já criada
        texto_pause = cls.FONTE_PEQUENA.render("PAUSE" if not GAME_PAUSED else "RESUME", True, BRANCO)
        tela.blit(texto_pause, texto_pause.get_rect(center=PAUSE_RECT.center))
        
        return BOTAO_RECT, PAUSE_RECT

    @classmethod
    def renderizar(cls, MODO_COLOCACAO_ATIVO, GAME_PAUSED):
        """Renderiza todos os elementos na tela."""
        tela = ScreenManager.get_tela()
        tela.fill(PRETO)
        
        TemplateRenderer.desenhar_mapa(tela)
        
        projeteis_grupo.draw(tela)
        caiporas_grupo.draw(tela)
        inimigos_grupo.draw(tela)
        
        ui_rects = cls.desenhar_ui(MODO_COLOCACAO_ATIVO, GAME_PAUSED)
        
        if GAME_PAUSED:
            # Usa a fonte já criada
            pausa_texto = cls.FONTE.render("JOGO PAUSADO", True, BRANCO)
            tela.blit(pausa_texto, pausa_texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2)))
        
        pygame.display.flip()
        return ui_rects