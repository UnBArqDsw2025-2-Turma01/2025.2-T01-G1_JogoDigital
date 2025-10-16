import pygame
from ..entity import Entity
from ..sprite_groups import guaranas_grupo
from Asset.AssetProvider import AssetProvider
from Template.UIConfigs import ALTURA_TELA

class Guarana(Entity):
    """Sprite colecionável que cai; fica em Items para separar Model/View."""
    def __init__(self, x, y, value=1, speed=2):
        super().__init__(x, y, 40, 40, None)
        
        self.remove(self.groups())
        guaranas_grupo.add(self)
        
        self.value = value
        self.speed = speed

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
        self.rect.y += self.speed
        # Remove o guaraná se ele passar da borda da tela
        if self.rect.top > ALTURA_TELA:
            self.kill()

    def collect(self):
        """Coleta o guaraná (placeholder para efeitos sonoros/visuais)."""
        self.kill()
