# View/UIRenderer.py

import pygame

class UIRenderer:
    @staticmethod
    def desenhar_botao(surface, rect, cor, texto, fonte, cor_texto=(255, 255, 255)):
        """
        Desenha um botão simples com fundo e texto centralizado.

        Args:
            surface (pygame.Surface): superfície onde desenhar
            rect (pygame.Rect): retângulo do botão
            cor (tuple): cor de fundo (R, G, B)
            texto (str): texto do botão
            fonte (pygame.font.Font): fonte do texto
            cor_texto (tuple): cor do texto (R, G, B)
        """
        # Desenha fundo
        pygame.draw.rect(surface, cor, rect)

        # Renderiza texto centralizado
        texto_surface = fonte.render(texto, True, cor_texto)
        surface.blit(texto_surface, texto_surface.get_rect(center=rect.center))
