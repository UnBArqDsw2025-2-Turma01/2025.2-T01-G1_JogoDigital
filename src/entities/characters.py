import pygame

class Inimigos:
    def __init__(self, nome: str, hp: int, atk: int, atk_speed: int, speed: int, sprite: pygame.Surface):
        self._nome = nome
        self._hp = hp
        self._atk = atk
        self._atk_speed = atk_speed
        self._speed = speed
        self._sprite = sprite

    def atacar(self):
        pass

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    def receber_dano(self, dano: int):
        self.hp -= dano
        self.hp()

    def mover(self):
        pass


class Heroi:
    def __init__(self, nome: str, hp: int, atk: int, atk_speed: int, sprite: pygame.Surface):
        self._nome = nome
        self._hp = hp
        self._atk = atk
        self._atk_speed = atk_speed
        self._sprite = sprite

    def atacar(self):
        pass

    def receber_dano(self, dano: int):
        self.hp -= dano
        self.hp()

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

class AtributosHeroi:
    def __init__(self, imagem_de_fundo: pygame.Surface, hp: int, atk: int, atk_speed: int, botao_melhorar: pygame.Rect, botao_voltar: pygame.Rect, musica_de_fundo: pygame.mixer.Sound, sprite: pygame.Surface):
        self._imagem_de_fundo = imagem_de_fundo
        self._hp = hp
        self._atk = atk
        self._atk_speed = atk_speed
        self._botao_melhorar = botao_melhorar
        self._botao_voltar = botao_voltar
        self._musica_de_fundo = musica_de_fundo
        self._sprite = sprite

    def apertar_melhorar(self):
        pass

    def apertar_voltar(self):
        pass

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def atk(self):
        return self._atk

    @atk.setter
    def atk(self, value):
        self.atk = value

    @property
    def atk_speed(self):
        return self.atk_speed

    @atk_speed.setter
    def atk_speed(self, value):
        self._atk_speed = value
