from typing import List
from ..dominio.eventos import EventoDominio
from .uow import UnidadDeTrabajo


class UnidadDeTrabajoMemoria(UnidadDeTrabajo):
    """Implementación en memoria de la Unidad de Trabajo."""
    
    def __init__(self):
        self._eventos: List[EventoDominio] = []
        self._en_transaccion = False
    
    async def __aenter__(self):
        """Inicia la transacción."""
        self._en_transaccion = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Finaliza la transacción."""
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
    
    async def commit(self) -> None:
        """Confirma la transacción."""
        # En una implementación real, aquí se confirmarían los cambios en la base de datos
        # y se publicarían los eventos
        self._en_transaccion = False
        # Los eventos se podrían publicar aquí si tuviéramos un despachador
        # Por ahora solo los limpiamos
        self._eventos.clear()
    
    async def rollback(self) -> None:
        """Revierte la transacción."""
        # En una implementación real, aquí se revertirían los cambios
        self._eventos.clear()
        self._en_transaccion = False
    
    def agregar_eventos(self, eventos: List[EventoDominio]):
        """Agrega eventos para ser publicados."""
        self._eventos.extend(eventos)
    
    @property
    def eventos(self) -> List[EventoDominio]:
        """Obtiene los eventos pendientes."""
        return self._eventos.copy()
