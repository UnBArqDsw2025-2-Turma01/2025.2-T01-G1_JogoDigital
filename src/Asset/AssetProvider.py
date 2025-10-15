# Asset/AssetProvider.py

import pygame
from Template.UIConfigs import * # Importa as constantes de tamanho

class AssetProvider:
    # Assets de classe para armazenar as imagens carregadas
    ASSETS = {}
    
    @classmethod
    def carregar_assets(cls):
        """Carrega e escala todos os assets do jogo."""
        
        try:
            # MAP TILES
            cls.ASSETS['grass_claro'] = pygame.transform.scale(pygame.image.load('src/Asset/maps/map1/titleset/grass1.png').convert_alpha(), (TAMANHO_QUADRADO, TAMANHO_QUADRADO))
            cls.ASSETS['grass_escuro'] = pygame.transform.scale(pygame.image.load('src/Asset/maps/map1/titleset/grass2.png').convert_alpha(), (TAMANHO_QUADRADO, TAMANHO_QUADRADO))
            
            # CAIPORA
            cls.ASSETS['caipora_attack'] = [
                pygame.transform.scale(pygame.image.load(f'src/Asset/characters/defense/caipora/caipora_attack{i}.png').convert_alpha(), (TAMANHO_CAIPORA, TAMANHO_CAIPORA))
                for i in range(1, 3) 
            ]
            cls.ASSETS['caipora_projectile'] = pygame.transform.scale(pygame.image.load('src/Asset/characters/defense/caipora/caipora_arrow.png').convert_alpha(), (30, 30))
            
            # BICHO PAPÃO
            bp_walk = [
                pygame.image.load(f'src/Asset/characters/enemies/bicho-papao/bp_walk{i}.png').convert_alpha()
                for i in range(1, 5) 
            ]
            cls.ASSETS['bp_walk'] = [
                pygame.transform.scale(pygame.transform.flip(img, True, False), (TAMANHO_BP, TAMANHO_BP))
                for img in bp_walk
            ]
            
            print("Assets carregados com sucesso.")
        
        except pygame.error as e:
            print(f"ERRO CRÍTICO ao carregar assets: {e}")
            pygame.quit()
            exit()
            
    @classmethod
    def get(cls, key):
        """Método helper para acessar um asset."""
        return cls.ASSETS.get(key)