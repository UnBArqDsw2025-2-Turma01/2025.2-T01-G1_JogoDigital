# View/ViewRenderer.py

import pygame
from Template.UIConfigs import *
from Template.TemplateRenderer import TemplateRenderer
from Model.sprite_groups import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Core.ScreenManager import ScreenManager
from Model.Level import LevelStatus

class ViewRenderer:
    # Fontes inicializadas como None
    FONTE = None
    FONTE_PEQUENA = None
    FONTE_TITULO = None
    FONTE_NORMAL = None
    
    @classmethod
    def inicializar_fontes(cls):
        """Cria os objetos de fonte APÓS Pygame ter sido inicializado (no ScreenManager)."""
        if cls.FONTE is None:
            # Agora é seguro criar a fonte.
            cls.FONTE = pygame.font.SysFont('Arial', 30)
            cls.FONTE_PEQUENA = pygame.font.SysFont('Arial', 20)
            cls.FONTE_TITULO = pygame.font.Font(None, 80)
            cls.FONTE_NORMAL = pygame.font.Font(None, 40)
    
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
    
    
    @classmethod
    def renderizar_level_select(cls, surface, levels, selected_level, level_rects, back_rect, play_rect):
        COLOR_BG = (20, 30, 40)
        COLOR_TEXT = (255, 255, 255)
        
        surface.fill(COLOR_BG)
        
        title = cls.FONTE_TITULO.render("SELEÇÃO DE NÍVEL", True, COLOR_TEXT)
        surface.blit(title, title.get_rect(centerx=surface.get_width()//2, top=30))
        
        cls._desenhar_niveis_grid(surface, levels, selected_level, level_rects)
        
        cls._desenhar_info_nivel_selecionado(surface, selected_level)
        
        cls._desenhar_botoes_level_select(surface, back_rect, play_rect, selected_level)
    
    @classmethod
    def _desenhar_niveis_grid(cls, surface, levels, selected_level, level_rects):
        COLOR_LOCKED = (100, 100, 100)
        COLOR_UNLOCKED = (50, 150, 200)
        COLOR_COMPLETED = (50, 200, 100)
        COLOR_SELECTED = (255, 200, 50)
        COLOR_TEXT = (255, 255, 255)
        
        cols = 3
        card_width = 250
        card_height = 200
        spacing_x = 50
        spacing_y = 30
        start_x = (surface.get_width() - (cols * card_width + (cols-1) * spacing_x)) // 2
        start_y = 150
        
        level_rects.clear()
        
        for idx, level in enumerate(levels):
            row = idx // cols
            col = idx % cols
            
            x = start_x + col * (card_width + spacing_x)
            y = start_y + row * (card_height + spacing_y)
            
            rect = pygame.Rect(x, y, card_width, card_height)
            level_rects[level.level_id] = rect
            
            if level.status == LevelStatus.LOCKED:
                color = COLOR_LOCKED
            elif level.status == LevelStatus.COMPLETED:
                color = COLOR_COMPLETED
            else:
                color = COLOR_UNLOCKED
            
            if selected_level == level:
                border_color = COLOR_SELECTED
                border_width = 5
            else:
                border_color = color
                border_width = 2
            
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, border_color, rect, border_width)
            
            if level.status == LevelStatus.LOCKED:
                lock_text = cls.FONTE_NORMAL.render("BLOQUEADO", True, COLOR_TEXT)
                surface.blit(lock_text, lock_text.get_rect(center=(rect.centerx, rect.centery - 30)))
            
            name_parts = level.name.split(" - ")
            level_num = cls.FONTE_NORMAL.render(name_parts[0], True, COLOR_TEXT)
            surface.blit(level_num, level_num.get_rect(center=(rect.centerx, rect.centery)))
            
            if len(name_parts) > 1:
                level_name = cls.FONTE_PEQUENA.render(name_parts[1], True, COLOR_TEXT)
                surface.blit(level_name, level_name.get_rect(center=(rect.centerx, rect.centery + 35)))
            
            if level.status == LevelStatus.COMPLETED:
                stars_text = cls.FONTE_PEQUENA.render(f"★ {level.stars_earned}/3", True, (255, 215, 0))
                surface.blit(stars_text, stars_text.get_rect(center=(rect.centerx, rect.bottom - 25)))
    
    @classmethod
    def _desenhar_info_nivel_selecionado(cls, surface, selected_level):
        COLOR_TEXT = (255, 255, 255)
        COLOR_COMPLETED = (50, 200, 100)
        COLOR_UNLOCKED = (50, 150, 200)
        
        if not selected_level:
            info_text = cls.FONTE_NORMAL.render("Selecione um nível para jogar", True, COLOR_TEXT)
            surface.blit(info_text, info_text.get_rect(center=(surface.get_width()//2, 620)))
        else:
            if selected_level.status == LevelStatus.COMPLETED:
                status_text = f"Completado - {selected_level.stars_earned}/3 estrelas"
                color = COLOR_COMPLETED
            else:
                status_text = "Novo nível!"
                color = COLOR_UNLOCKED
            
            status = cls.FONTE_NORMAL.render(status_text, True, color)
            surface.blit(status, status.get_rect(center=(surface.get_width()//2, 620)))
    
    @classmethod
    def _desenhar_botoes_level_select(cls, surface, back_rect, play_rect, selected_level):
        COLOR_BUTTON = (70, 70, 70)
        COLOR_TEXT = (255, 255, 255)
        COLOR_UNLOCKED = (50, 150, 200)
        COLOR_BUTTON_DISABLED = (50, 50, 50)
        
        # Botão VOLTAR
        pygame.draw.rect(surface, COLOR_BUTTON, back_rect)
        pygame.draw.rect(surface, COLOR_TEXT, back_rect, 2)
        back_text = cls.FONTE_PEQUENA.render("VOLTAR", True, COLOR_TEXT)
        surface.blit(back_text, back_text.get_rect(center=back_rect.center))
        
        # Botão JOGAR
        if selected_level:
            color = COLOR_UNLOCKED
        else:
            color = COLOR_BUTTON_DISABLED
        
        pygame.draw.rect(surface, color, play_rect)
        pygame.draw.rect(surface, COLOR_TEXT, play_rect, 2)
        play_text = cls.FONTE_PEQUENA.render("JOGAR", True, COLOR_TEXT)
        surface.blit(play_text, play_text.get_rect(center=play_rect.center))