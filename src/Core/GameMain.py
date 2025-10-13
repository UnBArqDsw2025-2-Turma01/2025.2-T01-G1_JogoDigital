# Core/GameMain.py

import pygame
from Core.ScreenManager import ScreenManager
from Core.EventManager import EventManager
from Model.Level import Level
from Model.Entities import caiporas_grupo, inimigos_grupo, projeteis_grupo
from Template.PhysicsEngine import PhysicsEngine
from View.ViewRenderer import ViewRenderer
from Template.UIConfigs import FPS

class GameMain:
    def __init__(self):
        # 1. Inicializa Pygame e carrega Assets
        ScreenManager.inicializar_pygame()
        
        # 2. Inicializa as fontes APÓS o Pygame estar pronto
        ViewRenderer.inicializar_fontes() 
        
        # 3. Inicializa o Mapa e as Entidades Iniciais
        Level.inicializar_mapa()
        
        # Variáveis de Estado do Jogo (centralizadas aqui)
        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

    def update(self):
        """Lógica de atualização do jogo."""
        
        PhysicsEngine.processar_colisoes()
        
        caiporas_grupo.update()
        inimigos_grupo.update()
        projeteis_grupo.update()
        
    def loop(self):
        """Loop principal do jogo."""
        rodando = True
        relogio = ScreenManager.get_relogio()
        
        while rodando:
            
            # --- INPUT/EVENTOS ---
            rodando, self.state_vars = EventManager.processar_eventos(self.state_vars)
            if not rodando:
                break
            
            # --- ATUALIZAÇÃO ---
            if not self.state_vars['GAME_PAUSED']:
                self.update()
            
            # --- RENDERIZAÇÃO ---
            ViewRenderer.renderizar(
                self.state_vars['MODO_COLOCACAO_ATIVO'], 
                self.state_vars['GAME_PAUSED']
            )
            
            relogio.tick(FPS)
            
        pygame.quit()