import pygame
from Core.ScreenManager import ScreenManager


# classe obsoleta, mas mantida por compatibilidade
class EventManager:
    @staticmethod
    def processar_eventos():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # pra sair do jogo
            else:
                # o event manager apenas encaminha os eventos
                # e as respectivas telas lidam com eles
                tela = ScreenManager.get_tela_atual()
                if tela:
                    tela.handle_event(event)
        return True
