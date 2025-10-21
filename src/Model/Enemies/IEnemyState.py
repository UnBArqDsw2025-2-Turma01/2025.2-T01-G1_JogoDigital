from typing import Protocol

class IEnemyState(Protocol):
    """Interface para estados de inimigos seguindo o State Pattern."""
    
    def enter(self, enemy) -> None:
        """Método chamado ao entrar no estado."""
        ...
    
    def exit(self, enemy) -> None:
        """Método chamado ao sair do estado."""
        ...
    
    def update(self, enemy) -> None:
        """Método executado a cada frame (Update loop)."""
        ...
    
    def handle_collision(self, enemy, other) -> None:
        """Método para lidar com colisões específicas do estado."""
        ...
