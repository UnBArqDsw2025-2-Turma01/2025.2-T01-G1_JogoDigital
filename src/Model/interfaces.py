from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IIterator(ABC, Generic[T]):
    """
    Declara as operações necessárias para percorrer uma coleção.
    """
    
    @abstractmethod
    def getNext(self) -> T:
        """
        Pega o próximo elemento da iteração.
        """
        pass

    @abstractmethod
    def hasMore(self) -> bool:
        """
        Verifica se ainda há elementos para percorrer.
        """
        pass

    @abstractmethod
    def getPosition(self) -> int:
        """
        Retorna o índice ou posição atual do iterador.
        """
        pass

    @abstractmethod
    def restart(self):
        """
        Reinicia o iterador, voltando para a primeira posição.
        """
        pass


class IIterableCollection(ABC, Generic[T]):
    """
    Declara um ou mais métodos para obter iteradores.
    """
    
    @abstractmethod
    def createIterator(self) -> IIterator[T]:
        """
        Retorna uma nova instância de um iterador compatível.
        """
        pass