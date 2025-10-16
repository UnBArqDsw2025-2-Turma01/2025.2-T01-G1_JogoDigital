# models/bruxa.py
from ..Enemies.enemy import Enemy
import pygame
from Asset.AssetProvider import AssetProvider
from Model.sprite_groups import inimigos_grupo, get_posicao_tela

class Bruxa(Enemy):
    def __init__(self, grid_x, grid_y):
        # Converte coordenadas do grid para posição na tela
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.pos_x, self.pos_y = get_posicao_tela(grid_x, grid_y)
        
        # Inicializa a entidade sem imagem
        super().__init__(self.pos_x, self.pos_y, 70, 100, image_path=None)
        
        # Carrega sprites
        self.walk_animation = AssetProvider.get('bruxa_walk')
        self.attack_animation = AssetProvider.get('bruxa_attack')
        self.current_frame = 0
        self.image = self.walk_animation[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.animation_speed = 0.15  # Velocidade da animação
        self.is_using_attack_animation = False

        # Adiciona a instância ao grupo de inimigos
        inimigos_grupo.add(self)

        # Atributos de combate e habilidade
        self.health = 250
        self.speed = 0.7
        self.damage = 25
        
        # Atributos da habilidade especial (Envenenamento)
        self.poison_range = 100  # Distância para usar a habilidade
        self.poison_damage = 5  # Dano por tick do veneno
        self.poison_duration = 5000  # 5 segundos de envenenamento
        self.poison_cooldown = 10000  # Só pode envenenar a cada 10 segundos
        self.last_poison_time = -self.poison_cooldown
    
    def update(self):
        # Escolhe a animação apropriada
        if self.is_using_attack_animation:
            current_animation = self.attack_animation
        else:
            current_animation = self.walk_animation
        
        # Atualiza a animação
        self.current_frame = (self.current_frame + self.animation_speed) % len(current_animation)
        self.image = current_animation[int(self.current_frame)]

        # Chama a lógica de update da classe pai (movimento, etc.)
        super().update()

    def attack(self, defense):
        """Ataca a defesa, priorizando a habilidade de envenenamento se estiver disponível."""
        now = pygame.time.get_ticks()
        
        # Verifica se pode usar a habilidade de envenenamento
        if now - self.last_poison_time > self.poison_cooldown:
            poison_area = self.rect.copy()
            poison_area.x -= self.poison_range
            
            if poison_area.colliderect(defense.rect):
                self.poison(defense)
                self.last_poison_time = now
                self.is_using_attack_animation = True
                return
        
        # Ataque padrão: aplica dano à defesa
        self.is_using_attack_animation = True
        defense.health -= self.damage * 0.1
        
    def poison(self, defense):
        """Aplica o efeito de veneno na defesa alvo."""
        if hasattr(defense, 'get_poisoned'):
            defense.get_poisoned(self.poison_damage, self.poison_duration)
            print(f"Bruxa envenenou a defesa em ({defense.grid_x}, {defense.grid_y})!")
