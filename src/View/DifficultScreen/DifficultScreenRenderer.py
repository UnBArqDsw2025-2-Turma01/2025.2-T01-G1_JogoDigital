import pygame
from Asset.AssetProvider import AssetProvider  
from View.ViewRenderer import ViewRenderer      

class DifficultScreenRenderer:
    
    def __init__(self, screen):
        self.screen = screen
        
        self.bg_color = (20, 30, 40)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (128, 128, 128)
        self.dark_gray = (64, 64, 64)
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 149, 237)
        self.disabled_color = (100, 100, 100)
    
    def draw(self, surface):
        surface.fill(self.bg_color)
        
        self._draw_title(surface)
        
        self._draw_level_info(surface)
        
        self._draw_difficulty_cards(surface)
        
        self._draw_navigation_buttons(surface)
    
    def _draw_title(self, surface):
        title_text = ViewRenderer.get_fonte("grande").render("Escolha a Dificuldade", True, self.white)
        title_rect = title_text.get_rect(center=(surface.get_width() // 2, 80))
        surface.blit(title_text, title_rect)
    
    def _draw_level_info(self, surface):
        if not self.screen.selected_level:
            return
        
        level_text = ViewRenderer.get_fonte("normal").render(
            f"{self.screen.selected_level.name}", 
            True, 
            (200, 200, 255)
        )
        level_rect = level_text.get_rect(center=(surface.get_width() // 2, 140))
        surface.blit(level_text, level_rect)
    
    def _draw_difficulty_cards(self, surface):
        card_width = 300
        card_height = 200
        card_spacing = 50
        
        total_width = len(self.screen.difficulties) * card_width + (len(self.screen.difficulties) - 1) * card_spacing
        start_x = (surface.get_width() - total_width) // 2
        start_y = 250
        
        self.screen.difficulty_rects.clear()
        
        for i, (difficulty, info) in enumerate(self.screen.difficulties.items()):
            card_x = start_x + i * (card_width + card_spacing)
            card_y = start_y
            
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            self.screen.difficulty_rects[difficulty] = card_rect
            
            is_selected = self.screen.selected_difficulty == difficulty
            is_hovered = self.screen.hover_difficulty == difficulty
            
            if is_selected:
                border_color = self.white
                border_width = 4
                bg_color = info["color"]
            elif is_hovered:
                border_color = info["hover_color"]
                border_width = 3
                bg_color = info["hover_color"]
            else:
                border_color = info["color"]
                border_width = 2
                bg_color = info["color"]
            
            pygame.draw.rect(surface, bg_color, card_rect)
            pygame.draw.rect(surface, border_color, card_rect, border_width)
            
            title_text = ViewRenderer.get_fonte("normal").render(info["name"], True, self.black)
            title_rect = title_text.get_rect(center=(card_x + card_width // 2, card_y + 70))
            surface.blit(title_text, title_rect)
            
            self._draw_difficulty_icon(surface, difficulty, card_x + card_width // 2, card_y + 120)
            
            if is_selected:
                check_text = ViewRenderer.get_fonte("normal").render("▀", True, self.white)
                check_rect = check_text.get_rect(center=(card_x + card_width - 30, card_y + 30))
                surface.blit(check_text, check_rect)
    
    def _draw_difficulty_icon(self, surface, difficulty, center_x, center_y):
        
        if difficulty.value == "easy":
            self._draw_simple_star(surface, center_x, center_y, 15, (255, 215, 0))
            
        elif difficulty.value == "medium":
            self._draw_simple_star(surface, center_x - 12, center_y, 12, (255, 215, 0))
            self._draw_simple_star(surface, center_x + 12, center_y, 12, (255, 215, 0))
                
        else:  # hard
            self._draw_simple_star(surface, center_x - 18, center_y, 10, (255, 215, 0))
            self._draw_simple_star(surface, center_x, center_y, 10, (255, 215, 0))
            self._draw_simple_star(surface, center_x + 18, center_y, 10, (255, 215, 0))
    
    def _draw_simple_star(self, surface, center_x, center_y, size, color):
        import math
        
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:  
                radius = size
            else:  
                radius = size * 0.4
            
            x = center_x + radius * math.cos(angle - math.pi/2)
            y = center_y + radius * math.sin(angle - math.pi/2)
            points.append((int(x), int(y)))
        
        pygame.draw.polygon(surface, color, points)
    
    def _draw_navigation_buttons(self, surface):
        back_color = self.button_hover_color if self._is_point_in_rect(pygame.mouse.get_pos(), self.screen.back_rect) else self.button_color
        pygame.draw.rect(surface, back_color, self.screen.back_rect)
        pygame.draw.rect(surface, self.white, self.screen.back_rect, 2)
        
        back_text = ViewRenderer.get_fonte("normal").render("Voltar", True, self.white)
        back_text_rect = back_text.get_rect(center=self.screen.back_rect.center)
        surface.blit(back_text, back_text_rect)
        
        play_enabled = self.screen.selected_difficulty is not None
        play_color = self.button_hover_color if play_enabled and self._is_point_in_rect(pygame.mouse.get_pos(), self.screen.play_rect) else (self.button_color if play_enabled else self.disabled_color)
        
        pygame.draw.rect(surface, play_color, self.screen.play_rect)
        pygame.draw.rect(surface, self.white if play_enabled else self.gray, self.screen.play_rect, 2)
        
        play_text = ViewRenderer.get_fonte("normal").render("Jogar", True, self.white if play_enabled else self.gray)
        play_text_rect = play_text.get_rect(center=self.screen.play_rect.center)
        surface.blit(play_text, play_text_rect)
        
        if not self.screen.selected_difficulty:
            instruction_text = ViewRenderer.get_fonte("pequena").render("Selecione uma dificuldade para continuar", True, self.gray)
            instruction_rect = instruction_text.get_rect(center=(surface.get_width() // 2, 650))
            surface.blit(instruction_text, instruction_rect)
    
    def _is_point_in_rect(self, point, rect):
        return rect.collidepoint(point)