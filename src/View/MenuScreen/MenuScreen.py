import pygame
from Template.BaseScreen import BaseScreen
from Core.ScreenManager import ScreenManager

class MenuScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.font_titulo = pygame.font.Font(None, 100)
        self.font_sub = pygame.font.Font(None, 50)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                ScreenManager.set_tela("jogo")
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


    def update(self):
        pass  # pode colocar animações do menu aqui depois

    def draw(self, surface):
        surface.fill((20, 20, 60))
        titulo = self.font_titulo.render("MEU JOGO", True, (255, 255, 255))
        sub = self.font_sub.render("Pressione ENTER para começar", True, (200, 200, 200))
        
        surface.blit(titulo, (surface.get_width()//2 - titulo.get_width()//2, 200))
        surface.blit(sub, (surface.get_width()//2 - sub.get_width()//2, 350))
