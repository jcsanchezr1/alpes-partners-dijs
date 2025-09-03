from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..dominio.eventos import EventoDominio


class UnidadDeTrabajo(ABC):
    """Interfaz para Unit of Work."""
    
    @abstractmethod
    async def __aenter__(self):
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Confirma los cambios y despacha eventos."""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Revierte los cambios."""
        pass


class UnidadDeTrabajoSQLAlchemy(UnidadDeTrabajo):
    """Implementación de Unit of Work con SQLAlchemy."""
    
    def __init__(self, session: AsyncSession, despachador_eventos=None):
        self.session = session
        self.despachador_eventos = despachador_eventos
        self._eventos: List[EventoDominio] = []
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
    
    async def commit(self) -> None:
        """Confirma los cambios y despacha eventos."""
        try:
            await self.session.commit()
            # Despachar eventos después del commit exitoso
            if self.despachador_eventos:
                for evento in self._eventos:
                    await self.despachador_eventos.despachar(evento)
            self._eventos.clear()
        except Exception:
            await self.rollback()
            raise
    
    async def rollback(self) -> None:
        """Revierte los cambios."""
        await self.session.rollback()
        self._eventos.clear()
    
    def agregar_eventos(self, eventos: List[EventoDominio]) -> None:
        """Agrega eventos para ser despachados."""
        self._eventos.extend(eventos)
