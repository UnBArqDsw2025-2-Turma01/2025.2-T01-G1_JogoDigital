import pygame
from Template.Modal import Modal
from Core.ScreenManager import ScreenManager
# Importa o novo renderer
from View.Modal.PauseModalRenderer import PauseModalRenderer 

class PauseModal(Modal):
    def __init__(self):
        super().__init__(blocks_update=True) 

        
        # Volumes (lidos do ScreenManager)
        self.music_volume = getattr(ScreenManager, 'MUSIC_VOLUME', 1.0)
        self.music_muted = not getattr(ScreenManager, 'MUSIC_ON', True)
        self.sfx_volume = getattr(ScreenManager, 'SFX_VOLUME', 1.0)
        self.sfx_muted = not getattr(ScreenManager, 'SFX_ON', True)

        # Estados de interação
        self.hover = {} 
        self.sair_hover = False
        self.dragging_music = False
        self.dragging_sfx = False

        self.btn_rects = {} 
        self.icon_music_rect = pygame.Rect(0,0,0,0)
        self.slider_music_rect = pygame.Rect(0,0,0,0)
        self.icon_sfx_rect = pygame.Rect(0,0,0,0)
        self.slider_sfx_rect = pygame.Rect(0,0,0,0)
        self.sair_rect = pygame.Rect(0,0,0,0)
        self.renderer = PauseModalRenderer(self)


    def _volume_step_index(self, vol):
        """Calcula o "passo" de volume mais próximo (0, 0.25, 0.5, 0.75, 1.0)"""
        steps = [0.0, 0.25, 0.5, 0.75, 1.0]
        return min(range(len(steps)), key=lambda i: abs(steps[i] - vol))

    def _apply_music_volume(self, vol):
        """Aplica a lógica de volume da música e atualiza o ScreenManager"""
        vol = max(0.0, min(1.0, vol))
        idx = self._volume_step_index(vol)
        chosen = [0.0,0.25,0.5,0.75,1.0][idx]
        
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
        """Aplica a lógica de volume dos efeitos e atualiza o ScreenManager"""
        vol = max(0.0, min(1.0, vol))
        idx = self._volume_step_index(vol)
        chosen = [0.0,0.25,0.5,0.75,1.0][idx]
        
        self.sfx_volume = chosen
        self.sfx_muted = (chosen == 0.0)
        
        if ScreenManager:
            setattr(ScreenManager, 'SFX_VOLUME', self.sfx_volume)
            setattr(ScreenManager, 'SFX_ON', not self.sfx_muted)


    def handle_event(self, event):
        """
        Processa um evento de input.
        Retorna 'close' se o modal deve ser fechado.
        """
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            
            for name, rect in self.btn_rects.items():
                self.hover[name] = rect.collidepoint(x, y)
            self.sair_hover = self.sair_rect.collidepoint(x, y)
            
            if self.dragging_music:
                rel_x = x - self.slider_music_rect.x
                rel = rel_x / max(1, self.slider_music_rect.w)
                self._apply_music_volume(rel)
                return
            
            if self.dragging_sfx:
                rel_x = x - self.slider_sfx_rect.x
                rel = rel_x / max(1, self.slider_sfx_rect.w)
                self._apply_sfx_volume(rel)
                return

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            
            # Clicks nos botões (musica, efeito, tutorial)
            for name, rect in self.btn_rects.items():
                if rect.collidepoint(x, y):
                    if name == 'musica':
                        self.music_muted = not self.music_muted
                        self._apply_music_volume(0.0 if self.music_muted else 1.0)
                        return
                    if name == 'efeito':
                        self.sfx_muted = not self.sfx_muted
                        self._apply_sfx_volume(0.0 if self.sfx_muted else 1.0)
                        return
                    if name == 'tutorial':
                        print("Abrir tutorial (implementar)")
                        return

            if self.sair_rect.collidepoint(x, y):
                if ScreenManager:
                    ScreenManager.set_tela('menu') 
                return 'close'

            if self.icon_music_rect.collidepoint(x, y):
                self.music_muted = not self.music_muted
                self._apply_music_volume(0.0 if self.music_muted else 1.0)
                return
            
            if self.icon_sfx_rect.collidepoint(x, y):
                self.sfx_muted = not self.sfx_muted
                self._apply_sfx_volume(0.0 if self.sfx_muted else 1.0)
                return

            if self.slider_music_rect.collidepoint(x, y):
                self.dragging_music = True
                rel_x = x - self.slider_music_rect.x
                rel = rel_x / max(1, self.slider_music_rect.w)
                self._apply_music_volume(rel)
                return
            
            if self.slider_sfx_rect.collidepoint(x, y):
                self.dragging_sfx = True
                rel_x = x - self.slider_sfx_rect.x
                rel = rel_x / max(1, self.slider_sfx_rect.w)
                self._apply_sfx_volume(rel)
                return

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_music or self.dragging_sfx:
                self.dragging_music = False
                self.dragging_sfx = False
                return

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return 'close'
        return None

    def update(self):
        """ 
        Atualiza a lógica do modal.
        Este modal é totalmente orientado a eventos, então nada é feito aqui.
        """
        pass

    def draw(self, surface):
        """ Delega o desenho ao renderer. """
        self.renderer.draw(surface)