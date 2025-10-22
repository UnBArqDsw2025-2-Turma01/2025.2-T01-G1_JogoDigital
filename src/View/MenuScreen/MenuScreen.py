import pygame
from Template.BaseScreen import BaseScreen
from Core.ScreenManager import ScreenManager
from View.Modal.ConfigModal import ConfigModal
from View.MenuScreen.MenuScreenRenderer import MenuScreenRenderer
from View.ViewRenderer import ViewRenderer
from View.InputHandler import InputHandler, InputType

class MenuScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.font_titulo = pygame.font.Font(None, 100)
        self.font_sub = pygame.font.Font(None, 50)

        # áreas clicáveis
        self.start_rect = pygame.Rect(340, 400, 220, 60)   # JOGAR
        self.shop_rect = pygame.Rect(340, 480, 220, 60)    # LOJA
        self.credits_rect = pygame.Rect(340, 560, 220, 60) # CRÉDITOS
        self.config_rect = pygame.Rect(700, 20, 20, 20)    # CONFIGURAÇÕES

        # estados de hover
        self.hover_states = [False, False, False, False]

        # renderer dedicado
        self.renderer = MenuScreenRenderer(self)

    def handle_event(self, event):
        tipo = InputHandler.classificar_evento(event)

        if tipo == InputType.QUIT:
            pygame.quit()
            exit()

        elif tipo == InputType.KEYBOARD and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                ViewRenderer.transition_to("level_select")

        elif tipo == InputType.MOUSE:
            x, y = InputHandler.mouse_posicao()
            self.hover_states[0] = self.start_rect.collidepoint(x, y)
            self.hover_states[1] = self.shop_rect.collidepoint(x, y)
            self.hover_states[2] = self.credits_rect.collidepoint(x, y)
            self.hover_states[3] = self.config_rect.collidepoint(x, y)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_rect.collidepoint(x, y):
                    ViewRenderer.transition_to("level_select")
                elif self.shop_rect.collidepoint(x, y):
                    print("Abrir loja")
                elif self.credits_rect.collidepoint(x, y):
                    print("Mostrar créditos")
                elif self.config_rect.collidepoint(x, y):
                    ScreenManager.push_modal(ConfigModal())

    def update(self):
        """Atualização lógica da tela."""
        pass

    def draw(self, surface):
        """Renderiza a tela de menu."""
        self.renderer.draw(surface, self.hover_states)
