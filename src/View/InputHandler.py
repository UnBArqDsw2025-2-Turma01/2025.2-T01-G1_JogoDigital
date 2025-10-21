import pygame
from typing import Optional, Callable, Dict, List, Protocol
from enum import Enum

class InputHandler(Protocol):
    """Interface que handlers de input devem implementar."""
    def handle_input(self, event: pygame.event.Event) -> bool:
        """
        Processa um evento de input.
        Retorna True se consumiu o evento, False caso contrário.
        """
        ...

class InputType(Enum):
    """Tipos de input suportados."""
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    JOYSTICK = "joystick"
    QUIT = "quit"

class InputHandler:
    """
    Responsabilidades:
    - Esconder a complexidade de captura e distribuição de eventos
    - Gerenciar atalhos globais
    - Fornecer interface simples para processamento de inputs
    """

    _global_handlers: Dict[str, Callable] = {}
    _input_enabled = True
    _current_screen_name: Optional[str] = None

    _keys_pressed: Dict[int, bool] = {}
    _mouse_pos: tuple = (0, 0)
    _mouse_buttons: Dict[int, bool] = {}
    
    _events_processed = 0
    _events_filtered = 0

    @classmethod
    def inicializar(cls):
        """Inicializa o Facade de Input."""
        cls._global_handlers.clear()
        cls._keys_pressed.clear()
        cls._mouse_buttons.clear()
        cls._input_enabled = True
        cls._current_screen_name = None
        print("[InputHandler] Facade de Input inicializado")

    @classmethod
    def add_global_handler(cls, nome: str, handler: Callable):
        """
        Adiciona um handler global ao facade.
        
        Args:
            nome: Identificador único do handler
            handler: Função que recebe (event) e retorna bool (True = consumiu evento)
        """
        cls._global_handlers[nome] = handler
        print(f"[InputHandler] Handler global '{nome}' registrado")
    
    @classmethod
    def remove_global_handler(cls, nome: str):
        """Remove um handler global."""
        if nome in cls._global_handlers:
            del cls._global_handlers[nome]
            print(f"[InputHandler] Handler global '{nome}' removido")

    @classmethod
    def process_events(cls) -> bool:
        """
        Interface simplificada para processar todos os eventos.
        Esconde a complexidade de captura e distribuição de eventos.
        
        Returns:
            bool: False se recebeu evento QUIT, True caso contrário
        """
        if not cls._input_enabled:
            pygame.event.clear()
            return True
        
        for event in pygame.event.get():
            cls._events_processed += 1
            
            cls._atualizar_estado(event)

            if event.type == pygame.QUIT:
                return False

            if cls._processar_handlers_globais(event):
                continue

            cls._distribuir_evento(event)
        
        return True
    
    @classmethod
    def _distribuir_evento(cls, event: pygame.event.Event):
        """
        Distribui evento para modais ou screen atual.
        Esconde a complexidade de priorização (modais > screen).
        """
        from Core.ScreenManager import ScreenManager
        from View.ViewRenderer import ViewRenderer

        if ScreenManager._modals:
            top_modal = ScreenManager._modals[-1]
            result = top_modal.handle_event(event)
            if result == 'close':
                ScreenManager.pop_modal()
            return

        current_screen = ViewRenderer.get_current_screen()
        if current_screen:
            current_screen.handle_event(event)

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
    def _processar_handlers_globais(cls, event: pygame.event.Event) -> bool:
        """
        Processa handlers globais.
        Retorna True se algum handler consumiu o evento.
        """
        for nome, handler in cls._global_handlers.items():
            try:
                if handler(event):
                    return True
            except Exception as e:
                print(f"[InputHandler] ERRO no handler global '{nome}': {e}")
        return False

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

    @classmethod
    def enable(cls):
        """Habilita processamento de inputs."""
        cls._input_enabled = True
        print("[InputHandler] Input habilitado")
    
    @classmethod
    def disable(cls):
        """Desabilita processamento de inputs (útil para cutscenes, etc.)."""
        cls._input_enabled = False
        print("[InputHandler] Input desabilitado")
    
    @classmethod
    def is_enabled(cls) -> bool:
        """Verifica se input está habilitado."""
        return cls._input_enabled

    @classmethod
    def setup_default_shortcuts(cls):
        """
        Configura atalhos globais padrão do projeto.
        Esconde a complexidade de registro de handlers.
        """
        
        def handler_esc(event):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from Core.ScreenManager import ScreenManager
                from View.Modal.PauseModal import PauseModal
                from View.ViewRenderer import ViewRenderer
                
                tela_atual = ViewRenderer.get_current_screen_name()
                
                if tela_atual == "menu":
                    print("[InputHandler] ESC - Fechando jogo")
                    pygame.quit()
                    exit()
                    return True
                
                elif tela_atual == "jogo":
                    if ScreenManager._modals:
                        print("[InputHandler] ESC - Fechando modal")
                        ScreenManager.pop_modal()
                    else:
                        print("[InputHandler] ESC - Abrindo PauseModal")
                        ScreenManager.push_modal(PauseModal())
                    return True
                
            return False
        
        cls.add_global_handler("esc", handler_esc)

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
    
    @classmethod
    def debug_info(cls) -> dict:
        """Retorna informações de debug."""
        return {
            'input_habilitado': cls._input_enabled,
            'handlers_globais': list(cls._global_handlers.keys()),
            'eventos_processados': cls._events_processed,
            'teclas_pressionadas': len([k for k, v in cls._keys_pressed.items() if v]),
            'mouse_pos': cls._mouse_pos,
        }