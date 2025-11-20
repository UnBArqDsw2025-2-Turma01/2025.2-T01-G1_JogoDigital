from abc import ABC, abstractmethod
from typing import Dict, Optional


class IEnemyPrototype(ABC):
    
    @abstractmethod
    def clone(self):
        pass


class EnemyPrototypeRegistry:
    
    _prototypes: Dict[str, IEnemyPrototype] = {}
    
    @classmethod
    def register(cls, enemy_type: str, prototype: IEnemyPrototype):
        cls._prototypes[enemy_type] = prototype
    
    @classmethod
    def create(cls, enemy_type: str, grid_x: int, grid_y: int, **kwargs):
        if enemy_type in cls._prototypes:
            cloned_prototype = cls._prototypes[enemy_type].clone()
            
            if kwargs:
                cloned_prototype.configure(**kwargs)
            
            if hasattr(cloned_prototype, 'create_enemy'):
                return cloned_prototype.create_enemy(grid_x, grid_y)
            
        return None
    
    @classmethod
    def get_types(cls) -> list:
        return list(cls._prototypes.keys())


class EnemyFactory:
    
    @classmethod
    def create_enemy(cls, enemy_type: str, grid_x: int, grid_y: int, **kwargs):
        return EnemyPrototypeRegistry.create(enemy_type, grid_x, grid_y, **kwargs)
    
    @classmethod
    def create_random_enemy(cls, grid_x: int, grid_y: int):
        import random
        types = EnemyPrototypeRegistry.get_types()
        if types:
            enemy_type = random.choice(types)
            return cls.create_enemy(enemy_type, grid_x, grid_y)
        return None


def initialize_enemy_prototypes():
    try:
        from Model.Enemies.bichopapao import BichoPapaoPrototype
        
        EnemyPrototypeRegistry.register("bicho_papao", BichoPapaoPrototype())
        print("[EnemyPrototype] Protótipos inicializados")
        
    except ImportError as e:
        print(f"[EnemyPrototype] ERRO: {e}")