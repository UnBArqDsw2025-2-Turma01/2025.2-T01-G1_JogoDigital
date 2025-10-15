import random
from typing import List, Optional
from enum import Enum
from Template.UIConfigs import NUM_LINHAS, NUM_COLUNAS
from Model.Entities import Caipora, BichoPapao

class LevelStatus(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked" 
    COMPLETED = "completed"

class Level:
    MAPA_LOGICO = []
    
    def __init__(self, 
                 level_id: str,
                 name: str,
                 prerequisites: Optional[List[str]] = None):
        self._level_id = level_id
        self._name = name
        self._prerequisites = prerequisites or []
        self._status = LevelStatus.LOCKED
        self._stars_earned = 0

    @property
    def level_id(self) -> str:
        return self._level_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def prerequisites(self) -> List[str]:
        return self._prerequisites.copy()

    @property
    def status(self) -> LevelStatus:
        return self._status

    @property
    def stars_earned(self) -> int:
        return self._stars_earned

    def is_unlocked(self, completed_levels: List[str]) -> bool:
        if not self._prerequisites:
            return True
        return all(prereq in completed_levels for prereq in self._prerequisites)

    def unlock(self, completed_levels: List[str]) -> bool:
        if self.is_unlocked(completed_levels):
            if self._status == LevelStatus.LOCKED:
                self._status = LevelStatus.UNLOCKED
            return True
        return False

    def complete(self, stars: int = 1) -> bool:
        if self._status in [LevelStatus.UNLOCKED, LevelStatus.COMPLETED]:
            self._status = LevelStatus.COMPLETED
            if stars > self._stars_earned and 1 <= stars <= 3:
                self._stars_earned = stars
            return True
        return False
    
    @classmethod
    def inicializar_mapa(cls):
        """Inicializa o mapa lógico e a população inicial."""
        cls.MAPA_LOGICO = [[0] * NUM_COLUNAS for _ in range(NUM_LINHAS)] 
        
        for linha in range(NUM_LINHAS):
            cls.MAPA_LOGICO[linha][0] = 1 
            Caipora(0, linha)

        linha_bp = random.randint(0, NUM_LINHAS - 1)
        BichoPapao(NUM_COLUNAS - 1, linha_bp)
        
    @classmethod
    def is_posicao_vazia(cls, linha, coluna):
        """Verifica se uma posição no mapa está vazia."""
        return cls.MAPA_LOGICO[linha][coluna] == 0
        
    @classmethod
    def adicionar_entidade(cls, linha, coluna, entidade_type):
        """Adiciona uma entidade ao mapa lógico e cria a instância."""
        if entidade_type == 'Caipora' and cls.is_posicao_vazia(linha, coluna):
            cls.MAPA_LOGICO[linha][coluna] = 1
            Caipora(coluna, linha)
            return True
        return False