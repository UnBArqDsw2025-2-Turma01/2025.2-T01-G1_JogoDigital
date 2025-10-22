import pygame
from Template.Modal import Modal
from Core.ScreenManager import ScreenManager
from View.Modal.ConfigModalRenderer import ConfigModalRenderer # Importa o novo renderer

class ConfigModal(Modal):
    def __init__(self):
        super().__init__(blocks_update=True)
                
        # Volumes iniciais (lidos do ScreenManager)
        self.music_volume = getattr(ScreenManager, 'MUSIC_VOLUME', 1.0)
        self.music_muted = not getattr(ScreenManager, 'MUSIC_ON', True)
        self.sfx_volume = getattr(ScreenManager, 'SFX_VOLUME', 1.0)
        self.sfx_muted = not getattr(ScreenManager, 'SFX_ON', True)

        # Estados de interação
        self.hover = {}
        self.back_hover = False
        self.save_hover = False
        self.dragging_music = False
        self.dragging_sfx = False

        self.btn_rects = {} # Para 'musica', 'efeito', 'tutorial'
        self.icon_music_rect = pygame.Rect(0,0,0,0)
        self.slider_music_rect = pygame.Rect(0,0,0,0)
        self.icon_sfx_rect = pygame.Rect(0,0,0,0)
        self.slider_sfx_rect = pygame.Rect(0,0,0,0)
        self.back_rect = pygame.Rect(0,0,0,0)
        self.save_rect = pygame.Rect(0,0,0,0)
        self.renderer = ConfigModalRenderer(self)


    def _volume_step_index(self, vol):
        """Calcula o "passo" de volume mais próximo (0, 0.25, 0.5, 0.75, 1.0)"""
        steps = [0.0, 0.25, 0.5, 0.75, 1.0]
        return min(range(len(steps)), key=lambda i: abs(steps[i] - vol))

    def _apply_music_volume(self, vol):
        """Aplica a lógica de volume da música e atualiza o ScreenManager"""
        vol = max(0.0, min(1.0, vol))
        idx = self._volume_step_index(vol)
        chosen = [0.0, 0.25, 0.5, 0.75, 1.0][idx]
        
        self.music_volume = chosen
        self.music_muted = (chosen == 0.0)
        
        if ScreenManager:
            setattr(ScreenManager, 'MUSIC_VOLUME', self.music_volume)
            setattr(ScreenManager, 'MUSIC_ON', not self.music_muted)
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"Erro ao definir volume da música: {e}")

    def _apply_sfx_volume(self, vol):
        """Aplica a lógica de volume dos efeitos e atualiza o ScreenManager"""
        vol = max(0.0, min(1.0, vol))
        idx = self._volume_step_index(vol)
        chosen = [0.0, 0.25, 0.5, 0.75, 1.0][idx]
        
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
            
            # Atualiza estados de hover (lidos pelo renderer)
            for name, rect in self.btn_rects.items():
                self.hover[name] = rect.collidepoint(x, y)
            self.back_hover = self.back_rect.collidepoint(x, y)
            self.save_hover = self.save_rect.collidepoint(x, y)
            
            # Lógica de arrastar slider
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
            
            # Clicks nos botões principais
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

            # Clicks nos botões de ação (Voltar / Salvar)
            if self.back_rect.collidepoint(x, y):
                return 'close'
            
            if self.save_rect.collidepoint(x, y):
                print("Configurações salvas")
                return 'close'

            # Clicks nos ícones de mute
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

        # Se não consumiu o evento
        return None

    def update(self):
        """ Atualiza a lógica do modal (se necessário). """
        pass

    def draw(self, surface):
        """ Delega o desenho ao renderer. """
        self.renderer.draw(surface)