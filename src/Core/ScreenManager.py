import pygame
import os
from Template.UIConfigs import *
from Asset.AssetProvider import AssetProvider

class ScreenManager:
    """
    Gerenciador central de telas, modais e renderização.
    Pode trabalhar tanto com instâncias de Screen diretas
    quanto através do ViewRenderer Hub (padrão Facade).
    """
    TELA = None
    RELOGIO = None
    _telas = {}
    _tela_atual = None
    _tela_atual_nome = None  # nome da tela atual (para ViewRenderer Hub)
    _modals = []  # pilha de modais/overlays
    _usar_view_hub = False  # flag para usar ViewRenderer como Hub

    # --- 1. Inicialização global ---
    @classmethod
    def inicializar_pygame(cls):
        """Inicializa Pygame, relógio e carrega assets."""
        pygame.init()
        pygame.mixer.init()
        song_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Asset', 'songs', 'forest.wav'))
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(-1)

        if not pygame.font.get_init():
            pygame.font.init() 
            
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        cls.TELA = pygame.display.set_mode((LARGURA_TELA_JANELA, ALTURA_TELA_JANELA))
        pygame.display.set_caption(TITULO_JOGO)
        AssetProvider.carregar_assets()
        cls.RELOGIO = pygame.time.Clock()

    @classmethod
    def get_tela(cls):
        return cls.TELA

    @classmethod
    def get_relogio(cls):
        return cls.RELOGIO
    
    @classmethod
    def registrar_screens_via_hub(cls, screen_names):
        """
        Registra screens via ViewRenderer Hub.
        ViewRenderer criará as instâncias via lazy loading.
        Também registra handlers de input para cada screen no InputHandler.
        
        Args:
            screen_names: Lista de nomes de screens ['menu', 'jogo']
        """
        from View.ViewRenderer import ViewRenderer
        from View.InputHandler import InputHandler
        cls._usar_view_hub = True
        
        # Pré-carrega screens no Hub (opcional, lazy loading é automático)
        for name in screen_names:
            screen = ViewRenderer.get_screen(name)
            if screen:
                cls._telas[name] = screen
                # Registra handler de input para a screen
                cls._registrar_handler_input_screen(name, screen)
        
        print(f"[ScreenManager] Screens registradas via ViewRenderer Hub: {screen_names}")
        print(f"[ScreenManager] Handlers de input registrados no InputHandler")
    
    @classmethod
    def _registrar_handler_input_screen(cls, screen_name: str, screen):
        """Registra handler de input para uma screen no InputHandler Hub."""
        from View.InputHandler import InputHandler
        
        def screen_handler(event):
            """Handler que encaminha evento para a screen ou modal ativo."""
            # Prioridade: Modais > Screen
            if cls._modals:
                top_modal = cls._modals[-1]
                result = top_modal.handle_event(event)
                if result == 'close':
                    cls.pop_modal()
                return True  # Evento consumido pelo modal
            
            # Se não há modal, encaminha para screen
            if cls._tela_atual and cls._tela_atual_nome == screen_name:
                cls._tela_atual.handle_event(event)
            return False
        
        InputHandler.registrar_handler_screen(screen_name, screen_handler)

    @classmethod
    def set_tela(cls, nome_tela):
        """Troca a tela atual."""
        # Se estiver usando Hub e tela não foi carregada, busca no ViewRenderer
        if cls._usar_view_hub and nome_tela not in cls._telas:
            from View.ViewRenderer import ViewRenderer
            screen = ViewRenderer.get_screen(nome_tela)
            if screen:
                cls._telas[nome_tela] = screen
        
        if nome_tela in cls._telas:
            cls._tela_atual = cls._telas[nome_tela]
            cls._tela_atual_nome = nome_tela
            
            # Se estiver usando ViewRenderer Hub, notifica
            if cls._usar_view_hub:
                from View.ViewRenderer import ViewRenderer
                ViewRenderer.set_current_screen(nome_tela)
        else:
            print(f"[ScreenManager] ERRO: Screen '{nome_tela}' não encontrada")

    @classmethod
    def get_tela_atual(cls):
        return cls._tela_atual

    @classmethod
    def handle_events(cls):
        """
        Processa eventos através do InputHandler Hub.
        O InputHandler já captura pygame.event.get() e distribui para handlers registrados.
        """
        from View.InputHandler import InputHandler
        
        continuar = InputHandler.processar_eventos(screen_name=cls._tela_atual_nome)
        
        # Se não estiver usando handlers registrados no InputHandler,
        # a screen atual pode processar eventos diretamente via handle_event()
        # (isto será migrado gradualmente para usar handlers registrados)
        
        return continuar

    @classmethod
    def update(cls):
        # atualiza tela base apenas se não houver modal que bloqueie
        if cls._tela_atual:
            if not cls._modals:
                cls._tela_atual.update()
            else:
                # atualiza apenas o topo das modais
                top = cls._modals[-1]
                if hasattr(top, 'update'):
                    top.update()

    @classmethod
    def draw(cls):
        if cls._tela_atual:
            cls._tela_atual.draw(cls.TELA)
            # desenha modais em ordem
            for modal in cls._modals:
                modal.draw(cls.TELA)
            pygame.display.flip()

    @classmethod
    def push_modal(cls, modal):
        cls._modals.append(modal)

    @classmethod
    def pop_modal(cls):
        if cls._modals:
            cls._modals.pop()
    
    # --- Métodos para usar ViewRenderer como Hub (opcional) ---
    @classmethod
    def habilitar_view_hub(cls):
        """
        Habilita o uso do ViewRenderer como Hub/Facade.
        Quando habilitado, usa ViewRenderer para gerenciar screens.
        """
        cls._usar_view_hub = True
        from View.ViewRenderer import ViewRenderer
        ViewRenderer.inicializar()
        print("[ScreenManager] ViewRenderer Hub habilitado")
    
    @classmethod
    def usar_view_hub(cls) -> bool:
        """Retorna se está usando ViewRenderer como Hub."""
        return cls._usar_view_hub
