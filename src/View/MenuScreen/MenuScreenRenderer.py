import pygame
import os
from View.UIRenderer import UIRenderer
from Core.ScreenManager import ScreenManager

class MenuScreenRenderer:
    """Renderer específico da tela de menu, cuidando de UI e eventos."""

    def __init__(self, screen):
        self.screen = screen
        self.start_rect = screen.start_rect
        self.shop_rect = screen.shop_rect
        self.credits_rect = screen.credits_rect
        self.font_titulo = screen.font_titulo
        self.font_sub = screen.font_sub
        import os
        # Carrega imagens dos botões
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Asset', 'menu', 'menu_screen')
        self.btn_jogar = pygame.image.load(os.path.join(base, 'main_screen_button3.png')).convert_alpha()
        self.btn_jogar_hover = pygame.image.load(os.path.join(base, 'main_screen_button_click1.png')).convert_alpha()
        self.btn_loja = pygame.image.load(os.path.join(base, 'main_screen_button2.png')).convert_alpha()
        self.btn_loja_hover = pygame.image.load(os.path.join(base, 'main_screen_button_click2.png')).convert_alpha()
        self.btn_creditos = pygame.image.load(os.path.join(base, 'main_screen_button1.png')).convert_alpha()
        self.btn_creditos_hover = pygame.image.load(os.path.join(base, 'main_screen_button_click3.png')).convert_alpha()


    def update(self):
        # Pode colocar animações ou seleção de botão por hover aqui
        pass

    def draw(self, surface, hover_states):
        # Fundo com imagem cortada
        menu_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Asset', 'menu', 'menu_screen', 'main_screen.png')
        menu_img_path = os.path.normpath(menu_img_path)
        menu_img = pygame.image.load(menu_img_path).convert_alpha()
        area = pygame.Rect(0, 0, surface.get_width(), surface.get_height())
        surface.blit(menu_img, (0, 0), area)

        # Botões com hover
        btns = [
            (self.start_rect, self.btn_jogar, self.btn_jogar_hover, hover_states[0]),
            (self.shop_rect, self.btn_loja, self.btn_loja_hover, hover_states[1]),
            (self.credits_rect, self.btn_creditos, self.btn_creditos_hover, hover_states[2])
        ]
        gap = 20  # pixels entre botões
        margin_bottom = 200
        total_height = sum(btn_img.get_height() for _, btn_img, _, _ in btns) + gap * (len(btns) - 1)
        start_y = surface.get_height() - total_height - margin_bottom
        y = start_y

        for idx, (rect, img, img_hover, hovered) in enumerate(btns):
            btn_img = img_hover if hovered else img
            x = (surface.get_width() - btn_img.get_width()) // 2
            btn_rect = pygame.Rect(x, y, btn_img.get_width(), btn_img.get_height())
            # Atualiza o rect para hover correto
            rect.left = x
            rect.top = y
            rect.width = btn_img.get_width()
            rect.height = btn_img.get_height()
            surface.blit(btn_img, (x, y))
            y += btn_img.get_height() + gap
