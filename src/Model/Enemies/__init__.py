from .EnemyPrototype import (
    IEnemyPrototype,
    EnemyPrototypeRegistry, 
    EnemyFactory,
    initialize_enemy_prototypes
)

from .enemy import Enemy
from .bichopapao import BichoPapao, BichoPapaoPrototype

from .WalkingState import WalkingState
from .AttackingState import AttackingState

__all__ = [
    'IEnemyPrototype',
    'EnemyPrototypeRegistry',
    'EnemyFactory',
    'Enemy',
    'BichoPapao',
    'BichoPapaoPrototype',
    'WalkingState',
    'AttackingState',
    'initialize_enemy_prototypes'
]