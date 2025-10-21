from ..entity import Entity
from Model.Defense.IdleState import IdleState
import pygame

# Classe base dos Heróis usando State Pattern
class Defense(Entity):
    """
    Classe base para defesas usando State Design Pattern.
    
    Responsabilidades:
    - Gerenciar transições de estado (Idle, Attacking, Scared)
    - Delegar comportamento para o estado atual
    - Manter atributos compartilhados entre estados
    """
    
    def __init__(self, x, y, width, height, image_path, deploy_cost):
        super().__init__(x, y, width, height, image_path)
        self.deploy_cost = deploy_cost
        self.is_scared = False
        self.atacando = False
        
        # State Pattern - começa no estado Idle
        self._current_state = None
        self.set_state(IdleState())
    
    def set_state(self, new_state) -> None:
        """
        Muda o estado atual da defesa.
        Chama exit() no estado anterior e enter() no novo estado.
        """
        if self._current_state is not None:
            self._current_state.exit(self)
        
        self._current_state = new_state
        self._current_state.enter(self)
    
    def get_state(self):
        """Retorna o estado atual (útil para debug)."""
        return self._current_state
    
    def update(self):
        """Delega update para o estado atual."""
        if self._current_state:
            self._current_state.update(self)
    
    def get_scared(self, duration: int = 3000):
        """
        Método chamado quando o Bicho-Papão assusta esta defesa.
        Muda para ScaredState por uma duração específica.
        """
        from Model.Defense.ScaredState import ScaredState
        self.set_state(ScaredState(duration))

    # Cada Herói tem uma lógica específica (atirar, etc.)