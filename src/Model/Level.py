# Model/Level.py

import random
from Template.UIConfigs import NUM_LINHAS, NUM_COLUNAS
from Model.Entities import Caipora, BichoPapao

class Level:
    MAPA_LOGICO = []
    
    @classmethod
    def inicializar_mapa(cls):
        """Inicializa o mapa lógico e a população inicial."""
        cls.MAPA_LOGICO = [[0] * NUM_COLUNAS for _ in range(NUM_LINHAS)] 
        
        # População Inicial de Caiporas (Coluna 0)
        for linha in range(NUM_LINHAS):
            cls.MAPA_LOGICO[linha][0] = 1 
            Caipora(0, linha)

        # População Inicial de Bicho Papão (Coluna 8)
        linha_bp = random.randint(0, NUM_LINHAS - 1)
        BichoPapao(NUM_COLUNAS - 1, linha_bp)
        
    @classmethod
    def is_posicao_vazia(cls, linha, coluna):
        return cls.MAPA_LOGICO[linha][coluna] == 0
        
    @classmethod
    def adicionar_entidade(cls, linha, coluna, entidade_type):
        """Adiciona uma entidade ao mapa lógico e cria a instância."""
        if entidade_type == 'Caipora' and cls.is_posicao_vazia(linha, coluna):
            cls.MAPA_LOGICO[linha][coluna] = 1
            Caipora(coluna, linha)
            return True
        return False