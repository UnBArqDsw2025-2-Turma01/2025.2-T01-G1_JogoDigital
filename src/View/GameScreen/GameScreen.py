import pygame
from Template.BaseScreen import BaseScreen
from Model.Level import Level
from View.GameScreen.GameScreenRenderer import GameScreenRenderer
from Core.ScreenManager import ScreenManager
from View.Modal.PauseModal import PauseModal
from Template.UIConfigs import *
from Model.Wave.WaveManager import WaveManager, WaveState

class GameScreen(BaseScreen):
    def __init__(self):
        super().__init__()

        # Inicializa mapa sem spawnar inimigos (será controlado pelo WaveManager)
        Level.inicializar_mapa(spawn_enemies=False)

        self.current_level = None
        
        # Sistema de ondas integrado
        self.wave_manager = WaveManager("linear", total_waves=5)
        self.game_started = False
        self.game_completed = False

        # Estado da tela
        self.state_vars = {
            'MODO_COLOCACAO_ATIVO': False,
            'GAME_PAUSED': False
        }

        # Botões específicos desta tela
        self.add_rect = pygame.Rect(50, 20, 120, 40)
        self.pause_rect = pygame.Rect(200, 20, 120, 40)
        self.coins_rect = pygame.Rect(350, 20, 120, 40)

        # Fonte
        self.font = pygame.font.SysFont(None, 24)

        # Cria o renderer desta tela
        self.renderer = GameScreenRenderer(self)

    def handle_event(self, event):
        """Processa eventos específicos da GameScreen."""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                from View.ViewRenderer import ViewRenderer
                ViewRenderer.transition_to("level_select")
            
            elif event.key == pygame.K_g and not self.game_started:
                # Inicia o jogo com ondas
                self._start_wave_game()
            
            elif event.key == pygame.K_SPACE and self.game_started:
                # Inicia próxima onda se a atual terminou
                self._try_start_next_wave()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Botão PAUSE
            if self.pause_rect.collidepoint(x, y):
                ScreenManager.push_modal(PauseModal())

            # Botão ADICIONAR
            elif self.add_rect.collidepoint(x, y):
                self.state_vars['MODO_COLOCACAO_ATIVO'] = not self.state_vars['MODO_COLOCACAO_ATIVO']

            # Grid para colocar Caipora
            elif self.state_vars['MODO_COLOCACAO_ATIVO']:
                self._handle_grid_click(x, y)

            # Clique em guaraná (coletar)
            else:
                self._handle_guarana_click(x, y)
    
    def _handle_grid_click(self, x: int, y: int):
        """Processa clique no grid para colocar Caipora."""
        grid_x_min = GRID_OFFSET_X
        grid_x_max = GRID_OFFSET_X + NUM_COLUNAS * TAMANHO_QUADRADO
        grid_y_min = GRID_OFFSET_Y
        grid_y_max = GRID_OFFSET_Y + NUM_LINHAS * TAMANHO_QUADRADO

        if grid_x_min <= x < grid_x_max and grid_y_min <= y < grid_y_max:
            coluna = (x - GRID_OFFSET_X) // TAMANHO_QUADRADO
            linha = (y - GRID_OFFSET_Y) // TAMANHO_QUADRADO
            if Level.adicionar_entidade(linha, coluna, 'Caipora'):
                self.state_vars['MODO_COLOCACAO_ATIVO'] = False
    
    def _handle_guarana_click(self, x: int, y: int):
        """Processa clique em guaranás para coletar."""
        from Model.sprite_groups import sprite_manager
        guaranas_grupo = sprite_manager.guaranas
        
        for guarana in list(guaranas_grupo):
            if guarana.rect.collidepoint(x, y):
                guarana.collect()
                self.renderer.coins += guarana.value
                print(f"Guaraná coletado! Coins: {self.renderer.coins}")
                break

    def set_current_level(self, level):
        self.current_level = level
        print(f"Nível configurado: {level.name}")
        Level.inicializar_mapa(spawn_enemies=False)  # WaveManager controlará os inimigos

    def _start_wave_game(self):
        """
        Inicia o jogo com sistema de ondas.
        Reutiliza estrutura existente de controle de jogo.
        """
        self.game_started = True
        self.game_completed = False
        
        # Limpa inimigos que possam ter sido criados na inicialização
        from Model.sprite_groups import sprite_manager
        sprite_manager.inimigos.empty()
        
        # Inicia primeira onda
        if self.wave_manager.start_next_wave():
            print(f"[GameScreen] Jogo iniciado! Pressione SPACE para próxima onda")
        else:
            print(f"[GameScreen] ERRO: Falha ao iniciar primeira onda")

    def _try_start_next_wave(self):
        """
        Tenta iniciar a próxima onda se a atual terminou.
        Integra com WaveManager existente.
        """
        if not self.game_started or self.game_completed:
            return
            
        if self.wave_manager.is_wave_complete():
            if self.wave_manager.start_next_wave():
                progress = self.wave_manager.get_progress()
                print(f"[GameScreen] Onda {progress['current_wave']}/{progress['total_waves']} iniciada!")
            else:
                print(f"[GameScreen] Todas as ondas concluídas!")
        else:
            print(f"[GameScreen] Aguarde a onda atual terminar...")

    def _complete_game(self):
        self.game_completed = True
        progress = self.wave_manager.get_progress()
        
        print(f"[GameScreen] JOGO CONCLUÍDO!")
        print(f"  - Ondas completadas: {progress['current_wave']}/{progress['total_waves']}")
        print(f"  - Pressione M para voltar ao menu")

    def get_wave_info(self):
        """
        Retorna informações das ondas para o renderer.
        Reutiliza padrão de exposição de dados para UI.
        """
        if not hasattr(self, 'wave_manager'):
            return None
            
        progress = self.wave_manager.get_progress()
        return {
            'game_started': self.game_started,
            'game_completed': self.game_completed,
            'current_wave': progress['current_wave'],
            'total_waves': progress['total_waves'],
            'wave_state': progress['state'],
            'enemies_remaining': progress['enemies_remaining']
        }

    def update(self):
        self.state_vars['GAME_PAUSED'] = bool(ScreenManager._modals)
        
        # Integra WaveManager ao loop principal (reutiliza estrutura de update existente)
        if self.game_started and not self.state_vars['GAME_PAUSED']:
            # Atualiza sistema de ondas
            self.wave_manager.update(1/60)  # 60 FPS
            
            # Verifica se jogo terminou
            if self.wave_manager.is_all_waves_complete() and not self.game_completed:
                self._complete_game()
        
        self.renderer.update()

    def draw(self, surface):
        self.renderer.draw(surface)
