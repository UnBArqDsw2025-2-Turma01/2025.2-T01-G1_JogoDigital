import pygame
from typing import List, Dict
from enum import Enum
from Model.Wave.WaveStrategy import WaveStrategy, LinearWaveStrategy, IntenseWaveStrategy
from Model.Enemies.EnemyPrototype import EnemyFactory
from Template.UIConfigs import NUM_LINHAS, NUM_COLUNAS

class WaveState(Enum):
    WAITING = "waiting"          
    SPAWNING = "spawning"        
    ACTIVE = "active"           
    COMPLETED = "completed"     

class WaveManager:
    def __init__(self, strategy_type: str = "linear", total_waves: int = 5):
        # Reutiliza Strategy Pattern
        if strategy_type == "intense":
            self._strategy = IntenseWaveStrategy()
        else:
            self._strategy = LinearWaveStrategy()
        
        self._current_wave = 0
        self._total_waves = total_waves
        self._state = WaveState.WAITING
        
        # Controle de spawn
        self._spawn_timer = 0.0
        self._enemies_to_spawn = []
        
        print(f"[WaveManager] Inicializado: {self._strategy.get_strategy_name()} - {total_waves} ondas")
    
    def start_next_wave(self) -> bool:
        if self._current_wave >= self._total_waves:
            self._state = WaveState.COMPLETED
            return False
        
        self._current_wave += 1
        self._enemies_to_spawn = self._strategy.get_wave_enemies(self._current_wave)
        self._spawn_timer = 0.0
        self._state = WaveState.SPAWNING
        
        print(f"[WaveManager] Iniciando onda {self._current_wave}/{self._total_waves}")
        print(f"  - {len(self._enemies_to_spawn)} inimigos para spawnar")
        
        return True
    
    def update(self, delta_time: float) -> None:
        if self._state == WaveState.SPAWNING:
            self._update_spawning(delta_time)
        elif self._state == WaveState.ACTIVE:
            self._check_wave_completion()
    
    def _update_spawning(self, delta_time: float) -> None:
        self._spawn_timer += delta_time
        
        # Spawna inimigos que já passaram do delay
        enemies_spawned = False
        for enemy_data in self._enemies_to_spawn:
            if not enemy_data.get('spawned', False) and self._spawn_timer >= enemy_data['delay']:
                self._spawn_enemy(enemy_data['type'], enemy_data['lane'])
                enemy_data['spawned'] = True
                enemies_spawned = True
        
        # Verifica se terminou de spawnar todos
        all_spawned = all(enemy.get('spawned', False) for enemy in self._enemies_to_spawn)
        if all_spawned:
            self._state = WaveState.ACTIVE
            print(f"[WaveManager] Onda {self._current_wave} - Todos inimigos spawnados")
    
    def _spawn_enemy(self, enemy_type: str, lane: int) -> bool:
        # Garante que a lane está dentro dos limites
        lane = max(0, min(lane, NUM_LINHAS - 1))
        spawn_x = NUM_COLUNAS - 1  # Spawna na direita
        
        # Reutiliza EnemyFactory
        enemy = EnemyFactory.create_enemy(enemy_type, spawn_x, lane)
        
        if enemy:
            print(f"[WaveManager] {enemy_type} spawnado na lane {lane}")
            return True
        else:
            print(f"[WaveManager] ERRO: Falha ao spawnar {enemy_type}")
            return False
    
    def _check_wave_completion(self) -> None:
        """Verifica se a onda atual terminou."""
        from Model.sprite_groups import sprite_manager
        
        # Se não há mais inimigos, onda terminou
        if len(sprite_manager.inimigos) == 0:
            print(f"[WaveManager] Onda {self._current_wave} concluída!")
            self._state = WaveState.WAITING
    
    def is_wave_complete(self) -> bool:
        return self._state == WaveState.WAITING
    
    def is_all_waves_complete(self) -> bool:
        return self._state == WaveState.COMPLETED
    
    def get_current_wave(self) -> int:
        return self._current_wave
    
    def get_total_waves(self) -> int:
        return self._total_waves
    
    def get_state(self) -> WaveState:
        return self._state
    
    def get_progress(self) -> Dict[str, any]:
        try:
            from Model.sprite_groups import sprite_manager
            enemies_remaining = len(sprite_manager.inimigos)
        except:
            enemies_remaining = 0
            
        return {
            'current_wave': self._current_wave,
            'total_waves': self._total_waves,
            'state': self._state.value,
            'enemies_remaining': enemies_remaining
        }