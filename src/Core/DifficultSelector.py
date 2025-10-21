import pygame
from abc import ABC, abstractmethod

class StrategyDifficulty(ABC):
    
    @abstractmethod
    def obter_multiplicador_vida(self) -> float:
        pass

    @abstractmethod
    def obter_multiplicador_ataque(self) -> float:
        pass

    @abstractmethod
    def obter_multiplicador_velocidade(self) -> float:
        pass

    def aplicar_regras(self):
        print(f"[Core Log] Estratégia de Dificuldade '{self.__class__.__name__}' aplicada.")


class EasyStrategy(StrategyDifficulty):
    def obter_multiplicador_vida(self) -> float:
        return 0.7
    
    def obter_multiplicador_ataque(self) -> float:
        return 0.7
        
    def obter_multiplicador_velocidade(self) -> float:
        return 0.9


class NormalStrategy(StrategyDifficulty):
    def obter_multiplicador_vida(self) -> float:
        return 1.0
    
    def obter_multiplicador_ataque(self) -> float:
        return 1.0

    def obter_multiplicador_velocidade(self) -> float:
        return 1.0


class HardStrategy(StrategyDifficulty):
    def obter_multiplicador_vida(self) -> float:
        return 1.5
    
    def obter_multiplicador_ataque(self) -> float:
        return 1.5
        
    def obter_multiplicador_velocidade(self) -> float:
        return 1.2  

class DifficultySelector:
 
    _strategy: StrategyDifficulty | None = None
    _nivel: str = 'normal'

    @classmethod
    def inicializar(cls, nivel: str = 'normal'):
        cls.set_difficulty(nivel)

    @classmethod
    def set_difficulty(cls, nivel: str):
        nivel = (nivel or 'normal').lower()
        mapping = {
            'easy': EasyStrategy,
            'normal': NormalStrategy,
            'hard': HardStrategy,
        }
        Strategy = mapping.get(nivel, NormalStrategy)
        cls._strategy = Strategy()
        cls._nivel = nivel
        cls._strategy.aplicar_regras()

    @classmethod
    def obter_multiplicador_vida(cls) -> float:
        if cls._strategy is None:
            cls._strategy = NormalStrategy()
        return cls._strategy.obter_multiplicador_vida()

    @classmethod
    def obter_multiplicador_ataque(cls) -> float:
        if cls._strategy is None:
            cls._strategy = NormalStrategy()
        return cls._strategy.obter_multiplicador_ataque()

    @classmethod
    def obter_multiplicador_velocidade(cls) -> float:
        if cls._strategy is None:
            cls._strategy = NormalStrategy()
        return cls._strategy.obter_multiplicador_velocidade()

    @classmethod
    def get_current_level(cls) -> str:
        return cls._nivel