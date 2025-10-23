from .defense import Defense
from ..Items.arrow import Arrow
from ..sprite_groups import sprite_manager, get_posicao_tela
from Asset.AssetProvider import AssetProvider
import pygame

class Caipora(Defense):
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(grid_x, grid_y)
        
        super().__init__(self.pos_x, self.pos_y, 80, 80, None, 10)
        
        self.remove(self.groups())
        sprite_manager.caiporas.add(self)
        
        self.frames = AssetProvider.get('caipora_attack')
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.animation_timer = 0
        self.frame_duration = 25 
        self.FRAME_DE_TIRO = len(self.frames) - 1
        self.health = 200

    def update(self):
        """Atualização delegada para o estado atual (State Pattern)."""
        super().update()
            
    def atirar(self):
        """Dispara uma flecha."""
        Arrow(self.rect.centerx, self.rect.centery, self.grid_y)