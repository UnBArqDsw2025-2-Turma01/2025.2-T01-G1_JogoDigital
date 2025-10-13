# Model/Entities.py

import pygame
from Template.UIConfigs import *
from Asset.AssetProvider import AssetProvider

# Grupos de Sprites (Definidos globalmente ou importados, aqui definimos para simplificar)
caiporas_grupo = pygame.sprite.Group()
inimigos_grupo = pygame.sprite.Group()
projeteis_grupo = pygame.sprite.Group()

# Funções de Posição
def get_posicao_tela(col, lin):
    x = GRID_OFFSET_X + col * TAMANHO_QUADRADO
    y = GRID_OFFSET_Y + lin * TAMANHO_QUADRADO
    return x, y


class Caipora(pygame.sprite.Sprite):
    # ... (Os métodos __init__ e update são iguais, mas usando AssetProvider.get())
    def __init__(self, grid_x, grid_y):
        super().__init__(caiporas_grupo) 
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(grid_x, grid_y)
        
        self.frames = AssetProvider.get('caipora_attack')
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.animation_timer = 0
        self.frame_duration = 25 
        self.atacando = False
        self.alvo_na_linha = False
        self.FRAME_DE_TIRO = len(self.frames) - 1 

    def update(self):
        # 1. Verifica alvo
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
        Projetil(self.rect.centerx, self.rect.centery, self.grid_y) 

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, linha_y):
        super().__init__(projeteis_grupo) 
        self.image = AssetProvider.get('caipora_projectile')
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 8 
        self.linha_y = linha_y 

    def update(self):
        self.rect.x += self.velocidade
        if self.rect.x > LARGURA_TELA:
            self.kill()

class BichoPapao(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__(inimigos_grupo) 
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(self.grid_x, self.grid_y)
        
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