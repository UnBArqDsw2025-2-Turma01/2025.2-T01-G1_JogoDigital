"""
Estado ocioso para defesas.
Responsável por manter a defesa esperando por inimigos.
"""
import pygame

class IdleState:
    """Estado onde a defesa está ociosa, sem alvos."""
    
    def enter(self, defense) -> None:
        """Configurações ao entrar no estado ocioso."""
        defense.atacando = False
        defense.frame_index = 0
        if hasattr(defense, 'frames') and defense.frames:
            defense.image = defense.frames[defense.frame_index]
        print(f"[{defense.__class__.__name__}] Entrando em IdleState")
    
    def exit(self, defense) -> None:
        """Limpeza ao sair do estado ocioso."""
        pass
    
    def update(self, defense) -> None:
        """Verifica se há inimigos na linha para mudar para AttackingState."""
        from Model.sprite_groups import inimigos_grupo
        
        # Verifica se há inimigo na mesma linha
        alvo_na_linha = any(
            e for e in inimigos_grupo 
            if e.grid_y == defense.grid_y and e.rect.right > defense.rect.right
        )
        
        if alvo_na_linha:
            from Model.Defense.AttackingState import AttackingState
            defense.set_state(AttackingState())
