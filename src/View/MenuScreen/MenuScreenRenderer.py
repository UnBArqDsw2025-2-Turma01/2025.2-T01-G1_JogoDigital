import pygame
from View.UIRenderer import UIRenderer
from Core.ScreenManager import ScreenManager

class MenuScreenRenderer:
    """Renderer específico da tela de menu, cuidando de UI e eventos."""

    def __init__(self, screen):
        self.screen = screen
        self.start_rect = screen.start_rect
        self.exit_rect = screen.exit_rect
        self.font_titulo = screen.font_titulo
        self.font_sub = screen.font_sub
        self.state_vars = screen.state_vars

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from Core.ScreenManager import ScreenManager
                ScreenManager.set_tela("jogo")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.start_rect.collidepoint(x, y):
                from Core.ScreenManager import ScreenManager
                ScreenManager.set_tela("jogo")
            elif self.exit_rect.collidepoint(x, y):
                pygame.quit()
                exit()

    def update(self):
        # Pode colocar animações ou seleção de botão por hover aqui
        pass

    def draw(self, surface):
        # Fundo
        surface.fill((20, 20, 60))

        # Título
        titulo = self.font_titulo.render("MEU JOGO", True, (255, 255, 255))
        surface.blit(titulo, titulo.get_rect(center=(surface.get_width()//2, 150)))

        # Botões
        UIRenderer.desenhar_botao(surface, self.start_rect, (0, 100, 200), "START", self.font_sub)
        UIRenderer.desenhar_botao(surface, self.exit_rect, (200, 0, 0), "SAIR", self.font_sub)

        pygame.display.flip()
