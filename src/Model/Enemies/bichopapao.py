# models/bicho_papao.py
from ..Enemies.enemy import Enemy
import pygame
from Asset.AssetProvider import AssetProvider
from Model.sprite_groups import inimigos_grupo, get_posicao_tela

class BichoPapao(Enemy):
    def __init__(self, grid_x, grid_y):
        # Converte coordenadas do grid para posição na tela
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(grid_x, grid_y)
        
        # Inicializa a entidade sem imagem, pois vamos usar uma animação
        super().__init__(self.pos_x, self.pos_y, 70, 100, image_path=None)
        
        # Carrega a animação e configura o estado inicial
        self.walk_animation = AssetProvider.get('bp_walk')
        self.current_frame = 0
        self.image = self.walk_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.animation_speed = 0.1  # Velocidade da animação

        # Adiciona a instância ao grupo de inimigos
        inimigos_grupo.add(self)

        # Atributos de combate e habilidade
        self.health = 400
        self.speed = 1.2
        self.damage = 30
        
        self.scare_range = 100
        self.scare_duration = 3000 
        self.scare_cooldown = 8000 
        self.last_scare_time = -self.scare_cooldown 
    
    def update(self):
        # Atualiza a animação
        self.current_frame = (self.current_frame + self.animation_speed) % len(self.walk_animation)
        self.image = self.walk_animation[int(self.current_frame)]

        # Chama a lógica de update da classe pai (movimento, etc.)
        super().update()

    def attack(self, defense):
        """Ataca a defesa, priorizando a habilidade de susto se estiver disponível."""
        now = pygame.time.get_ticks()
        
        # Verifica se pode usar a habilidade de susto
        if now - self.last_scare_time > self.scare_cooldown:
            scare_area = self.rect.copy()
            scare_area.x -= self.scare_range
            
            if scare_area.colliderect(defense.rect):
                self.scare(defense)
                self.last_scare_time = now
                return
        
        # Ataque padrão: aplica dano à defesa
        defense.health -= self.damage * 0.1
        
    def scare(self, defense):
        if hasattr(defense, 'get_scared'):
            defense.get_scared(self.scare_duration)