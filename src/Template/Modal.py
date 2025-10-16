import pygame


class Modal:
    """Base simples para modais/overlays.

    Subclasse deve implementar handle_event(event), draw(surface) e opcionalmente update().
    blocks_update: se True, bloqueia a atualização (update) da tela de baixo.
    """

    def __init__(self, blocks_update=True):
        self.blocks_update = blocks_update

    def handle_event(self, event):
        """Recebe um evento pygame. Pode consumir ou ignorar."""
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass
