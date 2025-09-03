from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

from .entidades import AgregadoRaiz

T = TypeVar('T', bound=AgregadoRaiz)


class Repositorio(ABC, Generic[T]):
    """Interfaz base para repositorios."""
    
    @abstractmethod
    async def obtener_por_id(self, id: str) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        pass
    
    @abstractmethod
    async def agregar(self, entidad: T) -> None:
        """Agrega una nueva entidad."""
        pass
    
    @abstractmethod
    async def actualizar(self, entidad: T) -> None:
        """Actualiza una entidad existente."""
        pass
    
    @abstractmethod
    async def eliminar(self, entidad: T) -> None:
        """Elimina una entidad."""
        pass
    
    @abstractmethod
    async def obtener_todos(self) -> List[T]:
        """Obtiene todas las entidades."""
        pass
