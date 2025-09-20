import pygame

class PaginaInicial:
    def __init__(self, titulo_jogo: pygame.Surface, imagem_de_fundo: pygame.Surface, botao_jogar: pygame.Rect, botao_loja: pygame.Rect, botao_configuracoes: pygame.Rect, botao_creditos: pygame.Rect, botao_sair: pygame.Rect, musica_de_fundo: pygame.mixer.Sound, versao_jogo: str):
        self._titulo_jogo = titulo_jogo
        self._imagem_de_fundo = imagem_de_fundo
        self._botao_jogar = botao_jogar
        self._botao_loja = botao_loja
        self._botao_configuracoes = botao_configuracoes
        self._botao_creditos = botao_creditos
        self._botao_sair = botao_sair
        self._musica_de_fundo = musica_de_fundo
        self._versao_jogo = versao_jogo

    def apertar_jogar(self):
        pass

    def apertar_loja(self):
        pass

    def apertar_configuracoes(self):
        pass

class PaginaJogar:
    def __init__(self, imagem_de_fundo: pygame.Surface, botao_voltar: pygame.Rect, mapas: pygame.Rect, botao_selecionar: pygame.Rect, musica_de_fundo: pygame.mixer.Sound):
        self._imagem_de_fundo = imagem_de_fundo
        self._botao_voltar = botao_voltar
        self._mapas = mapas
        self._botao_selecionar = botao_selecionar
        self._musica_de_fundo = musica_de_fundo

    def apertar_voltar(self):
        pass

    def apertar_mapa(self):
        pass

    def apertar_selecionar(self):
        pass

class PaginaLoja:
    def __init__(self, imagem_de_fundo: pygame.Surface, catalogo: list, botao_comprar: pygame.Rect, botao_voltar: pygame.Rect, musica_de_fundo: pygame.mixer.Sound, coin: int):
        self._imagem_de_fundo = imagem_de_fundo
        self._catalogo = catalogo
        self._botao_comprar = botao_comprar
        self._botao_voltar = botao_voltar
        self._musica_de_fundo = musica_de_fundo
        self._coin = coin

    def mostrar_catalogo(self):
        pass

    def atualizar_catalogo(self):
        pass

    def apertar_comprar(self):
        pass

class PaginaConfiguracoes:
    def __init__(self, imagem_de_fundo: pygame.Surface, botao_musica: pygame.Rect, botao_efeitos_sonoros: pygame.Rect, botao_idioma: pygame.Rect, botao_salvar: pygame.Rect, botao_voltar: pygame.Rect, musica_de_fundo: pygame.mixer.Sound):
        self._imagem_de_fundo = imagem_de_fundo
        self._botao_musica = botao_musica
        self._botao_efeitos_sonoros = botao_efeitos_sonoros
        self._botao_idioma = botao_idioma
        self._botao_salvar = botao_salvar
        self._botao_voltar = botao_voltar
        self._musica_de_fundo = musica_de_fundo

    def apertar_musica(self):
        pass

    def apertar_efeitos_sonoros(self):
        pass

    def apertar_idioma(self):
        pass

    def apertar_salvar(self):
        pass

    def apertar_voltar(self):
        pass

class PaginaPartida:
    def __init__(self, imagem_de_fundo: pygame.Surface, botao_configuracao: pygame.Rect, botao_heroi: pygame.Rect, botao_rodada: pygame.Rect, botao_nivel: pygame.Rect, musica_de_fundo: pygame.mixer.Sound, quantidade_guarana: int, recompensas: int):
        self._imagem_de_fundo = imagem_de_fundo
        self._botao_configuracao = botao_configuracao
        self._botao_heroi = botao_heroi
        self._botao_rodada = botao_rodada
        self._botao_nivel = botao_nivel
        self._musica_de_fundo = musica_de_fundo
        self._quantidade_guarana = quantidade_guarana
        self._recompensas = recompensas

    @property
    def quantidade_guarana(self):
        return self._quantidade_guarana

    @quantidade_guarana.setter
    def quantidade_guarana(self, value):
        self._quantidade_guarana = value

    def apertar_configuracao(self):
        pass

    def apertar_heroi(self):
        pass

    def apertar_rodada(self):
        pass

    def apertar_nivel(self):
        pass

    def coletar_guarana(self):
        pass

    def gerar_inimigo(self):
        pass

    def atualizar_coins(self):
        pass

    def atualizar_map_lib(self):
        pass