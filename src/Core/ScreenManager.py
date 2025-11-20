import pygame
import os
from Template.UIConfigs import *
from Asset.AssetProvider import AssetProvider
from View.ViewRenderer import ViewRenderer
from View.InputHandler import InputHandler

class ScreenManager:
    """
    Gerenciador central de telas, modais e renderização.
    Pode trabalhar tanto com instâncias de Screen diretas
    quanto através do ViewRenderer Hub (padrão Facade).
    """

    # --- superfícies / relógio ---
    TELA = None            # tela VIRTUAL onde as screens desenham
    TELA_REAL = None       # tela REAL (fullscreen/window) do monitor
    RELOGIO = None

    # --- tamanho virtual padrão (usado para escala) ---
    VIRTUAL_W = LARGURA_TELA_JANELA
    VIRTUAL_H = ALTURA_TELA_JANELA

    # --- screens / modais / flags ---
    _telas = {}
    _tela_atual = None
    _tela_atual_nome = None  # nome da tela atual (para ViewRenderer Hub)
    _modals = []  # pilha de modais/overlays
    _usar_view_hub = False  # flag para usar ViewRenderer como Hub

    # --- 1. Inicialização global ---
    @classmethod
    def inicializar_pygame(cls):
        """Inicializa Pygame, fullscreen e tela virtual."""
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"[ScreenManager] Aviso: mixer não inicializado: {e}")

        # carrega e toca música (se houver)
        try:
            song_path = os.path.normpath(os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..', 'Asset', 'songs', 'forest.wav'
            ))
            if os.path.exists(song_path):
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[ScreenManager] Aviso: não foi possível tocar música: {e}")

        if not pygame.font.get_init():
            pygame.font.init()

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        info = pygame.display.Info()

        # Tela real: fullscreen, tamanho do monitor
        cls.TELA_REAL = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.FULLSCREEN
        )

        # Tela virtual onde o jogo realmente desenha (resolução fixa)
        cls.VIRTUAL_W = LARGURA_TELA_JANELA
        cls.VIRTUAL_H = ALTURA_TELA_JANELA
        cls.TELA = pygame.Surface((cls.VIRTUAL_W, cls.VIRTUAL_H))

        pygame.display.set_caption(TITULO_JOGO)
        AssetProvider.carregar_assets()
        cls.RELOGIO = pygame.time.Clock()

        print(f"[ScreenManager] Inicializado: virtual={cls.VIRTUAL_W}x{cls.VIRTUAL_H}, real={info.current_w}x{info.current_h}")

    # --- Getters ---
    @classmethod
    def get_tela(cls):
        """Retorna a tela VIRTUAL, onde o jogo deve desenhar."""
        return cls.TELA

    @classmethod
    def get_relogio(cls):
        return cls.RELOGIO

    # --- Sistema de Screens via Hub ---
    @classmethod
    def registrar_screens_via_hub(cls, screen_names):
        """
        Registra screens via ViewRenderer Hub.
        ViewRenderer criará as instâncias via lazy loading.
        Também registra handlers de input para cada screen no InputHandler.
        """
        cls._usar_view_hub = True

        for name in screen_names:
            screen = ViewRenderer.get_screen(name)
            if screen:
                cls._telas[name] = screen
                cls._registrar_handler_input_screen(name, screen)

        print(f"[ScreenManager] Screens registradas via ViewRenderer Hub: {screen_names}")
        print(f"[ScreenManager] Handlers de input registrados no InputHandler")

    @classmethod
    def _registrar_handler_input_screen(cls, screen_name: str, screen):
        """Registra handler de input para uma screen no InputHandler Hub."""
        def screen_handler(event):
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
        """Troca a tela atual (usado quando ScreenManager gerencia screens diretamente)."""
        # Se estiver usando Hub e tela não foi carregada, busca no ViewRenderer
        if cls._usar_view_hub and nome_tela not in cls._telas:
            screen = ViewRenderer.get_screen(nome_tela)
            if screen:
                cls._telas[nome_tela] = screen

        if nome_tela in cls._telas:
            cls._tela_atual = cls._telas[nome_tela]
            cls._tela_atual_nome = nome_tela

            # Se estiver usando ViewRenderer Hub, notifica
            if cls._usar_view_hub:
                # tenta também instruir o ViewRenderer (se aplicável)
                try:
                    ViewRenderer.transition_to(nome_tela)
                except Exception:
                    try:
                        ViewRenderer.set_current_screen(nome_tela)
                    except Exception:
                        pass
        else:
            print(f"[ScreenManager] ERRO: Screen '{nome_tela}' não encontrada")

    @classmethod
    def get_tela_atual(cls):
        return cls._tela_atual

    # --- Input / eventos / update ---
    @classmethod
    def handle_events(cls):
        """
        Processa eventos através do InputHandler Hub.
        O InputHandler já captura pygame.event.get() e distribui para handlers registrados.
        """
        continuar = InputHandler.processar_eventos(screen_name=cls._tela_atual_nome)
        return continuar

    @classmethod
    def update(cls):
        # atualiza tela base apenas se não houver modal que bloqueie
        if cls._tela_atual:
            if not cls._modals:
                cls._tela_atual.update()
            else:
                top = cls._modals[-1]
                if hasattr(top, 'update'):
                    top.update()
        else:
            # Se não há _tela_atual local, delega ao ViewRenderer (quando usado como hub)
            if cls._usar_view_hub:
                ViewRenderer.update()

    # --- Renderização com LETTERBOX (fullscreen proporcional) ---
    @classmethod
    def draw(cls):
        """
        Renderiza a tela virtual (TELA) usando:
         - Se ScreenManager gerencia a screen diretamente: usa cls._tela_atual.draw(cls.TELA)
         - Se estiver usando ViewRenderer (hub) OU cls._tela_atual for None: usa ViewRenderer.render(cls.TELA)
        Depois escala a TELA para TELA_REAL com letterbox/pillarbox.
        """

        # Garantia de superfícies
        if cls.TELA is None or cls.TELA_REAL is None:
            print("[ScreenManager] Aviso: superfícies não inicializadas.")
            return

        # Limpa a tela virtual antes de desenhar (evita resíduos)
        cls.TELA.fill((0, 0, 0))

        # 1) Desenhar fonte de verdade na tela virtual
        if cls._tela_atual:
            # ScreenManager está gerenciando diretamente uma screen
            try:
                cls._tela_atual.draw(cls.TELA)
            except Exception as e:
                print(f"[ScreenManager] Erro ao desenhar _tela_atual: {e}")
        else:
            # Se estamos usando ViewRenderer como hub, ou não temos tela local,
            # delegamos a renderização ao ViewRenderer (ele desenha na surface passada).
            try:
                ViewRenderer.render(cls.TELA)
            except Exception as e:
                # último recurso: imprimir erro mas não falhar o draw
                print(f"[ScreenManager] Erro ao delegar render para ViewRenderer: {e}")

        # 2) Caso existam modais gerenciados pelo ScreenManager (eles devem ter sido desenhados
        #    pela chamada acima se ViewRenderer.render já aponta para ScreenManager._modals).
        #    Mas, para garantir, desenhamos quaisquer modais restantes diretamente na virtual:
        for modal in cls._modals:
            try:
                modal.draw(cls.TELA)
            except Exception:
                pass

        # 3) Escala proporcional (letterbox) da virtual para a tela real
        real = cls.TELA_REAL
        virtual = cls.TELA

        sw, sh = real.get_size()
        vw, vh = cls.VIRTUAL_W, cls.VIRTUAL_H

        # Proteção contra divisão por zero
        if vw == 0 or vh == 0:
            print("[ScreenManager] Aviso: virtual size inválida.")
            return

        scale = min(sw / vw, sh / vh)
        new_w = int(vw * scale)
        new_h = int(vh * scale)

        # Redimensiona (upscale/downscale) a tela virtual
        try:
            scaled = pygame.transform.scale(virtual, (new_w, new_h))
        except Exception as e:
            print(f"[ScreenManager] Erro ao escalonar virtual: {e}")
            return

        # Preenche fundo preto (bordas)
        real.fill((0, 0, 0))

        # Centraliza e blita
        x = (sw - new_w) // 2
        y = (sh - new_h) // 2
        real.blit(scaled, (x, y))

        # Atualiza o display
        pygame.display.flip()

    # --- Modais ---
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
        try:
            ViewRenderer.inicializar()
        except Exception:
            pass
        print("[ScreenManager] ViewRenderer Hub habilitado")

    @classmethod
    def usar_view_hub(cls) -> bool:
        """Retorna se está usando ViewRenderer como Hub."""
        return cls._usar_view_hub
