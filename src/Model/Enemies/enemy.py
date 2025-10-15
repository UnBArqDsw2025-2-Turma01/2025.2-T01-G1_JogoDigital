from ..entity import Entity

# Classe base dos Caçadores
class Enemy(Entity):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        self.speed = 1
        self.damage = 10
        self.is_attacking = False

    def update(self):
        # Enquanto o Caçador não estiver atacando, ele continuará andando
        if not self.is_attacking:
            self.rect.x -= self.speed