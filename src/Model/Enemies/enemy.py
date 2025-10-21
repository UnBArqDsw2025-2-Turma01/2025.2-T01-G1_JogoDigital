from ..entity import Entity
from Model.Enemies.WalkingState import WalkingState
from typing import Optional

# Classe base dos Caçadores usando State Pattern
class Enemy(Entity):
    """
    Classe base para inimigos usando State Design Pattern.
    
    Responsabilidades:
    - Gerenciar transições de estado (Walking, Attacking, Scared)
    - Delegar comportamento para o estado atual
    - Manter atributos compartilhados entre estados
    """
    
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)
        
        # Atributos compartilhados
        self.speed = 1
        self.damage = 10
        self.is_attacking = False
        
        # State Pattern - começa no estado de Walking
        self._current_state = None
        self.set_state(WalkingState())
    
    def set_state(self, new_state) -> None:
        """
        Muda o estado atual do inimigo.
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
    
    def handle_collision(self, other):
        """Delega tratamento de colisão para o estado atual."""
        if self._current_state:
            self._current_state.handle_collision(self, other)
    
    def get_scared(self, duration: int = 3000):
        """
        Método removido - inimigos não ficam assustados.
        O ScaredState é para defesas que são assustadas pelo Bicho-Papão.
        """
        pass
    
    def attack(self, defense):
        """
        Método de ataque padrão.
        Subclasses podem sobrescrever para comportamentos específicos.
        """
        defense.health -= self.damage * 0.1