# View/ViewRenderer.py
"""
Hub/Facade centralizado para todos os renderers do projeto.
Gerencia fontes, cache de screens e fornece interface unificada para outros pacotes.
"""

import pygame
from typing import Optional, Dict

class ViewRenderer:
    """
    Facade/Hub centralizado para todos os renderers.
    
    Responsabilidades:
    - Gerenciar recursos compartilhados (fontes, cache)
    - Fornecer interface unificada para Core e outros pacotes
    - Controlar ciclo de vida das screens
    """
    
    # === RECURSOS COMPARTILHADOS ===
    FONTE = None
    FONTE_PEQUENA = None
    FONTE_GRANDE = None
    
    # === CACHE DE SCREENS ===
    _screens: Dict[str, object] = {}
    _current_screen_name: Optional[str] = None
    
    # === INICIALIZAÇÃO ===
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
    
    # === GERENCIAMENTO DE SCREENS ===
    @classmethod
    def get_screen(cls, screen_name: str):
        """
        Retorna screen específica (com cache).
        Lazy loading: cria a screen apenas quando necessário.
        """
        if screen_name not in cls._screens:
            # Lazy load - importa e cria apenas quando necessário
            if screen_name == "game" or screen_name == "jogo":
                from View.GameScreen.GameScreen import GameScreen
                cls._screens[screen_name] = GameScreen()
                print(f"[ViewRenderer] GameScreen carregada e cacheada")
                
            elif screen_name == "menu":
                from View.MenuScreen.MenuScreen import MenuScreen
                cls._screens[screen_name] = MenuScreen()
                print(f"[ViewRenderer] MenuScreen carregada e cacheada")
            else:
                print(f"[ViewRenderer] AVISO: Screen '{screen_name}' não reconhecida")
                return None
        
        return cls._screens.get(screen_name)
    
    @classmethod
    def set_current_screen(cls, screen_name: str):
        """Define a screen atual (para tracking)."""
        cls._current_screen_name = screen_name
    
    # === INTERFACE PÚBLICA (Facade Pattern) ===
    @classmethod
    def render_screen(cls, screen_name: str, surface: pygame.Surface):
        """
        Renderiza tela específica.
        Interface principal para ScreenManager e outros pacotes.
        """
        screen = cls.get_screen(screen_name)
        if screen:
            screen.draw(surface)
    
    @classmethod
    def update_screen(cls, screen_name: str):
        """Atualiza lógica de tela específica."""
        screen = cls.get_screen(screen_name)
        if screen:
            screen.update()
    
    @classmethod
    def handle_event(cls, screen_name: str, event: pygame.event.Event):
        """Processa evento na tela atual."""
        screen = cls.get_screen(screen_name)
        if screen:
            screen.handle_event(event)
    
    # === UTILIDADES COMPARTILHADAS ===
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
    
    # === DEBUG/MÉTRICAS ===
    @classmethod
    def debug_info(cls) -> dict:
        """Retorna informações de debug sobre o estado do Hub."""
        return {
            'screens_cacheadas': list(cls._screens.keys()),
            'total_screens': len(cls._screens),
            'screen_atual': cls._current_screen_name,
            'fontes_inicializadas': cls.FONTE is not None
        }
    
    @classmethod
    def limpar_cache(cls):
        """Limpa cache de screens (útil para reload ou transições)."""
        cls._screens.clear()
        print("[ViewRenderer] Cache de screens limpo")