import pygame
from Template.BaseScreen import BaseScreen
from Core.ScreenManager import ScreenManager
from View.LevelSelectScreen.LevelSelectScreenRenderer import LevelSelectScreenRenderer
from Model.Level import Level, LevelStatus

class LevelSelectScreen(BaseScreen):
    
    def __init__(self):
        super().__init__()
        
        self.levels = self._criar_niveis()
        
        # -------------TROCAR POR JSON DEPOIS ----------------------
        self.completed_levels = []  
        
        self._atualizar_status_niveis()
        
        self.selected_level = None
        
        self.level_rects = {}
        
        self.font_title = pygame.font.Font(None, 80)
        self.font_normal = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        
        self.back_rect = pygame.Rect(50, 700, 150, 50)
        self.play_rect = pygame.Rect(1000, 700, 150, 50)
        
        self.renderer = LevelSelectScreenRenderer(self)
    
    def _criar_niveis(self):
        return [
            Level("level_1", "Nível 1 - Floresta", prerequisites=[]),
            Level("level_2", "Nível 2 - Rio", prerequisites=["level_1"]),
            Level("level_3", "Nível 3 - Montanha", prerequisites=["level_2"]),
            Level("level_4", "Nível 4 - Deserto", prerequisites=["level_3"]),
            Level("level_5", "Nível 5 - Cidade", prerequisites=["level_4"]),
        ]
    
    def _atualizar_status_niveis(self):
        for level in self.levels:
            level.unlock(self.completed_levels)
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ScreenManager.set_tela("menu")
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            if self.back_rect.collidepoint(x, y):
                ScreenManager.set_tela("menu")
            
            elif self.play_rect.collidepoint(x, y) and self.selected_level:
                self._iniciar_nivel(self.selected_level)
            
            else:
                for level_id, rect in self.level_rects.items():
                    if rect.collidepoint(x, y):
                        level = next((lv for lv in self.levels if lv.level_id == level_id), None)
                        if level and level.status != LevelStatus.LOCKED:
                            self.selected_level = level
                            print(f"Nível selecionado: {level.name}")
                        break
    
    def _iniciar_nivel(self, level):
        print(f"Iniciando {level.name}...")
        game_screen = ScreenManager._telas.get("jogo")
        if game_screen:
            game_screen.current_level = level
            game_screen.reiniciar_jogo()
        ScreenManager.set_tela("jogo")
    
    def update(self):
        pass
    
    def draw(self, surface):
        self.renderer.draw(surface)
