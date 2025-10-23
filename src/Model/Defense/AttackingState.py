"""
Estado de ataque para defesas.
Responsável por executar animação de ataque e disparar projéteis.
"""
import pygame

class AttackingState:
    """Estado onde a defesa está atacando inimigos."""
    
    def enter(self, defense) -> None:
        """Configurações ao entrar no estado de ataque."""
        defense.atacando = True
        defense.animation_timer = 0
        print(f"[{defense.__class__.__name__}] Entrando em AttackingState")
    
    def exit(self, defense) -> None:
        """Limpeza ao sair do estado de ataque."""
        defense.atacando = False
        defense.frame_index = 0
        if hasattr(defense, 'frames') and defense.frames:
            defense.image = defense.frames[defense.frame_index]
    
    def update(self, defense) -> None:
        """Executa animação de ataque e dispara projétil no frame correto."""
        from Model.sprite_groups import sprite_manager
        inimigos_grupo = sprite_manager.inimigos
        
        # Verifica se ainda há inimigos na linha
        alvo_na_linha = any(
            e for e in inimigos_grupo 
            if e.grid_y == defense.grid_y and e.rect.right > defense.rect.right
        )
        
        if not alvo_na_linha:
            # Não há mais inimigos, volta para IdleState
            from Model.Defense.IdleState import IdleState
            defense.set_state(IdleState())
            return
        
        # Atualiza animação de ataque
        defense.animation_timer += 1
        if defense.animation_timer >= defense.frame_duration:
            # No frame de tiro, dispara o projétil
            if defense.frame_index == defense.FRAME_DE_TIRO:
                defense.atirar()
            
            # Avança para próximo frame
            defense.frame_index = (defense.frame_index + 1) % len(defense.frames)
            defense.image = defense.frames[defense.frame_index]
            defense.animation_timer = 0
