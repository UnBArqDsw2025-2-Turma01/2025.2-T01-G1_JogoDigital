import pygame
from Template.BaseScreen import BaseScreen
from Core.ScreenManager import ScreenManager
from View.Modal.ConfigModal import ConfigModal
from View.MenuScreen.MenuScreenRenderer import MenuScreenRenderer

class MenuScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.font_titulo = pygame.font.Font(None, 100)
        self.font_sub = pygame.font.Font(None, 50)
        self.start_rect = pygame.Rect(340, 400, 220, 60)  # JOGAR
        self.shop_rect = pygame.Rect(340, 480, 220, 60)   # LOJA
        self.credits_rect = pygame.Rect(340, 560, 220, 60) # CREDITOS
        self.config_rect = pygame.Rect(700, 20, 20, 20)  # CONFIGURAÇÕES
        self.hover_states = [False, False, False, False] # JOGAR, LOJA, CREDITOS
        self.renderer = MenuScreenRenderer(self)
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from View.ViewRenderer import ViewRenderer
                ViewRenderer.transition_to("jogo")
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            self.hover_states[0] = self.start_rect.collidepoint(x, y)
            self.hover_states[1] = self.shop_rect.collidepoint(x, y)
            self.hover_states[2] = self.credits_rect.collidepoint(x,y)
            self.hover_states[3] = self.config_rect.collidepoint(x,y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.start_rect.collidepoint(x, y):
                from View.ViewRenderer import ViewRenderer
                ViewRenderer.transition_to("jogo")
            elif self.shop_rect.collidepoint(x, y):
                print("Abrir loja")
            elif self.credits_rect.collidepoint(x, y):
                print("Mostrar créditos")
            elif self.config_rect.collidepoint(x, y):
                from Core.ScreenManager import ScreenManager
                ScreenManager.push_modal(ConfigModal())

    def update(self):
        pass

    def draw(self, surface):
        self.renderer.draw(surface, self.hover_states)
