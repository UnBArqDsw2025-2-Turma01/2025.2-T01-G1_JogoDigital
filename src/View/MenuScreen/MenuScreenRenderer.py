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
        self.config_rect = screen.config_rect
        self.font_titulo = screen.font_titulo
        self.font_sub = screen.font_sub
        
        self.btn_jogar = AssetProvider.get('menu_btn_jogar')
        self.btn_jogar_hover = AssetProvider.get('menu_btn_jogar_hover')
        self.btn_loja = AssetProvider.get('menu_btn_loja')
        self.btn_loja_hover = AssetProvider.get('menu_btn_loja_hover')
        self.btn_creditos = AssetProvider.get('menu_btn_creditos')
        self.btn_creditos_hover = AssetProvider.get('menu_btn_creditos_hover')
        self.menu_img = AssetProvider.get('menu_principal')
        self.btn_config = AssetProvider.get('menu_btn_config')
        self.btn_config_hover = AssetProvider.get('menu_btn_config_hover')



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
            (self.credits_rect, self.btn_creditos, self.btn_creditos_hover, hover_states[2]),
            (self.config_rect, self.btn_config, self.btn_config_hover, hover_states[3]),
        ]

        primary_btns = btns[:-1]
        config_btn = btns[-1]

        gap = 20
        margin_bottom = 230

        total_height_primary = sum(b[1].get_height() for b in primary_btns) + gap * (len(primary_btns) - 1)
        start_y = surface.get_height() - total_height_primary - margin_bottom
        y = start_y
        center_x = surface.get_width() // 2

        for rect, img, img_hover, hovered in primary_btns:
            btn_img = img_hover if hovered else img
            x = center_x - btn_img.get_width() // 2
            rect.left = x
            rect.top = y
            rect.width = btn_img.get_width()
            rect.height = btn_img.get_height()
            surface.blit(btn_img, (x, y))
            y += btn_img.get_height() + gap

        extra_between_config = 0
        cfg_rect, cfg_img, cfg_img_hover, cfg_hovered = config_btn
        cfg_img_to_draw = cfg_img_hover if cfg_hovered else cfg_img

        y_config = y + extra_between_config - gap  
        x_config = center_x - cfg_img_to_draw.get_width() // 2

        cfg_rect.left = x_config
        cfg_rect.top = y_config
        cfg_rect.width = cfg_img_to_draw.get_width()
        cfg_rect.height = cfg_img_to_draw.get_height()

        surface.blit(cfg_img_to_draw, (x_config, y_config))