"""
Interface que todos os estados de defesas devem implementar.
Define os métodos que cada estado deve ter.
"""
from typing import Protocol

class IDefenseState(Protocol):
    """Interface para estados de defesas seguindo o State Pattern."""
    
    def enter(self, defense) -> None:
        """Método chamado ao entrar no estado."""
        ...
    
    def exit(self, defense) -> None:
        """Método chamado ao sair do estado."""
        ...
    
    def update(self, defense) -> None:
        """Método executado a cada frame (Update loop)."""
        ...
