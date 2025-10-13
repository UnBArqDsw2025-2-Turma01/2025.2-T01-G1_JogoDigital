from ..entity import Entity

# Classe da flecha usada pela Caipora
class Arrow(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 10, 'image_path')
        self.speed = 10
        self.damage = 30

    def update(self):
        self.rect.c += self.speed
        # Remove a flecha se ela passar da borda da tela
        if self.rect.left > 800:
            self.kill()