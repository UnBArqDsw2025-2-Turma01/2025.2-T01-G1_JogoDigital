"""
Estado de medo para defesas.
Responsável por impedir a defesa de atacar quando assustada pelo Bicho-Papão.
"""
import pygame

class ScaredState:
    """Estado onde a defesa está assustada e não pode atacar."""
    
    def __init__(self, duration: int = 3000):
        """
        Args:
            duration: Duração do estado de medo em milissegundos
        """
        self.duration = duration
        self.start_time = 0
    
    def enter(self, defense) -> None:
        """Configurações ao entrar no estado de medo."""
        self.start_time = pygame.time.get_ticks()
        defense.atacando = False
        defense.is_scared = True
        defense.frame_index = 0
        
        # Efeito visual de medo
        if hasattr(defense, 'image') and defense.image:
            defense.image = defense.image.copy()
            # Adiciona tonalidade azul/roxa para indicar medo
            defense.image.fill((80, 80, 150), special_flags=pygame.BLEND_RGB_ADD)
        
        print(f"[{defense.__class__.__name__}] Entrando em ScaredState por {self.duration}ms")
    
    def exit(self, defense) -> None:
        """Limpeza ao sair do estado de medo."""
        defense.is_scared = False
        
        # Restaura imagem original
        if hasattr(defense, 'frames') and defense.frames:
            defense.image = defense.frames[defense.frame_index]
        
        print(f"[{defense.__class__.__name__}] Saindo de ScaredState")
    
    def update(self, defense) -> None:
        """Espera até a duração do medo acabar."""
        now = pygame.time.get_ticks()
        
        # Verifica se duração do medo acabou
        if now - self.start_time >= self.duration:
            # Verifica se há inimigos para atacar ou volta para idle
            from Model.sprite_groups import inimigos_grupo
            
            alvo_na_linha = any(
                e for e in inimigos_grupo 
                if e.grid_y == defense.grid_y and e.rect.right > defense.rect.right
            )
            
            if alvo_na_linha:
                from Model.Defense.AttackingState import AttackingState
                defense.set_state(AttackingState())
            else:
                from Model.Defense.IdleState import IdleState
                defense.set_state(IdleState())
