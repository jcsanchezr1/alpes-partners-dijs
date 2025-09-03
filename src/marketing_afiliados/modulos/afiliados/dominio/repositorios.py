from abc import abstractmethod
from typing import List, Optional
from ...seedwork.dominio.repositorios import Repositorio
from .entidades import Afiliado
from .objetos_valor import TipoAfiliado, EstadoAfiliado


class RepositorioAfiliados(Repositorio[Afiliado]):
    """Repositorio para afiliados."""
    
    @abstractmethod
    async def obtener_por_email(self, email: str) -> Optional[Afiliado]:
        """Obtiene un afiliado por su email."""
        pass
    
    @abstractmethod
    async def obtener_por_estado(self, estado: EstadoAfiliado) -> List[Afiliado]:
        """Obtiene afiliados por estado."""
        pass
    
    @abstractmethod
    async def obtener_por_tipo(self, tipo: TipoAfiliado) -> List[Afiliado]:
        """Obtiene afiliados por tipo."""
        pass
    
    @abstractmethod
    async def obtener_por_categoria(self, categoria: str) -> List[Afiliado]:
        """Obtiene afiliados que manejan una categoría específica."""
        pass
    
    @abstractmethod
    async def buscar_por_nombre(self, nombre: str) -> List[Afiliado]:
        """Busca afiliados por nombre (búsqueda parcial)."""
        pass
    
    @abstractmethod
    async def existe_email(self, email: str) -> bool:
        """Verifica si existe un afiliado con el email dado."""
        pass
