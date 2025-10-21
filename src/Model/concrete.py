import pygame
from typing import TypeVar
from .interfaces import IIterator, IIterableCollection

# Define que 'T' deve ser sempre um tipo de Sprite
T = TypeVar('T', bound=pygame.sprite.Sprite)


class SpriteGroupIterator(IIterator[T]):
    
    def __init__(self, group: pygame.sprite.Group):
        # No exato momento da criação do iterador é tirado um "snapshot" 
        # (Uma cópia da lista que iterador irá percorrer)
        self._snapshot: list[T] = group.sprites()
        self._count: int = len(self._snapshot)
        self._position: int = 0

    def getNext(self) -> T:
        # Pega o próximo elemento da iteração se houver
        if self.hasMore():
            sprite = self._snapshot[self._position]
            self._position += 1
            return sprite
        else:
            raise StopIteration("Não há mais elementos na iteração.")

    def hasMore(self) -> bool:
        # Verifica se há mais elementos para iterar
        return self._position < self._count

    def getPosition(self) -> int:
        # Retorna a posição atual do iterador
        return self._position

    def restart(self):
        # Reinicia o iterador, voltando para a primeira posição do snapshot
        self._position = 0



class IterableSpriteGroup(IIterableCollection[T]):
    # Essa classe age como um adaptador para pygame.sprite.Group
    
    def __init__(self, group: pygame.sprite.Group):
        self._group = group

    def createIterator(self) -> IIterator[T]:
        # Cria um novo iterador, que vai tirar um novo snapshot
        return SpriteGroupIterator[T](self._group)
    
    def get_raw_group(self) -> pygame.sprite.Group:
        # Método auxiliar para acessar o grupo original, se necessário
        return self._group