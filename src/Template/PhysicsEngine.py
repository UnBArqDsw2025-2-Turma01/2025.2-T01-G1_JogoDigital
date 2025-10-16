# Template/PhysicsEngine.py

import pygame
from Model.sprite_groups import projeteis_grupo, inimigos_grupo, caiporas_grupo

class PhysicsEngine:
    @classmethod
    def processar_colisoes(cls):
        """Processa as colisões do jogo: projéteis vs inimigos e inimigos vs defesas."""
        
        # 1. Colisão de projéteis com inimigos
        # True (remove projetil), False (NÃO remove inimigo automaticamente)
        colisoes_projeteis = pygame.sprite.groupcollide(projeteis_grupo, inimigos_grupo, True, False)

        for projetil, inimigos_atingidos in colisoes_projeteis.items():
            for inimigo in inimigos_atingidos:
                inimigo.health -= 25  # Aplica dano ao inimigo
                
                # Remove o inimigo se a vida chegou a zero ou menos
                if inimigo.health <= 0:
                    inimigo.kill()
        
        # 2. Colisão de inimigos com defesas
        for inimigo in inimigos_grupo:
            # Verifica se há alguma defesa na mesma linha e próxima do inimigo
            defesas_na_linha = [d for d in caiporas_grupo if d.grid_y == inimigo.grid_y]
            
            for defesa in defesas_na_linha:
                # Verifica se há colisão entre o inimigo e a defesa
                if pygame.sprite.collide_rect(inimigo, defesa):
                    inimigo.is_attacking = True
                    
                    # Tenta usar a habilidade especial do inimigo (se tiver)
                    if hasattr(inimigo, 'attack'):
                        inimigo.attack(defesa)
                    else:
                        # Ataque padrão
                        defesa.health -= inimigo.damage * 0.1  # Aplica dano por frame
                    
                    # Remove a defesa se sua vida chegou a zero (independente do tipo de ataque)
                    if defesa.health <= 0:
                        defesa.kill()
                    
                    break
            else:
                # Se não há colisão, o inimigo não está atacando
                inimigo.is_attacking = False