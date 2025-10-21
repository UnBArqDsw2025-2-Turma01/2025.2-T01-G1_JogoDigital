import pygame
from Model.interfaces import IIterableCollection
from Model.Defense.caipora import Caipora
from Model.Enemies.enemy import Enemy
from Model.Items.arrow import Arrow

class PhysicsEngine:
    @classmethod
    def processar_colisoes(
        cls,
        projeteis_col: IIterableCollection[Arrow], 
        inimigos_col: IIterableCollection[Enemy], 
        caiporas_col: IIterableCollection[Caipora]
    ):
        # Colisão de projéteis com inimigos

        # Pega o iterador de projéteis e cria um snapshot da lista de projéteis
        iter_projeteis = projeteis_col.createIterator()
        
        # Percorre o snapshot de projéteis
        while iter_projeteis.hasMore():
            projetil = iter_projeteis.getNext()
            
            # Para cada projétil é criado um novo iterador de inimigos
            iter_inimigos = inimigos_col.createIterator()
            
            #Percorre o snapshot de inimigos
            while iter_inimigos.hasMore():
                inimigo = iter_inimigos.getNext()
                
                # Checa colisão entre o projétil e o inimigo
                if pygame.sprite.collide_rect(projetil, inimigo):
                    
                    # Usa o dano do projétil para reduzir a vida do inimigo
                    inimigo.health -= projetil.damage 
                    
                    if inimigo.health <= 0:
                        inimigo.kill() # Remove do grupo original
                    projetil.kill() # Remove o projétil do grupo original
                    break
        
        # Colisão de inimigos com defesas
        
        # Cria uma nova iteração de inimigos
        iter_inimigos_ataque = inimigos_col.createIterator()
        
        # Percorre o snapshot de inimigos
        while iter_inimigos_ataque.hasMore():
            inimigo = iter_inimigos_ataque.getNext()
            
            # Para cada inimigo, cria um novo iterador de Caiporas
            iter_caiporas = caiporas_col.createIterator()
            defesas_na_linha = [] # Lista temporária
            
            # Percorre o snapshot de Caiporas
            while iter_caiporas.hasMore():
                defesa = iter_caiporas.getNext()
                if defesa.grid_y == inimigo.grid_y:
                    defesas_na_linha.append(defesa)

            # Lógica de ataque
            atacou_alguem = False
            for defesa in defesas_na_linha:
                if pygame.sprite.collide_rect(inimigo, defesa):
                    inimigo.is_attacking = True
                    atacou_alguem = True
                    
                    if hasattr(inimigo, 'attack'):
                        inimigo.attack(defesa)
                    else:
                        defesa.health -= inimigo.damage * 0.1
                    
                    if defesa.health <= 0:
                        defesa.kill()
                    
                    break # Inimigo ataca apenas uma defesa por vez
            
            if not atacou_alguem:
                inimigo.is_attacking = False