# Template/PhysicsEngine.py

import pygame
from Model.sprite_groups import sprite_manager

class PhysicsEngine:
    @classmethod
    def processar_colisoes(cls):
        """Processa colisões entre projéteis, inimigos e defesas (caiporas)."""

        # 1. Colisão de projéteis com inimigos
        colisoes_projeteis = pygame.sprite.groupcollide(
            sprite_manager.projeteis, sprite_manager.inimigos, True, False
        )

        for projetil, inimigos_atingidos in colisoes_projeteis.items():
            for inimigo in inimigos_atingidos:
                inimigo.health -= 25  # dano base
                if inimigo.health <= 0:
                    inimigo.kill()

        # 2. Colisão de inimigos com defesas (caiporas)
        for inimigo in sprite_manager.inimigos:
            defesas_na_linha = [
                d for d in sprite_manager.caiporas if d.grid_y == inimigo.grid_y
            ]
            
            for defesa in defesas_na_linha:
                if pygame.sprite.collide_rect(inimigo, defesa):
                    inimigo.is_attacking = True
                    
                    if hasattr(inimigo, 'attack'):
                        inimigo.attack(defesa)
                    else:
                        defesa.health -= inimigo.damage * 0.1
                    
                    if defesa.health <= 0:
                        defesa.kill()
                    
                    break
            else:
                inimigo.is_attacking = False
