import pygame
from Template.Modal import Modal
from Asset.AssetProvider import AssetProvider
from Core.ScreenManager import ScreenManager

class PauseModal(Modal):
    def __init__(self):
        super().__init__(blocks_update=True)

        # Fundo do menu pausa
        self.menu_img = AssetProvider.get('menu_pausa')

        # escala segura (usa smoothscale se necessário)
        def _scale_img(img, factor):
            if not img:
                return None
            try:
                w = max(1, int(img.get_width() * factor))
                h = max(1, int(img.get_height() * factor))
                return pygame.transform.smoothscale(img, (w, h))
            except Exception:
                return img

        scale_factor = 0.8

        # Botões
        def _get_pair(key_normal, key_hover, factor=scale_factor):
            n = AssetProvider.get(key_normal)
            h = AssetProvider.get(key_hover)
            n = _scale_img(n, factor) if n else pygame.Surface((int(200*factor), int(60*factor)), pygame.SRCALPHA)
            h = _scale_img(h, factor) if h else n
            return {'normal': n, 'hover': h}

        # botões música, efeito, tutorial
        self.btns = {
            'musica': _get_pair('btn_musica', 'btn_musica_hover', factor=0.75),
            'efeito': _get_pair('btn_efeito', 'btn_efeito_hover', factor=0.85),
            'tutorial': _get_pair('btn_tutorial', 'btn_tutorial_hover', factor=0.75),
        }

        # botão "Sair da Partida"
        self.sair_btn = _get_pair('btn_sair', 'btn_sair_hover', factor=1.30)

        # Icons e barras
        self.icon_on = AssetProvider.get('icon_som') or AssetProvider.get('icon_som_normal')
        self.icon_off = AssetProvider.get('icon_mute') or AssetProvider.get('icon_som_mute')

        self.bar_keys = [
            ('barra_volume_mute', 'barra_volume_mute_houver'),
            ('barra_volume_25', 'barra_volume_25_houver'),
            ('barra_volume_50', 'barra_volume_50_houver'),
            ('barra_volume_75', 'barra_volume_75_houver'),
            ('barra_volume_100', 'barra_volume_100_houver'),
        ]

        self.hover = {k: False for k in self.btns.keys()}
        self.sair_hover = False
        self.rects = {}

        # Volume inicial (tenta pegar do ScreenManager)
        self.music_volume = getattr(ScreenManager, 'MUSIC_VOLUME', 1.0)
        self.music_muted = not getattr(ScreenManager, 'MUSIC_ON', True)

        self.sfx_volume = getattr(ScreenManager, 'SFX_VOLUME', 1.0)
        self.sfx_muted = not getattr(ScreenManager, 'SFX_ON', True)

        # slider/icon rects serão definidos no draw (dependem de posição do menu)
        self.icon_music_rect = pygame.Rect(0,0,0,0)
        self.slider_music_rect = pygame.Rect(0,0,0,0)
        self.icon_sfx_rect = pygame.Rect(0,0,0,0)
        self.slider_sfx_rect = pygame.Rect(0,0,0,0)

        self.dragging_music = False
        self.dragging_sfx = False

    def _volume_step_index(self, vol):
        steps = [0.0, 0.25, 0.5, 0.75, 1.0]
        idx = min(range(len(steps)), key=lambda i: abs(steps[i] - vol))
        return idx

    def _apply_music_volume(self, vol):
        vol = max(0.0, min(1.0, vol))
        idx = self._volume_step_index(vol)
        steps = [0.0, 0.25, 0.5, 0.75, 1.0]
        chosen = steps[idx]
        self.music_volume = chosen
        self.music_muted = (chosen == 0.0)
        if ScreenManager:
            setattr(ScreenManager, 'MUSIC_VOLUME', self.music_volume)
            setattr(ScreenManager, 'MUSIC_ON', not self.music_muted)
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception:
            pass

    def _apply_sfx_volume(self, vol):
        vol = max(0.0, min(1.0, vol))
        idx = self._volume_step_index(vol)
        steps = [0.0, 0.25, 0.5, 0.75, 1.0]
        chosen = steps[idx]
        self.sfx_volume = chosen
        self.sfx_muted = (chosen == 0.0)
        if ScreenManager:
            setattr(ScreenManager, 'SFX_VOLUME', self.sfx_volume)
            setattr(ScreenManager, 'SFX_ON', not self.sfx_muted)
        # deve ler ScreenManager.SFX_VOLUME ao tocar efeitos.

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            for name, rect in self.rects.items():
                self.hover[name] = rect.collidepoint(x, y)
            self.sair_hover = getattr(self, 'sair_rect', pygame.Rect(0,0,0,0)).collidepoint(x, y)
            if self.dragging_music:
                rel_x = x - self.slider_music_rect.x
                rel = rel_x / max(1, self.slider_music_rect.w)
                self._apply_music_volume(rel)
                return True
            if self.dragging_sfx:
                rel_x = x - self.slider_sfx_rect.x
                rel = rel_x / max(1, self.slider_sfx_rect.w)
                self._apply_sfx_volume(rel)
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            # clique nos botões menores
            for name, rect in self.rects.items():
                if rect.collidepoint(x, y):
                    if name == 'musica':
                        # alterna mute/restore
                        self.music_muted = not self.music_muted
                        if self.music_muted:
                            self._apply_music_volume(0.0)
                        else:
                            self._apply_music_volume(1.0)
                        return True
                    if name == 'efeito':
                        # alterna mute/restore para SFX
                        self.sfx_muted = not self.sfx_muted
                        if self.sfx_muted:
                            self._apply_sfx_volume(0.0)
                        else:
                            self._apply_sfx_volume(1.0)
                        return True
                    if name == 'tutorial':
                        print("Abrir tutorial (implementar)")
                        return True

            # clique no botão sair
            if getattr(self, 'sair_rect', pygame.Rect(0,0,0,0)).collidepoint(x, y):
                try:
                    ScreenManager.pop_modal()
                except Exception:
                    pass
                if ScreenManager:
                    # tenta várias APIs possíveis
                    for method in ('set_tela','set_screen','change_screen','change','goto','go_to','set_screen'):
                        if hasattr(ScreenManager, method):
                            try:
                                getattr(ScreenManager, method)('menu')
                            except Exception:
                                pass
                            break
                return True

            # clique nos ícones
            if self.icon_music_rect.collidepoint(x, y):
                self.music_muted = not self.music_muted
                if self.music_muted:
                    self._apply_music_volume(0.0)
                else:
                    self._apply_music_volume(1.0)
                return True
            if self.icon_sfx_rect.collidepoint(x, y):
                self.sfx_muted = not self.sfx_muted
                if self.sfx_muted:
                    self._apply_sfx_volume(0.0)
                else:
                    self._apply_sfx_volume(1.0)
                return True

            # clique nas barras -> inicia dragging e aplica passo
            if self.slider_music_rect.collidepoint(x, y):
                self.dragging_music = True
                rel_x = x - self.slider_music_rect.x
                rel = rel_x / max(1, self.slider_music_rect.w)
                self._apply_music_volume(rel)
                return True
            if self.slider_sfx_rect.collidepoint(x, y):
                self.dragging_sfx = True
                rel_x = x - self.slider_sfx_rect.x
                rel = rel_x / max(1, self.slider_sfx_rect.w)
                self._apply_sfx_volume(rel)
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            changed = False
            if self.dragging_music:
                self.dragging_music = False
                changed = True
            if self.dragging_sfx:
                self.dragging_sfx = False
                changed = True
            if changed:
                return True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            try:
                ScreenManager.pop_modal()
            except Exception:
                pass

        return False

    def draw(self, surface):
        # Fundo escurecido
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Centraliza o menu
        if self.menu_img:
            menu_x = (surface.get_width() - self.menu_img.get_width()) // 2
            menu_y = (surface.get_height() - self.menu_img.get_height()) // 2
            surface.blit(self.menu_img, (menu_x, menu_y))
        else:
            menu_w, menu_h = surface.get_width() - 200, 380
            menu_x = 100
            menu_y = (surface.get_height() - menu_h) // 2
            pygame.draw.rect(surface, (40,40,40), (menu_x, menu_y, menu_w, menu_h))

        # Posições dos botões (musica, efeito, tutorial)
        left = menu_x + 28
        top_start = menu_y + 160
        spacing = 85

        # Desenha botões menores e atualiza rects
        for i, name in enumerate(['musica', 'efeito', 'tutorial']):
            btn_img = self.btns[name]['hover'] if self.hover.get(name, False) else self.btns[name]['normal']
            y = top_start + i * spacing
            surface.blit(btn_img, (left, y))
            self.rects[name] = btn_img.get_rect(topleft=(left, y))

        # Desenha botão "sair da partida"
        sair_img = self.sair_btn['hover'] if self.sair_hover else self.sair_btn['normal']
        sair_w, sair_h = sair_img.get_width(), sair_img.get_height()
        sair_x = menu_x + ( (self.menu_img.get_width() if self.menu_img else (surface.get_width()-200)) - sair_w ) // 2
        # coloca o botão "sair da partida" abaixo dos outros botões com espaçamento extra
        sair_y = top_start + 3 * spacing + 20
        surface.blit(sair_img, (sair_x, sair_y))
        self.sair_rect = sair_img.get_rect(topleft=(sair_x, sair_y))

        # Sliders e ícones: posicione ao lado direito de cada botão (music -> first, sfx -> second)
        btn_music_img = self.btns['musica']['normal']
        btn_efeito_img = self.btns['efeito']['normal']
        btn_w = btn_music_img.get_width()
        slider_w = 150
        slider_h = 20
        icon_w = 40

        # music icon + slider (alinha com botão musica)
        slider_x = left + btn_w + 35
        music_y = top_start
        self.icon_music_rect = pygame.Rect(slider_x, music_y, icon_w, icon_w)
        self.slider_music_rect = pygame.Rect(slider_x + icon_w + 12, music_y + (icon_w - slider_h)//2, slider_w, slider_h)

        # sfx icon + slider (alinha com botão efeito)
        sfx_y = top_start + spacing
        self.icon_sfx_rect = pygame.Rect(slider_x, sfx_y, icon_w, icon_w)
        self.slider_sfx_rect = pygame.Rect(slider_x + icon_w + 12, sfx_y + (icon_w - slider_h)//2, slider_w, slider_h)

        # desenha ícones
        icon_music = self.icon_off if self.music_muted else self.icon_on
        if icon_music:
            try:
                icon_s = pygame.transform.smoothscale(icon_music, (self.icon_music_rect.w, self.icon_music_rect.h))
            except Exception:
                icon_s = icon_music
            surface.blit(icon_s, self.icon_music_rect.topleft)

        icon_sfx = self.icon_off if self.sfx_muted else self.icon_on
        if icon_sfx:
            try:
                icon_s2 = pygame.transform.smoothscale(icon_sfx, (self.icon_sfx_rect.w, self.icon_sfx_rect.h))
            except Exception:
                icon_s2 = icon_sfx
            surface.blit(icon_s2, self.icon_sfx_rect.topleft)

        # desenha barras (music)
        mouse_pos = pygame.mouse.get_pos()
        idx_m = self._volume_step_index(self.music_volume)
        mouse_over_music = self.slider_music_rect.collidepoint(mouse_pos)
        key_normal_m, key_hover_m = self.bar_keys[idx_m]
        key_m = key_hover_m if mouse_over_music else key_normal_m
        bar_img_m = AssetProvider.get(key_m)
        if bar_img_m:
            try:
                bar_m = pygame.transform.smoothscale(bar_img_m, (self.slider_music_rect.w, self.slider_music_rect.h))
            except Exception:
                bar_m = bar_img_m
            surface.blit(bar_m, self.slider_music_rect.topleft)
        else:
            pygame.draw.rect(surface, (80,80,80), self.slider_music_rect, border_radius=4)
            fill_w = int(self.music_volume * self.slider_music_rect.w)
            pygame.draw.rect(surface, (140,180,100), (self.slider_music_rect.x, self.slider_music_rect.y, fill_w, self.slider_music_rect.h), border_radius=4)
            pygame.draw.rect(surface, (200,200,200), self.slider_music_rect, 2, border_radius=4)

        # desenha barras (sfx)
        idx_s = self._volume_step_index(self.sfx_volume)
        mouse_over_sfx = self.slider_sfx_rect.collidepoint(mouse_pos)
        key_normal_s, key_hover_s = self.bar_keys[idx_s]
        key_s = key_hover_s if mouse_over_sfx else key_normal_s
        bar_img_s = AssetProvider.get(key_s)
        if bar_img_s:
            try:
                bar_s = pygame.transform.smoothscale(bar_img_s, (self.slider_sfx_rect.w, self.slider_sfx_rect.h))
            except Exception:
                bar_s = bar_img_s
            surface.blit(bar_s, self.slider_sfx_rect.topleft)
        else:
            pygame.draw.rect(surface, (80,80,80), self.slider_sfx_rect, border_radius=4)
            fill_w = int(self.sfx_volume * self.slider_sfx_rect.w)
            pygame.draw.rect(surface, (140,180,100), (self.slider_sfx_rect.x, self.slider_sfx_rect.y, fill_w, self.slider_sfx_rect.h), border_radius=4)
            pygame.draw.rect(surface, (200,200,200), self.slider_sfx_rect, 2, border_radius=4)
