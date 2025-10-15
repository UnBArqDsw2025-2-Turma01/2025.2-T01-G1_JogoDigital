from ..entity import Entity
from ..sprite_groups import projeteis_grupo
from Asset.AssetProvider import AssetProvider
from Template.UIConfigs import LARGURA_TELA

class Arrow(Entity):
    def __init__(self, x, y, linha_y):
        super().__init__(x, y, 40, 10, None)
        
        self.remove(self.groups())
        projeteis_grupo.add(self)
        
        self.image = AssetProvider.get('caipora_projectile')
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 8 
        self.linha_y = linha_y
        self.damage = 30

    def update(self):
        self.rect.x += self.velocidade
        # Remove a flecha se ela passar da borda da tela
        if self.rect.x > LARGURA_TELA:
            self.kill()