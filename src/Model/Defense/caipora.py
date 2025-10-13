from .defense import Defense
from ..Items.arrow import Arrow

import pygame

# Classe da Caipora
class Caipora(Defense):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 'Asset/characters/defense/caipora_attack1.png', 10)
        self.health = 200
        self.shoot_cooldown = 2000
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, enemies_in_lane):
        # Atira se tiver inimigos na lane
        if enemies_in_lane:
            now = pygame.time.get_ticks()
            if now - self.last_shot_time > self.shoot_cooldown:
                self.last_shot_time = now
                return self.shoot()
        return None
    
    def shoot(self):
        start_pos_x = self.rect.right
        start_pos_y = self.rect.centery - 5
        return Arrow(start_pos_x, start_pos_y)