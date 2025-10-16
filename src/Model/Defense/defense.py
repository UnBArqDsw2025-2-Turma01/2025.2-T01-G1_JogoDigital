from ..entity import Entity

import pygame

# Classe base dos Heróis
class Defense(Entity):
    def __init__(self, x, y, width, height, image_path, deploy_cost):
        super().__init__(x, y, width, height, image_path)
        self.deploy_cost = deploy_cost
        self.is_scared = False
        self.scared_duration = 0

    def get_scared(self, duration):
        self.is_scared = True
        self.scared_duration = pygame.time.get_ticks() + duration

    # Cada Herói tem uma lógica de atualização específica