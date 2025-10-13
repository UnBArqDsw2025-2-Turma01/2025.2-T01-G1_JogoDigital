# Core/EventManager.py

import pygame
from View.InputHandler import InputHandler

class EventManager:
    @classmethod
    def processar_eventos(cls, state_vars):
        """Processa todos os eventos do Pygame."""
        rodando = True
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # Passa o evento para o InputHandler processar
            state_vars = InputHandler.handle_event(evento, state_vars)
                
        return rodando, state_vars