from abc import ABC, abstractmethod
from typing import List, Dict
import random

class WaveStrategy(ABC):
    @abstractmethod
    def get_wave_enemies(self, wave_number: int) -> List[Dict[str, any]]:
        """
        Retorna lista simples de inimigos para spawnar na onda.
        
        Returns:
            Lista de dicts: [{'type': 'bicho_papao', 'lane': 0, 'delay': 1.0}]
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        pass


class LinearWaveStrategy(WaveStrategy):
    """Estratégia linear - dificuldade aumenta gradualmente."""
    
    def get_wave_enemies(self, wave_number: int) -> List[Dict[str, any]]:
        """Mais inimigos a cada onda, distribuídos aleatoriamente."""
        enemies = []
        enemy_count = 1 + wave_number  # Onda 1: 2 inimigos, Onda 2: 3 inimigos, etc.
        
        for i in range(enemy_count):
            enemies.append({
                'type': 'bicho_papao',
                'lane': random.randint(0, 5),  # Lane aleatória (0-5)
                'delay': i * 2.0  # 2 segundos entre cada spawn
            })
        
        return enemies
    
    def get_strategy_name(self) -> str:
        return "Linear"


class IntenseWaveStrategy(WaveStrategy):
    """Estratégia intensa - mais inimigos em menos tempo."""
    
    def get_wave_enemies(self, wave_number: int) -> List[Dict[str, any]]:
        """Muitos inimigos rapidamente."""
        enemies = []
        enemy_count = 2 + (wave_number * 2)  # Cresce mais rápido
        
        for i in range(enemy_count):
            enemies.append({
                'type': 'bicho_papao',
                'lane': random.randint(0, 5),
                'delay': i * 1.0  # 1 segundo entre spawns (mais rápido)
            })
        
        return enemies
    
    def get_strategy_name(self) -> str:
        return "Intense"