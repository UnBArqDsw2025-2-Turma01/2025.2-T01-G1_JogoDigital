import pygame

# Classe base de todos os objetos
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__()
        
        if image_path is None:
            self.image = pygame.Surface((width, height))
            self.image.fill((255, 0, 255))  
        else:
            self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100

    def update(self):
        # Cada entidade tem sua própria lógica de atualização
        pass