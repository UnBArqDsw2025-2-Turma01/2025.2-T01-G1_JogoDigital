import pygame
from Asset.AssetProvider import AssetProvider

class ConfigModalRenderer:
    
    def __init__(self, modal):
        """
        Inicializa o renderer, carregando todos os assets.
        
        Args:
            modal (ConfigModal): A instância da lógica do modal.
        """
        self.modal = modal
        self.scale_factor = 0.8
        
        # --- Carregamento de Assets ---
        
        self.menu_img = AssetProvider.get('menu_config')

        # Pares normal/hover para botões
        self.btns = {
            'musica': self._pair('btn_musica', 'btn_musica_hover', factor=0.75),
            'efeito': self._pair_width('btn_efeito', 'btn_efeito_hover', width_factor=1.0, height_scale=0.75),
            'tutorial': self._pair('btn_tutorial', 'btn_tutorial_hover', factor=0.75),
        }

        # Botões salvar/voltar
        self.back_btn = self._pair('btn_voltar', 'btn_voltar_hover', factor=0.95)
        self.save_btn = self._pair('btn_salvar', 'btn_salvar_hover', factor=0.95)

        # Ícones e assets das barras de volume
        self.icon_on = AssetProvider.get('icon_som') or AssetProvider.get('icon_som_normal')
        self.icon_off = AssetProvider.get('icon_mute') or AssetProvider.get('icon_som_mute')
        self.bar_keys = [
            ('barra_volume_mute', 'barra_volume_mute_houver'),
            ('barra_volume_25', 'barra_volume_25_houver'),
            ('barra_volume_50', 'barra_volume_50_houver'),
            ('barra_volume_75', 'barra_volume_75_houver'),
            ('barra_volume_100', 'barra_volume_100_houver'),
        ]

    # --- Métodos Auxiliares de Carregamento ---

    def _scale_img(self, img, factor):
        if not img:
            return None
        try:
            w = max(1, int(img.get_width() * factor))
            h = max(1, int(img.get_height() * factor))
            return pygame.transform.smoothscale(img, (w, h))
        except Exception:
            return img

    def _pair(self, nkey, hkey, factor):
        n = AssetProvider.get(nkey)
        h = AssetProvider.get(hkey)
        n_s = self._scale_img(n, factor) if n else pygame.Surface((int(200*factor), int(60*factor)), pygame.SRCALPHA)
        h_s = self._scale_img(h, factor) if h else n_s
        return {'normal': n_s, 'hover': h_s}

    def _pair_width(self, nkey, hkey, width_factor, height_scale):
        n = AssetProvider.get(nkey)
        h = AssetProvider.get(hkey)
        if n:
            try:
                new_w = max(1, int(n.get_width() * width_factor))
                new_h = max(1, int(n.get_height() * height_scale))
                n_s = pygame.transform.smoothscale(n, (new_w, new_h))
            except Exception:
                n_s = n
        else:
            n_s = pygame.Surface((int(200*width_factor), int(60*height_scale)), pygame.SRCALPHA)
        if h:
            try:
                h_s = pygame.transform.smoothscale(h, (n_s.get_width(), n_s.get_height()))
            except Exception:
                h_s = h
        else:
            h_s = n_s
        return {'normal': n_s, 'hover': h_s}

    # --- Método Principal de Desenho ---

    def draw(self, surface):
        """ Desenha o modal na superfície. """
        
        # 1. Overlay escuro
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # 2. Imagem de fundo do menu
        if self.menu_img:
            menu_x = (surface.get_width() - self.menu_img.get_width()) // 2
            menu_y = (surface.get_height() - self.menu_img.get_height()) // 2
            surface.blit(self.menu_img, (menu_x, menu_y))
            menu_inner_w = self.menu_img.get_width()
        else:
            # Fallback se a imagem não carregou
            menu_w, menu_h = surface.get_width() - 200, 380
            menu_x = 100
            menu_y = (surface.get_height() - menu_h) // 2
            menu_inner_w = menu_w
            pygame.draw.rect(surface, (40, 40, 40), (menu_x, menu_y, menu_w, menu_h))

        # 3. Posições base
        left = menu_x + 28
        top_start = menu_y + 160
        spacing = 85
        
        ref_btn = self.btns.get('musica', {}).get('normal')
        btn_h = ref_btn.get_height() if ref_btn else int(60 * self.scale_factor)
        total_buttons_height = 3 * btn_h + (3 - 1) * spacing

        # 4. Desenha botões (Musica, Efeito, Tutorial)
        for i, name in enumerate(['musica', 'efeito', 'tutorial']):
            # Lê o estado de hover do modal
            is_hovered = self.modal.hover.get(name, False)
            btn_img = self.btns[name]['hover'] if is_hovered else self.btns[name]['normal']
            
            y = top_start + i * spacing
            surface.blit(btn_img, (left, y))
            
            # ATUALIZA o rect no modal para detecção de clique
            self.modal.btn_rects[name] = btn_img.get_rect(topleft=(left, y))

        # 5. Posições e desenho dos Sliders e Ícones
        btn_w = self.btns['musica']['normal'].get_width()
        slider_w, slider_h, icon_w = 150, 20, 40
        slider_x = left + btn_w + 70

        # Posições de Música
        music_y = top_start
        icon_music_pos = (slider_x, music_y)
        slider_music_pos = (slider_x + icon_w + 12, music_y + (icon_w - slider_h) // 2)
        
        # Atualiza os rects no modal
        self.modal.icon_music_rect = pygame.Rect(icon_music_pos, (icon_w, icon_w))
        self.modal.slider_music_rect = pygame.Rect(slider_music_pos, (slider_w, slider_h))

        # Posições de Efeitos
        sfx_y = top_start + spacing
        icon_sfx_pos = (slider_x, sfx_y)
        slider_sfx_pos = (slider_x + icon_w + 12, sfx_y + (icon_w - slider_h) // 2)
        
        # Atualiza os rects no modal
        self.modal.icon_sfx_rect = pygame.Rect(icon_sfx_pos, (icon_w, icon_w))
        self.modal.slider_sfx_rect = pygame.Rect(slider_sfx_pos, (slider_w, slider_h))

        # Desenha ícones (lendo estado 'muted' do modal)
        icon_music_img = self.icon_off if self.modal.music_muted else self.icon_on
        if icon_music_img:
            icon_s = pygame.transform.smoothscale(icon_music_img, (icon_w, icon_w))
            surface.blit(icon_s, icon_music_pos)

        icon_sfx_img = self.icon_off if self.modal.sfx_muted else self.icon_on
        if icon_sfx_img:
            icon_s2 = pygame.transform.smoothscale(icon_sfx_img, (icon_w, icon_w))
            surface.blit(icon_s2, icon_sfx_pos)
            
        # Desenha barras de volume
        mouse_pos = pygame.mouse.get_pos()
        self._draw_volume_bar(surface, self.modal.slider_music_rect, self.modal.music_volume, mouse_pos)
        self._draw_volume_bar(surface, self.modal.slider_sfx_rect, self.modal.sfx_volume, mouse_pos)

        # 6. Desenha botões de ação (Voltar / Salvar)
        gap_actions = 16
        back_img = self.back_btn['hover'] if self.modal.back_hover else self.back_btn['normal']
        save_img = self.save_btn['hover'] if self.modal.save_hover else self.save_btn['normal']
        
        total_actions_w = back_img.get_width() + gap_actions + save_img.get_width()
        actions_x = menu_x + (menu_inner_w - total_actions_w) // 2
        actions_y = top_start + total_buttons_height + 5 # Padding

        # Posição Voltar
        back_x = actions_x
        surface.blit(back_img, (back_x, actions_y))
        # Atualiza o rect no modal
        self.modal.back_rect = back_img.get_rect(topleft=(back_x, actions_y))

        # Posição Salvar
        save_x = back_x + back_img.get_width() + gap_actions
        surface.blit(save_img, (save_x, actions_y))
        # Atualiza o rect no modal
        self.modal.save_rect = save_img.get_rect(topleft=(save_x, actions_y))

    def _draw_volume_bar(self, surface, rect, volume, mouse_pos):
        """Desenha uma barra de volume, com base em assets ou fallback."""
        
        # Lê o índice de volume do modal
        idx = self.modal._volume_step_index(volume)
        mouse_over = rect.collidepoint(mouse_pos)
        
        key_normal, key_hover = self.bar_keys[idx]
        key = key_hover if mouse_over else key_normal
        bar_img = AssetProvider.get(key)
        
        if bar_img:
            try:
                bar_scaled = pygame.transform.smoothscale(bar_img, rect.size)
            except Exception:
                bar_scaled = bar_img
            surface.blit(bar_scaled, rect.topleft)
        else:
            # Fallback se assets da barra não carregarem
            pygame.draw.rect(surface, (80, 80, 80), rect, border_radius=4)
            fill_w = int(volume * rect.w)
            fill_rect = pygame.Rect(rect.x, rect.y, fill_w, rect.h)
            pygame.draw.rect(surface, (140, 180, 100), fill_rect, border_radius=4)
            pygame.draw.rect(surface, (200, 200, 200), rect, 2, border_radius=4)