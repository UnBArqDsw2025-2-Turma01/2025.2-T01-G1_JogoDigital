import pygame
from ..entity import Entity
from ..sprite_groups import sprite_manager  # importa o composite
from Asset.AssetProvider import AssetProvider
from Template.UIConfigs import ALTURA_TELA, GRID_OFFSET_Y, NUM_LINHAS, TAMANHO_QUADRADO
import random

class Guarana(Entity):
    """Sprite colecionável que cai; fica em Items para separar Model/View."""
    def __init__(self, x, y, value=1, speed=2):
        super().__init__(x, y, 40, 40, None)
        
        # Adiciona automaticamente no grupo 'guaranas' do composite
        sprite_manager.guaranas.add(self)
        
        self.value = value
        self.speed = speed

        self.linha_destino = random.randint(0, NUM_LINHAS - 1)
        self.y_destino = GRID_OFFSET_Y + (self.linha_destino * TAMANHO_QUADRADO) + (TAMANHO_QUADRADO // 2)
        self.parado = False

        img = AssetProvider.get('guarana_coin')
        if img is None:
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 200, 0), (20, 20), 16)
            pygame.draw.circle(surf, (200, 150, 0), (20, 20), 16, 2)
            self.image = surf
        else:
            try:
                self.image = pygame.transform.scale(img, (40, 40))
            except Exception:
                self.image = img
        
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if not self.parado:
            self.rect.y += self.speed
            # Para quando atingir a linha de destino
            if self.rect.centery >= self.y_destino:
                self.rect.centery = self.y_destino
                self.parado = True

    def collect(self):
        """Coleta o guaraná (placeholder para efeitos sonoros/visuais)."""
        self.kill()
