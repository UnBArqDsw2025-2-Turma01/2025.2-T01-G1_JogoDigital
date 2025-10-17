import pygame
from Template.Modal import Modal
from Asset.AssetProvider import AssetProvider
from Core.ScreenManager import ScreenManager

class PauseModal(Modal):
    def __init__(self):
        super().__init__(blocks_update=True)

        # Fundo do menu pausa
        self.menu_img = AssetProvider.get('menu_pausa')

        # Botões (normal e hover)
        scale_factor = 0.8  # 80% do tamanho original

        self.btns = {
            'musica': {
                'normal': pygame.transform.scale_by(AssetProvider.get('btn_musica'), scale_factor),
                'hover': pygame.transform.scale_by(AssetProvider.get('btn_musica_hover'), scale_factor)
            },
            'efeito': {
                'normal': pygame.transform.scale_by(AssetProvider.get('btn_efeito'), scale_factor),
                'hover': pygame.transform.scale_by(AssetProvider.get('btn_efeito_hover'), scale_factor)
            },
            'tutorial': {
                'normal': pygame.transform.scale_by(AssetProvider.get('btn_tutorial'), scale_factor),
                'hover': pygame.transform.scale_by(AssetProvider.get('btn_tutorial_hover'), scale_factor)
            }
            
        }

        # Estados
        self.hover = {'musica': False, 'efeito': False, 'tutorial': False}
        self.rects = {}

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            for name, rect in self.rects.items():
                self.hover[name] = rect.collidepoint(x, y)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for name, rect in self.rects.items():
                if rect.collidepoint(x, y):
                    print(f"Clicou no botão {name}")

    def draw(self, surface):
        # Fundo escurecido
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Centraliza o menu
        menu_x = (surface.get_width() - self.menu_img.get_width()) // 2
        menu_y = (surface.get_height() - self.menu_img.get_height()) // 2
        surface.blit(self.menu_img, (menu_x, menu_y))

        # Posições dos botões
        left = menu_x + 30
        top_start = menu_y + 170
        spacing = 70

        # Desenha botões
        for i, name in enumerate(['musica', 'efeito', 'tutorial']):
            btn_img = self.btns[name]['hover'] if self.hover[name] else self.btns[name]['normal']
            y = top_start + i * spacing
            surface.blit(btn_img, (left, y))
            self.rects[name] = btn_img.get_rect(topleft=(left, y))
