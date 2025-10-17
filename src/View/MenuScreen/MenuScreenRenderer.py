import pygame
from View.UIRenderer import UIRenderer
from Core.ScreenManager import ScreenManager
from Asset.AssetProvider import AssetProvider

class MenuScreenRenderer:
    """Renderer específico da tela de menu, cuidando de UI e eventos."""

    def __init__(self, screen):
        self.screen = screen
        self.start_rect = screen.start_rect
        self.shop_rect = screen.shop_rect
        self.credits_rect = screen.credits_rect
        self.font_titulo = screen.font_titulo
        self.font_sub = screen.font_sub
        
        self.btn_jogar = AssetProvider.get('menu_btn_jogar')
        self.btn_jogar_hover = AssetProvider.get('menu_btn_jogar_hover')
        self.btn_loja = AssetProvider.get('menu_btn_loja')
        self.btn_loja_hover = AssetProvider.get('menu_btn_loja_hover')
        self.btn_creditos = AssetProvider.get('menu_btn_creditos')
        self.btn_creditos_hover = AssetProvider.get('menu_btn_creditos_hover')
        self.menu_img = AssetProvider.get('menu_principal')


    def update(self):
        # Pode colocar animações ou seleção de botão por hover aqui
        pass

    def draw(self, surface, hover_states):
        area = pygame.Rect(0, 0, surface.get_width(), surface.get_height())
        surface.blit(self.menu_img, (0, 0), area)

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
