from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from .comandos import Comando
from .queries import Query, ResultadoQuery

C = TypeVar('C', bound=Comando)
Q = TypeVar('Q', bound=Query)


class ManejadorComando(ABC, Generic[C]):
    """Interfaz para manejadores de comandos."""
    
    @abstractmethod
    async def handle(self, comando: C) -> None:
        """Maneja un comando."""
        pass


class ManejadorQuery(ABC, Generic[Q]):
    """Interfaz para manejadores de queries."""
    
    @abstractmethod
    async def handle(self, query: Q) -> ResultadoQuery:
        """Maneja una query."""
        pass
