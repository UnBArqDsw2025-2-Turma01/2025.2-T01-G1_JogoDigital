import pygame
from Template.BaseScreen import BaseScreen
from View.DifficultScreen.DifficultScreenRenderer import DifficultScreenRenderer
from View.ViewRenderer import ViewRenderer  
from View.InputHandler import InputHandler, InputType
from enum import Enum

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class DifficultScreen(BaseScreen):
    
    def __init__(self):
        super().__init__()
        
        self.difficulties = {
            Difficulty.EASY: {"name": "Fácil", "color": (100, 200, 100), "hover_color": (120, 220, 120)},
            Difficulty.MEDIUM: {"name": "Médio", "color": (200, 200, 100), "hover_color": (220, 220, 120)},
            Difficulty.HARD: {"name": "Difícil", "color": (200, 100, 100), "hover_color": (220, 120, 120)}
        }
        
        self.selected_difficulty = None
        self.selected_level = None
        self.hover_difficulty = None
        
        self.difficulty_rects = {}
        self.back_rect = pygame.Rect(50, 700, 150, 50)
        self.play_rect = pygame.Rect(1000, 700, 150, 50)
        
        self.font_title = ViewRenderer.get_fonte("grande")
        self.font_subtitle = ViewRenderer.get_fonte("normal") 
        self.font_normal = ViewRenderer.get_fonte("normal")
        self.font_small = ViewRenderer.get_fonte("pequena")
        
        self.renderer = DifficultScreenRenderer(self)
    
    def set_selected_level(self, level):
        self.selected_level = level
        print(f"Nível selecionado para escolha de dificuldade: {level.name if level else 'None'}")
    
    def handle_event(self, event):
        """Delegado principal de input, usando InputHandler."""
        tipo = InputHandler.classificar_evento(event)
        pos = InputHandler.mouse_posicao()

        if tipo == InputType.QUIT:
            pygame.quit()
            exit()
        elif tipo == InputType.KEYBOARD:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ViewRenderer.transition_to("level_select")
        elif tipo == InputType.MOUSE:
            if event.type == pygame.MOUSEMOTION:
                self.hover_difficulty = None
                for difficulty, rect in self.difficulty_rects.items():
                    if rect.collidepoint(pos):
                        self.hover_difficulty = difficulty
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_rect.collidepoint(pos):
                    ViewRenderer.transition_to("level_select")
                elif self.play_rect.collidepoint(pos) and self.selected_difficulty:
                    self._iniciar_jogo()
                else:
                    for difficulty, rect in self.difficulty_rects.items():
                        if rect.collidepoint(pos):
                            self.selected_difficulty = difficulty
                            print(f"Dificuldade selecionada: {self.difficulties[difficulty]['name']}")
                            break
        
    
    def _iniciar_jogo(self):
        if not self.selected_level or not self.selected_difficulty:
            return

        print(f"Iniciando jogo:")
        print(f"  Nível: {self.selected_level.name}")
        print(f"  Dificuldade: {self.difficulties[self.selected_difficulty]['name']}")

        ViewRenderer.transition_to("jogo")
        
        game_screen = ViewRenderer.get_current_screen()
        if game_screen and hasattr(game_screen, 'set_current_level'):
            game_screen.set_current_level(self.selected_level)
        
        # TODO: implementar lógica de dificuldade

    def update(self):
        pass
    
    def draw(self, surface):
        self.renderer.draw(surface)
