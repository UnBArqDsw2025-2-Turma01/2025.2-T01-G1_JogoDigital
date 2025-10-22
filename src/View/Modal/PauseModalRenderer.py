import pygame
from Asset.AssetProvider import AssetProvider

class PauseModalRenderer:
    
    def __init__(self, modal):
        """
        Inicializa o renderer, carregando todos os assets.
        
        Args:
            modal (PauseModal): A instância da lógica do modal.
        """
        self.modal = modal
        self.scale_factor = 0.8

        
        self.menu_img = AssetProvider.get('menu_pausa')

        # Botões
        self.btns = {
            'musica': self._get_pair('btn_musica', 'btn_musica_hover', factor=0.75),
            'efeito': self._get_pair_width('btn_efeito', 'btn_efeito_hover', width_factor=0.9, height_scale=0.75),
            'tutorial': self._get_pair('btn_tutorial', 'btn_tutorial_hover', factor=0.75),
        }
        # Botão "Sair da Partida"
        self.sair_btn = self._get_pair_width('btn_sair', 'btn_sair_hover', width_factor=1.25, height_scale=0.9)

        # Icons / barras
        self.icon_on = AssetProvider.get('icon_som') or AssetProvider.get('icon_som_normal')
        self.icon_off = AssetProvider.get('icon_mute') or AssetProvider.get('icon_som_mute')

        self.bar_keys = [
            ('barra_volume_mute', 'barra_volume_mute_houver'),
            ('barra_volume_25', 'barra_volume_25_houver'),
            ('barra_volume_50', 'barra_volume_50_houver'),
            ('barra_volume_75', 'barra_volume_75_houver'),
            ('barra_volume_100', 'barra_volume_100_houver'),
        ]


    def _scale_img(self, img, factor):
        if not img:
            return None
        try:
            w = max(1, int(img.get_width() * factor))
            h = max(1, int(img.get_height() * factor))
            return pygame.transform.smoothscale(img, (w, h))
        except Exception:
            return img

    def _scale_width(self, img, width_factor, height_scale=1.0):
        if not img:
            return None
        try:
            new_w = max(1, int(img.get_width() * width_factor))
            new_h = max(1, int(img.get_height() * height_scale))
            return pygame.transform.smoothscale(img, (new_w, new_h))
        except Exception:
            return img

    def _get_pair(self, key_normal, key_hover, factor):
        n = AssetProvider.get(key_normal)
        h = AssetProvider.get(key_hover)
        n_s = self._scale_img(n, factor) if n else pygame.Surface((int(200*factor), int(60*factor)), pygame.SRCALPHA)
        h_s = self._scale_img(h, factor) if h else n_s
        return {'normal': n_s, 'hover': h_s}

    def _get_pair_width(self, key_normal, key_hover, width_factor, height_scale):
        n = AssetProvider.get(key_normal)
        h = AssetProvider.get(key_hover)
        if n:
            n_s = self._scale_width(n, width_factor, height_scale)
        else:
            n_s = pygame.Surface((int(200*width_factor), int(60*height_scale)), pygame.SRCALPHA)
        if h:
            h_s = self._scale_width(h, width_factor, height_scale)
        else:
            h_s = n_s
        return {'normal': n_s, 'hover': h_s}


    def draw(self, surface):
        """ Desenha o modal na superfície. """
        
        # 1. Fundo escurecido
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # 2. Centraliza o menu
        if self.menu_img:
            menu_x = (surface.get_width() - self.menu_img.get_width()) // 2
            menu_y = (surface.get_height() - self.menu_img.get_height()) // 2
            surface.blit(self.menu_img, (menu_x, menu_y))
            menu_w = self.menu_img.get_width()
        else:
            # Fallback se asset não carregou
            menu_w, menu_h = surface.get_width() - 200, 380
            menu_x = 100
            menu_y = (surface.get_height() - menu_h) // 2
            pygame.draw.rect(surface, (40,40,40), (menu_x, menu_y, menu_w, menu_h))

        # 3. Posições dos botões (musica, efeito, tutorial)
        left = menu_x + 28
        top_start = menu_y + 160
        spacing = 85

        # 4. Desenha botões menores e ATUALIZA rects no modal
        for i, name in enumerate(['musica', 'efeito', 'tutorial']):
            # Lê o estado de hover do modal
            is_hovered = self.modal.hover.get(name, False)
            btn_img = self.btns[name]['hover'] if is_hovered else self.btns[name]['normal']
            
            y = top_start + i * spacing
            surface.blit(btn_img, (left, y))
            
            self.modal.btn_rects[name] = btn_img.get_rect(topleft=(left, y))

        # 5. Desenha botão "sair da partida"
        # Lê o estado de hover do modal
        sair_img = self.sair_btn['hover'] if self.modal.sair_hover else self.sair_btn['normal']
        sair_w, sair_h = sair_img.get_width(), sair_img.get_height()
        sair_x = menu_x + (menu_w - sair_w) // 2
        sair_y = top_start + 3 * spacing + 20
        surface.blit(sair_img, (sair_x, sair_y))
        self.modal.sair_rect = sair_img.get_rect(topleft=(sair_x, sair_y))

        # 6. Sliders e ícones
        btn_w = self.btns['musica']['normal'].get_width()
        slider_w, slider_h, icon_w = 150, 20, 40

        # Posições de Música
        slider_x = left + btn_w + 35
        music_y = top_start
        self.modal.icon_music_rect = pygame.Rect(slider_x, music_y, icon_w, icon_w)
        self.modal.slider_music_rect = pygame.Rect(slider_x + icon_w + 12, music_y + (icon_w - slider_h)//2, slider_w, slider_h)

        # Posições de Efeitos
        sfx_y = top_start + spacing
        self.modal.icon_sfx_rect = pygame.Rect(slider_x, sfx_y, icon_w, icon_w)
        self.modal.slider_sfx_rect = pygame.Rect(slider_x + icon_w + 12, sfx_y + (icon_w - slider_h)//2, slider_w, slider_h)

        # 7. Desenha ícones (lendo estado 'muted' do modal)
        icon_music = self.icon_off if self.modal.music_muted else self.icon_on
        if icon_music:
            icon_s = pygame.transform.smoothscale(icon_music, self.modal.icon_music_rect.size)
            surface.blit(icon_s, self.modal.icon_music_rect.topleft)

        icon_sfx = self.icon_off if self.modal.sfx_muted else self.icon_on
        if icon_sfx:
            icon_s2 = pygame.transform.smoothscale(icon_sfx, self.modal.icon_sfx_rect.size)
            surface.blit(icon_s2, self.modal.icon_sfx_rect.topleft)

        # 8. Desenha barras de volume (lendo estado 'volume' do modal)
        
        # Barra de Música
        mouse_pos = pygame.mouse.get_pos()
        idx_m = self.modal._volume_step_index(self.modal.music_volume) 
        mouse_over_music = self.modal.slider_music_rect.collidepoint(mouse_pos)
        key_normal_m, key_hover_m = self.bar_keys[idx_m]
        key_m = key_hover_m if mouse_over_music else key_normal_m
        bar_img_m = AssetProvider.get(key_m)
        
        if bar_img_m:
            bar_m = pygame.transform.smoothscale(bar_img_m, self.modal.slider_music_rect.size)
            surface.blit(bar_m, self.modal.slider_music_rect.topleft)
        else:
            rect = self.modal.slider_music_rect
            pygame.draw.rect(surface, (80,80,80), rect, border_radius=4)
            fill_w = int(self.modal.music_volume * rect.w)
            pygame.draw.rect(surface, (140,180,100), (rect.x, rect.y, fill_w, rect.h), border_radius=4)
            pygame.draw.rect(surface, (200,200,200), rect, 2, border_radius=4)

        # Barra de Efeitos
        idx_s = self.modal._volume_step_index(self.modal.sfx_volume)
        mouse_over_sfx = self.modal.slider_sfx_rect.collidepoint(mouse_pos)
        key_normal_s, key_hover_s = self.bar_keys[idx_s]
        key_s = key_hover_s if mouse_over_sfx else key_normal_s
        bar_img_s = AssetProvider.get(key_s)
        
        if bar_img_s:
            bar_s = pygame.transform.smoothscale(bar_img_s, self.modal.slider_sfx_rect.size)
            surface.blit(bar_s, self.modal.slider_sfx_rect.topleft)
        else:
            rect = self.modal.slider_sfx_rect
            pygame.draw.rect(surface, (80,80,80), rect, border_radius=4)
            fill_w = int(self.modal.sfx_volume * rect.w)
            pygame.draw.rect(surface, (140,180,100), (rect.x, rect.y, fill_w, rect.h), border_radius=4)
            pygame.draw.rect(surface, (200,200,200), rect, 2, border_radius=4)