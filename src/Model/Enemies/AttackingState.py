"""
Estado de ataque para inimigos.
Responsável por executar ataques contra defesas.
"""
import pygame

class AttackingState:
    """Estado onde o inimigo está atacando uma defesa."""
    
    def __init__(self):
        self.attack_cooldown = 1000  # ms entre ataques
        self.last_attack_time = 0
        self.attack_frame_index = 0  # Índice para alternar entre sprites de ataque
        self.attack_animation_timer = 0
        self.attack_frame_duration = 10  # Frames para cada sprite de ataque
    
    def enter(self, enemy) -> None:
        """Configurações ao entrar no estado de ataque."""
        enemy.is_attacking = True
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_frame_index = 0
        self.attack_animation_timer = 0
        
        # Carrega sprites de ataque do AssetProvider se ainda não tiver
        if not hasattr(enemy, 'attack_animation') or enemy.attack_animation is None:
            from Asset.AssetProvider import AssetProvider
            enemy.attack_animation = AssetProvider.get('bp_attack')
        
        # Define imagem inicial do ataque
        if enemy.attack_animation and len(enemy.attack_animation) > 0:
            enemy.image = enemy.attack_animation[0]
        
        print(f"[{enemy.__class__.__name__}] Entrando em AttackingState")
    
    def exit(self, enemy) -> None:
        """Limpeza ao sair do estado de ataque."""
        enemy.is_attacking = False
        
        # Restaura o primeiro frame da animação de walking
        if hasattr(enemy, 'walk_animation') and enemy.walk_animation:
            enemy.current_frame = 0  # Reseta para o primeiro frame
            enemy.image = enemy.walk_animation[0]
        
        print(f"[{enemy.__class__.__name__}] Saindo de AttackingState, restaurando walking frame 0")
    
    def update(self, enemy) -> None:
        """Lógica de ataque - PhysicsEngine já chamou enemy.attack()."""
        
        # Atualiza animação de ataque alternando entre os sprites disponíveis
        if hasattr(enemy, 'attack_animation') and enemy.attack_animation and len(enemy.attack_animation) > 0:
            self.attack_animation_timer += 1
            
            if self.attack_animation_timer >= self.attack_frame_duration:
                # Alterna entre os sprites de ataque
                self.attack_frame_index = (self.attack_frame_index + 1) % len(enemy.attack_animation)
                enemy.image = enemy.attack_animation[self.attack_frame_index]
                self.attack_animation_timer = 0
        
        # PhysicsEngine define is_attacking=False quando não há mais colisão
        if not enemy.is_attacking:
            from Model.Enemies.WalkingState import WalkingState
            print(f"[{enemy.__class__.__name__}] PhysicsEngine não detectou mais colisão, voltando para WalkingState")
            enemy.set_state(WalkingState())