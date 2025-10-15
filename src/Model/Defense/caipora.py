from .defense import Defense
from ..Items.arrow import Arrow
from ..sprite_groups import caiporas_grupo, inimigos_grupo, get_posicao_tela
from Asset.AssetProvider import AssetProvider
import pygame

class Caipora(Defense):
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(grid_x, grid_y)
        
        super().__init__(self.pos_x, self.pos_y, 80, 80, None, 10)
        
        self.remove(self.groups())
        caiporas_grupo.add(self)
        
        self.frames = AssetProvider.get('caipora_attack')
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.animation_timer = 0
        self.frame_duration = 25 
        self.atacando = False
        self.alvo_na_linha = False
        self.FRAME_DE_TIRO = len(self.frames) - 1
        self.health = 200

    def update(self):
        self.alvo_na_linha = any(e for e in inimigos_grupo if e.grid_y == self.grid_y and e.rect.right > self.rect.right)
        
        if self.alvo_na_linha:
            self.atacando = True
        else:
            self.atacando = False
            self.frame_index = 0
            self.image = self.frames[self.frame_index]

        if self.atacando:
            self.animation_timer += 1
            if self.animation_timer >= self.frame_duration:
                if self.frame_index == self.FRAME_DE_TIRO:
                    self.atirar()
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
                self.animation_timer = 0
            
    def atirar(self):
        Arrow(self.rect.centerx, self.rect.centery, self.grid_y)