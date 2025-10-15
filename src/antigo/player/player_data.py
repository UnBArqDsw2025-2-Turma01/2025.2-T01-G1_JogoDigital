import pygame

class DadosJogador:
    def __init__(self, coin: int, linguagem: str, mapas_liberados: list[str], volume_musica: int, volume_sonoro: int, herois_liberados: list[str]):
        self._coin = coin
        self._linguagem = linguagem
        self._mapas_liberados = mapas_liberados
        self._volume_musica = volume_musica
        self._volume_sonoro = volume_sonoro
        self._herois_liberados = herois_liberados

    @property
    def coin(self):
        return self._coin

    @coin.setter
    def coin(self, value):
        self._coin = value

    @property
    def linguagem(self):
        return self._linguagem

    @linguagem.setter
    def linguagem(self, value):
        self._linguagem = value

    @property
    def mapas_liberados(self):
        return self._mapas_liberados

    @mapas_liberados.setter
    def mapas_liberados(self, value):
        self._mapas_liberados = value

    @property
    def volume_musica(self):
        return self._volume_musica

    @volume_musica.setter
    def volume_musica(self, value):
        self._volume_musica = value

    @property
    def volume_sonoro(self):
        return self._volume_sonoro

    @volume_sonoro.setter
    def volume_sonoro(self, value):
        self._volume_sonoro = value

    @property
    def herois_liberados(self):
        return self._herois_liberados

    @herois_liberados.setter
    def herois_liberados(self, value):
        self._herois_liberados = value

