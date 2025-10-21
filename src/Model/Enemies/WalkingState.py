import pygame

class WalkingState:
    """Estado onde o inimigo está andando normalmente."""
    
    def enter(self, enemy) -> None:
        """Configurações ao entrar no estado de andar."""
        enemy.is_attacking = False
        
        # Garante que começa com o primeiro frame da animação de walking
        if hasattr(enemy, 'walk_animation') and enemy.walk_animation:
            enemy.current_frame = 0
            enemy.image = enemy.walk_animation[0]
        
        print(f"[{enemy.__class__.__name__}] Entrando em WalkingState")
    
    def exit(self, enemy) -> None:
        """Limpeza ao sair do estado de andar."""
        pass
    
    def update(self, enemy) -> None:
        """Movimento horizontal enquanto andando."""
        enemy.rect.x -= enemy.speed
        
        # Atualiza animação se disponível
        if hasattr(enemy, 'walk_animation') and enemy.walk_animation:
            enemy.current_frame = (enemy.current_frame + enemy.animation_speed) % len(enemy.walk_animation)
            enemy.image = enemy.walk_animation[int(enemy.current_frame)]
        
        # PhysicsEngine define is_attacking, aqui apenas reagimos
        if enemy.is_attacking:
            from Model.Enemies.AttackingState import AttackingState
            enemy.set_state(AttackingState())
            print(f"[{enemy.__class__.__name__}] PhysicsEngine detectou colisão, mudando para AttackingState")