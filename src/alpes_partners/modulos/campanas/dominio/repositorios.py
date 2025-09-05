"""
Repositorios para el dominio de campañas.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entidades import Campaña


class RepositorioCampanas(ABC):
    """Repositorio abstracto para campañas."""
    
    @abstractmethod
    def obtener_por_id(self, campaña_id: str) -> Optional[Campaña]:
        """Obtiene una campaña por su ID."""
        pass
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[Campaña]:
        """Obtiene una campaña por su nombre."""
        pass
    
    @abstractmethod
    def obtener_activas(self) -> List[Campaña]:
        """Obtiene todas las campañas activas."""
        pass
    
    @abstractmethod
    def obtener_por_categoria(self, categoria: str) -> List[Campaña]:
        """Obtiene campañas que incluyan una categoría específica."""
        pass
    
    @abstractmethod
    def obtener_por_influencer_origen(self, influencer_id: str) -> List[Campaña]:
        """Obtiene campañas creadas para un influencer específico."""
        pass
    
    @abstractmethod
    def obtener_todas(self, limite: int = 100, offset: int = 0) -> List[Campaña]:
        """Obtiene todas las campañas con paginación."""
        pass
    
    @abstractmethod
    def agregar(self, campaña: Campaña) -> None:
        """Agrega una nueva campaña."""
        pass
    
    @abstractmethod
    def actualizar(self, campaña: Campaña) -> None:
        """Actualiza una campaña existente."""
        pass
    
    @abstractmethod
    def eliminar(self, campaña_id: str) -> None:
        """Elimina una campaña."""
        pass
    
    @abstractmethod
    def existe_con_nombre(self, nombre: str, excluir_id: Optional[str] = None) -> bool:
        """Verifica si existe una campaña con el nombre dado."""
        pass
