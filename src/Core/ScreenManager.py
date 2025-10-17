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
        ✅ RECOMENDADO: Registra screens via ViewRenderer Hub.
        ViewRenderer criará as instâncias via lazy loading.
        
        Args:
            screen_names: Lista de nomes de screens ['menu', 'jogo']
        """
        from View.ViewRenderer import ViewRenderer
        cls._usar_view_hub = True
        
        # Pré-carrega screens no Hub (opcional, lazy loading é automático)
        for name in screen_names:
            screen = ViewRenderer.get_screen(name)
            if screen:
                cls._telas[name] = screen
        
        print(f"[ScreenManager] ✅ Screens registradas via ViewRenderer Hub: {screen_names}")

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
            print(f"[ScreenManager] ⚠️ ERRO: Screen '{nome_tela}' não encontrada")

    @classmethod
    def get_tela_atual(cls):
        return cls._tela_atual

    @classmethod
    def handle_events(cls):
        """Encaminha eventos para a tela atual."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Eventos vão primeiro para o modal no topo (se houver)
            if cls._modals:
                top = cls._modals[-1]
                res = top.handle_event(event)
                # se modal indicar fechar com 'close', desempilha
                if res == 'close':
                    cls.pop_modal()
                continue
            if cls._tela_atual:
                cls._tela_atual.handle_event(event)
        return True

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
