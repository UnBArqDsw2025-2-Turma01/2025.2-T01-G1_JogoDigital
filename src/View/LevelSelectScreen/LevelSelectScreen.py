import pygame
from Template.BaseScreen import BaseScreen
from View.LevelSelectScreen.LevelSelectScreenRenderer import LevelSelectScreenRenderer
from Model.Level import Level, LevelStatus
from View.InputHandler import InputHandler, InputType
from View.ViewRenderer import ViewRenderer  

class LevelSelectScreen(BaseScreen):
    
    def __init__(self):
        super().__init__()
        self.levels = self._criar_niveis()
        self.completed_levels = [] 
        self._atualizar_status_niveis()

        self.selected_level = None
        self.level_rects = {}

        self.font_title = ViewRenderer.get_fonte("grande")
        self.font_normal = ViewRenderer.get_fonte("normal")
        self.font_small = ViewRenderer.get_fonte("pequena")

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
        tipo = InputHandler.classificar_evento(event)

        if tipo == InputType.QUIT:
            pygame.quit()
            exit()

        elif tipo == InputType.KEYBOARD:
            self._handle_keyboard(event)

        elif tipo == InputType.MOUSE:
            self._handle_mouse(event)

    def _handle_keyboard(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            ViewRenderer.transition_to("menu")

    def _handle_mouse(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        x, y = event.pos

        if self.back_rect.collidepoint(x, y):
            ViewRenderer.transition_to("menu")

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
        print(f"Selecionando nível {level.name} para escolha de dificuldade...")
        ViewRenderer.transition_to("difficulty")

        difficulty_screen = ViewRenderer.get_current_screen()
        if difficulty_screen and hasattr(difficulty_screen, 'set_selected_level'):
            difficulty_screen.set_selected_level(level)

    def update(self):
        pass

    def draw(self, surface):
        self.renderer.draw(surface)
