# models/bicho_papao.py
from ..Enemies.enemy import Enemy
from .EnemyPrototype import IEnemyPrototype
import pygame
import copy
from Asset.AssetProvider import AssetProvider
from Model.sprite_groups import sprite_manager, get_posicao_tela

class BichoPapao(Enemy):
    def __init__(self, grid_x, grid_y):
        # Converte coordenadas do grid para posição na tela
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(grid_x, grid_y)
        
        # Inicializa a entidade sem imagem, pois vamos usar uma animação
        super().__init__(self.pos_x, self.pos_y, 70, 100, image_path=None)
        
        # Carrega as animações e configura o estado inicial
        self.walk_animation = AssetProvider.get('bp_walk')
        self.attack_animation = AssetProvider.get('bp_attack')
        self.current_frame = 0
        self.image = self.walk_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.animation_speed = 0.1  # Velocidade da animação

        # Adiciona a instância ao grupo de inimigos
        sprite_manager.inimigos.add(self)

        # Atributos de combate e habilidade
        self.health = 400
        self.speed = 6
        self.damage = 30
        
        self.scare_range = 100
        self.scare_duration = 3000 
        self.scare_cooldown = 8000 
        self.last_scare_time = -self.scare_cooldown 
    
    def update(self):
        """
        Atualização delegada para o estado atual.
        O State Pattern cuida da animação e movimento.
        """
        super().update()

    def attack(self, defense):
        """
        Ataque especializado do Bicho-Papão.
        Prioriza habilidade de susto, depois ataque padrão.
        """
        now = pygame.time.get_ticks()
        
        # Verifica se pode usar a habilidade de susto
        if now - self.last_scare_time > self.scare_cooldown:
            scare_area = self.rect.copy()
            scare_area.x -= self.scare_range
            
            if scare_area.colliderect(defense.rect):
                self._scare_defense(defense)
                self.last_scare_time = now
                return
        
        # Ataque padrão: aplica dano à defesa
        defense.health -= self.damage * 0.1
    
    def _scare_defense(self, defense):
        """Assusta uma defesa se ela tiver o método get_scared."""
        if hasattr(defense, 'get_scared'):
            defense.get_scared(self.scare_duration)
            print(f"[BichoPapao] Assustou {defense.__class__.__name__}!")

class BichoPapaoPrototype(IEnemyPrototype):
    
    def clone(self, grid_x: int, grid_y: int, **kwargs):
        health = kwargs.get('health', 400)
        speed = kwargs.get('speed', 6)
        damage = kwargs.get('damage', 30)
        
        new_enemy = BichoPapao(grid_x, grid_y)
        
        new_enemy.health = health
        new_enemy.speed = speed
        new_enemy.damage = damage
        
        return new_enemy