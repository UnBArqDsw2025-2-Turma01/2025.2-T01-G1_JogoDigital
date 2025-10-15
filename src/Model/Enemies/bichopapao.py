from .enemy import Enemy
from ..sprite_groups import inimigos_grupo, get_posicao_tela
from Asset.AssetProvider import AssetProvider
from Template.UIConfigs import *

class BichoPapao(Enemy):
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(self.grid_x, self.grid_y)
        
        super().__init__(self.pos_x, self.pos_y, TAMANHO_BP, TAMANHO_BP, None)
        
        self.remove(self.groups())
        inimigos_grupo.add(self)
        
        self.frames = AssetProvider.get('bp_walk')
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.animation_timer = 0 
        self.frame_duration = 10 
        
        OFFSET_CENTER = (TAMANHO_QUADRADO - TAMANHO_BP) // 2 
        self.rect = self.image.get_rect(topleft=(self.pos_x + OFFSET_CENTER, self.pos_y + OFFSET_CENTER))
        
        self.vida = 2 
        self.velocidade = 0.5

    def update(self):
        self.rect.x -= self.velocidade
        self.grid_x = max(0, (self.rect.x - GRID_OFFSET_X) // TAMANHO_QUADRADO)
        
        self.animation_timer += 1
        if self.animation_timer >= self.frame_duration: 
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0
            
        if self.vida <= 0:
            self.kill()