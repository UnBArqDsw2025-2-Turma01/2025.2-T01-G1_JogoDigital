# Template/PhysicsEngine.py

import pygame
from Model.Entities import projeteis_grupo, inimigos_grupo

class PhysicsEngine:
    @classmethod
    def processar_colisoes(cls):
        """Processa a colisão de projéteis com inimigos e aplica dano."""
        
        # True (remove projetil), False (NÃO remove inimigo)
        colisoes = pygame.sprite.groupcollide(projeteis_grupo, inimigos_grupo, True, False)

        for projetil, inimigos_atingidos in colisoes.items():
            for inimigo in inimigos_atingidos:
                inimigo.vida -= 1 
                # A remoção final do inimigo ocorre no próximo 'update()' se vida <= 0
                # print(f"Bicho Papão atingido! Vida restante: {inimigo.vida}") # Opcional