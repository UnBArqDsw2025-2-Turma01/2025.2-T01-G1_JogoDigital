import pygame
from Model.Level import LevelStatus

class LevelSelectScreenRenderer:
    
    def __init__(self, screen):
        self.screen = screen
        
        self.COLOR_BG = (20, 30, 40)
        self.COLOR_LOCKED = (100, 100, 100)
        self.COLOR_UNLOCKED = (50, 150, 200)
        self.COLOR_COMPLETED = (50, 200, 100)
        self.COLOR_SELECTED = (255, 200, 50)
        self.COLOR_TEXT = (255, 255, 255)
        self.COLOR_BUTTON = (70, 70, 70)
        self.COLOR_BUTTON_HOVER = (100, 100, 100)
        self.COLOR_BUTTON_DISABLED = (50, 50, 50)
    
    def draw(self, surface):
        surface.fill(self.COLOR_BG)
        
        title = self.screen.font_title.render("SELEÇÃO DE NÍVEL", True, self.COLOR_TEXT)
        surface.blit(title, title.get_rect(centerx=surface.get_width()//2, top=30))
        
        self._desenhar_niveis(surface)
        
        self._desenhar_info_nivel(surface)
        
        self._desenhar_botoes(surface)
    
    def _desenhar_niveis(self, surface):

        cols = 3
        card_width = 250
        card_height = 200
        spacing_x = 50
        spacing_y = 30
        start_x = (surface.get_width() - (cols * card_width + (cols-1) * spacing_x)) // 2
        start_y = 150
        
        self.screen.level_rects.clear()
        
        for idx, level in enumerate(self.screen.levels):
            row = idx // cols
            col = idx % cols
            
            x = start_x + col * (card_width + spacing_x)
            y = start_y + row * (card_height + spacing_y)
            
            rect = pygame.Rect(x, y, card_width, card_height)
            self.screen.level_rects[level.level_id] = rect
            
            # Cor baseada no status
            if level.status == LevelStatus.LOCKED:
                color = self.COLOR_LOCKED
            elif level.status == LevelStatus.COMPLETED:
                color = self.COLOR_COMPLETED
            else:
                color = self.COLOR_UNLOCKED
            
            if self.screen.selected_level == level:
                border_color = self.COLOR_SELECTED
                border_width = 5
            else:
                border_color = color
                border_width = 2
            
            # Desenha card
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, border_color, rect, border_width)
            
            # Ícone de cadeado se bloqueado
            if level.status == LevelStatus.LOCKED:
                lock_text = self.screen.font_normal.render("BLOQUEADO", True, self.COLOR_TEXT)
                surface.blit(lock_text, lock_text.get_rect(center=(rect.centerx, rect.centery - 30)))
            
            name_parts = level.name.split(" - ")
            level_num = self.screen.font_normal.render(name_parts[0], True, self.COLOR_TEXT)
            surface.blit(level_num, level_num.get_rect(center=(rect.centerx, rect.centery)))
            
            if len(name_parts) > 1:
                level_name = self.screen.font_small.render(name_parts[1], True, self.COLOR_TEXT)
                surface.blit(level_name, level_name.get_rect(center=(rect.centerx, rect.centery + 35)))
            
            # Estrelas (se completado)
            if level.status == LevelStatus.COMPLETED:
                stars_text = self.screen.font_small.render(f"★ {level.stars_earned}/3", True, (255, 215, 0))
                surface.blit(stars_text, stars_text.get_rect(center=(rect.centerx, rect.bottom - 25)))
    
    def _desenhar_info_nivel(self, surface):
        if not self.screen.selected_level:
            info_text = self.screen.font_normal.render("Selecione um nível para jogar", True, self.COLOR_TEXT)
            surface.blit(info_text, info_text.get_rect(center=(surface.get_width()//2, 620)))
        else:
            level = self.screen.selected_level
            
            if level.status == LevelStatus.COMPLETED:
                status_text = f"Completado - {level.stars_earned}/3 estrelas"
                color = self.COLOR_COMPLETED
            else:
                status_text = "Novo nível!"
                color = self.COLOR_UNLOCKED
            
            status = self.screen.font_normal.render(status_text, True, color)
            surface.blit(status, status.get_rect(center=(surface.get_width()//2, 620)))
    
    def _desenhar_botoes(self, surface):
        pygame.draw.rect(surface, self.COLOR_BUTTON, self.screen.back_rect)
        pygame.draw.rect(surface, self.COLOR_TEXT, self.screen.back_rect, 2)
        back_text = self.screen.font_small.render("VOLTAR", True, self.COLOR_TEXT)
        surface.blit(back_text, back_text.get_rect(center=self.screen.back_rect.center))
        
        if self.screen.selected_level:
            color = self.COLOR_UNLOCKED
        else:
            color = self.COLOR_BUTTON_DISABLED
        
        pygame.draw.rect(surface, color, self.screen.play_rect)
        pygame.draw.rect(surface, self.COLOR_TEXT, self.screen.play_rect, 2)
        play_text = self.screen.font_small.render("JOGAR", True, self.COLOR_TEXT)
        surface.blit(play_text, play_text.get_rect(center=self.screen.play_rect.center))
