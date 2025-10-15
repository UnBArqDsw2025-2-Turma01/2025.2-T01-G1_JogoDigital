from ..entity import Entity

# Classe base dos Heróis
class Defense(Entity):
    def __init__(self, x, y, width, height, image_path, deploy_cost):
        super().__init__(x, y, width, height, image_path)
        self.deploy_cost = deploy_cost

    # Cada Herói tem uma lógica de atualização específica