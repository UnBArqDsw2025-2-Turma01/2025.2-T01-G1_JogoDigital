from typing import List, Optional
from enum import Enum

class LevelStatus(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked" 
    COMPLETED = "completed"

class Level:
    
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