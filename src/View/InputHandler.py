import pygame
from typing import Optional, Callable, Dict, List
from enum import Enum

class InputType(Enum):
    """Tipos de input suportados."""
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    JOYSTICK = "joystick"
    QUIT = "quit"

class InputHandler:
    """
    Hub/Facade centralizado para todos os inputs.
    
    Responsabilidades:
    - Capturar eventos do Pygame
    - Classificar e filtrar eventos
    - Distribuir eventos para handlers registrados
    - Gerenciar atalhos globais
    - Fornecer interface unificada para input
    """
    
    # === ESTADO GLOBAL ===
    _global_handlers: Dict[str, Callable] = {}  # Handlers globais (ex: ESC, F11)
    _screen_handlers: Dict[str, Callable] = {}  # Handlers por screen
    _event_filters: List[Callable] = []  # Filtros customizados
    _input_enabled = True  # Flag para pausar inputs
    
    # === ESTADO DE INPUT (para consultas) ===
    _keys_pressed: Dict[int, bool] = {}  # Teclas pressionadas
    _mouse_pos: tuple = (0, 0)  # Posição do mouse
    _mouse_buttons: Dict[int, bool] = {}  # Botões do mouse
    
    # === ESTATÍSTICAS ===
    _events_processed = 0
    _events_filtered = 0
    
    # === INICIALIZAÇÃO ===
    @classmethod
    def inicializar(cls):
        """Inicializa o Hub de Input."""
        cls._global_handlers.clear()
        cls._screen_handlers.clear()
        cls._event_filters.clear()
        cls._keys_pressed.clear()
        cls._mouse_buttons.clear()
        cls._input_enabled = True
        print("[InputHandler] Hub de Input inicializado")
    
    # === REGISTRO DE HANDLERS ===
    @classmethod
    def registrar_handler_global(cls, nome: str, handler: Callable):
        """
        Registra um handler global (processado antes de screen handlers).
        
        Args:
            nome: Identificador único do handler
            handler: Função que recebe (event) e retorna bool (True = consumiu evento)
        """
        cls._global_handlers[nome] = handler
        print(f"[InputHandler] Handler global '{nome}' registrado")
    
    @classmethod
    def registrar_handler_screen(cls, screen_name: str, handler: Callable):
        """
        Registra um handler para uma screen específica.
        
        Args:
            screen_name: Nome da screen ('menu', 'jogo', etc.)
            handler: Função que recebe (event) e retorna bool
        """
        cls._screen_handlers[screen_name] = handler
        print(f"[InputHandler] Handler de screen '{screen_name}' registrado")
    
    @classmethod
    def remover_handler_global(cls, nome: str):
        """Remove um handler global."""
        if nome in cls._global_handlers:
            del cls._global_handlers[nome]
            print(f"[InputHandler] Handler global '{nome}' removido")
    
    @classmethod
    def registrar_filtro(cls, filtro: Callable):
        """
        Registra um filtro de eventos.
        Filtro recebe (event) e retorna bool (True = processar, False = ignorar)
        """
        cls._event_filters.append(filtro)
    
    # === PROCESSAMENTO DE EVENTOS ===
    @classmethod
    def processar_eventos(cls, screen_name: Optional[str] = None) -> bool:
        """
        Processa todos os eventos da fila do Pygame.
        
        Args:
            screen_name: Nome da screen atual (para handlers específicos)
            
        Returns:
            bool: False se recebeu evento QUIT, True caso contrário
        """
        if not cls._input_enabled:
            pygame.event.clear()  # Limpa fila se input desabilitado
            return True
        
        for event in pygame.event.get():
            cls._events_processed += 1
            
            # Atualiza estado interno
            cls._atualizar_estado(event)
            
            # Aplica filtros
            if not cls._aplicar_filtros(event):
                cls._events_filtered += 1
                continue
            
            # Verifica QUIT
            if event.type == pygame.QUIT:
                return False
            
            # Processa handlers globais (prioridade)
            if cls._processar_handlers_globais(event):
                continue  # Evento consumido
            
            # Processa handler da screen atual
            if screen_name and screen_name in cls._screen_handlers:
                cls._screen_handlers[screen_name](event)
        
        return True
    
    @classmethod
    def processar_evento_unico(cls, event: pygame.event.Event, screen_name: Optional[str] = None):
        """
        Processa um único evento (útil para testes ou processamento customizado).
        
        Args:
            event: Evento do Pygame
            screen_name: Nome da screen atual
        """
        if not cls._input_enabled:
            return
        
        cls._events_processed += 1
        cls._atualizar_estado(event)
        
        if not cls._aplicar_filtros(event):
            cls._events_filtered += 1
            return
        
        # Handlers globais primeiro
        if cls._processar_handlers_globais(event):
            return
        
        # Handler da screen
        if screen_name and screen_name in cls._screen_handlers:
            cls._screen_handlers[screen_name](event)
    
    # === MÉTODOS INTERNOS ===
    @classmethod
    def _atualizar_estado(cls, event: pygame.event.Event):
        """Atualiza estado interno baseado no evento."""
        if event.type == pygame.KEYDOWN:
            cls._keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            cls._keys_pressed[event.key] = False
        elif event.type == pygame.MOUSEMOTION:
            cls._mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cls._mouse_buttons[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            cls._mouse_buttons[event.button] = False
    
    @classmethod
    def _aplicar_filtros(cls, event: pygame.event.Event) -> bool:
        """Aplica filtros registrados. Retorna True se evento deve ser processado."""
        for filtro in cls._event_filters:
            if not filtro(event):
                return False
        return True
    
    @classmethod
    def _processar_handlers_globais(cls, event: pygame.event.Event) -> bool:
        """
        Processa handlers globais.
        Retorna True se algum handler consumiu o evento.
        """
        for nome, handler in cls._global_handlers.items():
            try:
                if handler(event):
                    return True  # Evento consumido
            except Exception as e:
                print(f"[InputHandler] ERRO no handler global '{nome}': {e}")
        return False
    
    # === CONSULTAS DE ESTADO ===
    @classmethod
    def tecla_pressionada(cls, key: int) -> bool:
        """Verifica se uma tecla está pressionada."""
        return cls._keys_pressed.get(key, False)
    
    @classmethod
    def teclas_direcionais(cls) -> dict:
        """Retorna estado das teclas direcionais (WASD e setas)."""
        return {
            'cima': cls.tecla_pressionada(pygame.K_w) or cls.tecla_pressionada(pygame.K_UP),
            'baixo': cls.tecla_pressionada(pygame.K_s) or cls.tecla_pressionada(pygame.K_DOWN),
            'esquerda': cls.tecla_pressionada(pygame.K_a) or cls.tecla_pressionada(pygame.K_LEFT),
            'direita': cls.tecla_pressionada(pygame.K_d) or cls.tecla_pressionada(pygame.K_RIGHT),
        }
    
    @classmethod
    def mouse_posicao(cls) -> tuple:
        """Retorna posição atual do mouse."""
        return cls._mouse_pos
    
    @classmethod
    def mouse_botao_pressionado(cls, button: int = 1) -> bool:
        """Verifica se botão do mouse está pressionado (1=esquerdo, 2=meio, 3=direito)."""
        return cls._mouse_buttons.get(button, False)
    
    # === CONTROLE DE ESTADO ===
    @classmethod
    def habilitar_input(cls):
        """Habilita processamento de inputs."""
        cls._input_enabled = True
        print("[InputHandler] Input habilitado")
    
    @classmethod
    def desabilitar_input(cls):
        """Desabilita processamento de inputs (útil para cutscenes, etc.)."""
        cls._input_enabled = False
        print("[InputHandler] Input desabilitado")
    
    @classmethod
    def esta_habilitado(cls) -> bool:
        """Verifica se input está habilitado."""
        return cls._input_enabled
    
    # === ATALHOS GLOBAIS PRÉ-DEFINIDOS ===
    @classmethod
    def registrar_atalhos_padrao(cls):
        """
        Registra atalhos globais padrão do projeto.
        
        ESC - Comportamento dependente da tela:
        - Menu Principal: Fecha o jogo (pygame.quit)
        - GameScreen: Abre/Fecha PauseModal
        """
        
        def handler_esc(event):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from Core.ScreenManager import ScreenManager
                from View.Modal.PauseModal import PauseModal
                
                tela_atual = ScreenManager._tela_atual_nome
                
                # Menu Principal - Fecha o jogo
                if tela_atual == "menu":
                    print("[InputHandler] ESC no menu - Fechando jogo")
                    pygame.quit()
                    exit()
                    return True  # Consome evento
                
                # GameScreen - Abre/Fecha PauseModal
                elif tela_atual == "jogo":
                    if ScreenManager._modals:
                        # Se há modal aberto, fecha ele
                        print("[InputHandler] ESC - Fechando modal")
                        ScreenManager.pop_modal()
                    else:
                        # Se não há modal, abre PauseModal
                        print("[InputHandler] ESC - Abrindo PauseModal")
                        ScreenManager.push_modal(PauseModal())
                    return True  # Consome evento
                
            return False
        
        cls.registrar_handler_global("esc", handler_esc)
    
    # === UTILITÁRIOS ===
    @classmethod
    def classificar_evento(cls, event: pygame.event.Event) -> InputType:
        """Classifica tipo do evento."""
        if event.type == pygame.QUIT:
            return InputType.QUIT
        elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
            return InputType.KEYBOARD
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return InputType.MOUSE
        elif event.type in (pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
            return InputType.JOYSTICK
        return None
    
    # === DEBUG/MÉTRICAS ===
    @classmethod
    def debug_info(cls) -> dict:
        """Retorna informações de debug sobre o estado do Hub."""
        return {
            'input_habilitado': cls._input_enabled,
            'handlers_globais': list(cls._global_handlers.keys()),
            'handlers_screens': list(cls._screen_handlers.keys()),
            'filtros_ativos': len(cls._event_filters),
            'eventos_processados': cls._events_processed,
            'eventos_filtrados': cls._events_filtered,
            'teclas_pressionadas': len([k for k, v in cls._keys_pressed.items() if v]),
            'mouse_pos': cls._mouse_pos,
        }
    
    @classmethod
    def resetar_estatisticas(cls):
        """Reseta contadores de estatísticas."""
        cls._events_processed = 0
        cls._events_filtered = 0
        print("[InputHandler] Estatísticas resetadas")