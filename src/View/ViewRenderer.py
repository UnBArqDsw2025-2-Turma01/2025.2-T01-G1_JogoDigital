import pygame
from typing import Optional, Dict, Protocol

class IScreen(Protocol):
    """Interface que todas as screens devem implementar."""
    def open_screen(self) -> None:
        """Chamado quando a screen é aberta."""
        ...
    
    def close_screen(self) -> None:
        """Chamado quando a screen é fechada."""
        ...
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Processa um evento."""
        ...
    
    def update(self) -> None:
        """Atualiza a lógica da screen."""
        ...
    
    def draw(self, surface: pygame.Surface) -> None:
        """Renderiza a screen."""
        ...

class ViewRenderer:
    """
    Facade que simplifica o gerenciamento de screens.
    
    Responsabilidades:
    - Esconder a complexidade de transição entre screens
    - Gerenciar recursos compartilhados (fontes)
    - Fornecer interface simples para ScreenManager
    """

    FONTE = None
    FONTE_PEQUENA = None
    FONTE_GRANDE = None

    _current_screen: Optional[IScreen] = None
    _current_screen_name: Optional[str] = None
    _all_screens: Dict[str, IScreen] = {}

    @classmethod
    def inicializar(cls):
        """Inicializa recursos globais de renderização."""
        cls.inicializar_fontes()
        print("[ViewRenderer] Hub inicializado com sucesso")
    
    @classmethod
    def inicializar_fontes(cls):
        """Cria os objetos de fonte APÓS Pygame ter sido inicializado."""
        if cls.FONTE is None:
            cls.FONTE = pygame.font.SysFont('Arial', 30)
            cls.FONTE_PEQUENA = pygame.font.SysFont('Arial', 20)
            cls.FONTE_GRANDE = pygame.font.SysFont('Arial', 48)
            print("[ViewRenderer] Fontes inicializadas")

    @classmethod
    def add_screen(cls, screen_name: str, screen: IScreen):
        """Adiciona uma screen ao facade."""
        cls._all_screens[screen_name] = screen
        print(f"[ViewRenderer] Screen '{screen_name}' registrada")
    
    @classmethod
    def init_screens(cls, initial_screen_name: str):
        """
        Inicializa todas as screens e abre a inicial.
        Fecha todas as outras screens antes de abrir a inicial.
        """
        cls._close_all_screens()
        cls._current_screen_name = initial_screen_name
        cls._current_screen = cls._all_screens.get(initial_screen_name)
        if cls._current_screen:
            cls._current_screen.open_screen()
            print(f"[ViewRenderer] Screen inicial '{initial_screen_name}' aberta")
    
    @classmethod
    def transition_to(cls, screen_name: str):
        """
        Transição simplificada entre screens.
        Fecha a screen atual e abre a nova.
        """
        if screen_name not in cls._all_screens:
            print(f"[ViewRenderer] ERRO: Screen '{screen_name}' não encontrada")
            return

        if cls._current_screen:
            cls._current_screen.close_screen()

        cls._current_screen_name = screen_name
        cls._current_screen = cls._all_screens[screen_name]
        cls._current_screen.open_screen()
        print(f"[ViewRenderer] Transição para '{screen_name}' concluída")
    
    @classmethod
    def _close_all_screens(cls):
        """Fecha todas as screens registradas."""
        for screen in cls._all_screens.values():
            screen.close_screen()
    
    @classmethod
    def render(cls, surface: pygame.Surface):
        """
        Renderiza a screen atual e modais ativos.
        Esconde a complexidade de renderização em camadas.
        """
        from Core.ScreenManager import ScreenManager

        if cls._current_screen:
            cls._current_screen.draw(surface)

        for modal in ScreenManager._modals:
            modal.draw(surface)
    
    @classmethod
    def update(cls):
        """
        Atualiza a lógica da screen atual ou modal ativo.
        Esconde a complexidade de priorização.
        """
        from Core.ScreenManager import ScreenManager
        
        if ScreenManager._modals:
            top_modal = ScreenManager._modals[-1]
            if hasattr(top_modal, 'update'):
                top_modal.update()
        elif cls._current_screen:
            cls._current_screen.update()
    
    @classmethod
    def get_current_screen_name(cls) -> Optional[str]:
        """Retorna o nome da screen atual."""
        return cls._current_screen_name
    
    @classmethod
    def get_current_screen(cls) -> Optional[IScreen]:
        """Retorna a screen atual."""
        return cls._current_screen
    
    @classmethod
    def get_fonte(cls, tamanho: str = "normal") -> pygame.font.Font:
        """
        Retorna fonte do tamanho especificado.
        
        Args:
            tamanho: 'pequena', 'normal', 'grande'
        """
        if tamanho == "pequena":
            return cls.FONTE_PEQUENA
        elif tamanho == "grande":
            return cls.FONTE_GRANDE
        return cls.FONTE
    
    @classmethod
    def debug_info(cls) -> dict:
        """Retorna informações de debug."""
        return {
            'screens_registradas': list(cls._all_screens.keys()),
            'total_screens': len(cls._all_screens),
            'screen_atual': cls._current_screen_name,
            'fontes_inicializadas': cls.FONTE is not None
        }