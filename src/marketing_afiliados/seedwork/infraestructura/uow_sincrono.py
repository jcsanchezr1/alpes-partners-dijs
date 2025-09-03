from typing import List
from sqlalchemy.orm import Session
import logging
from ..dominio.eventos import EventoDominio

logger = logging.getLogger(__name__)


class UnidadDeTrabajoSincrona:
    """Implementación síncrona y simple de la Unidad de Trabajo."""
    
    def __init__(self, session: Session):
        self.session = session
        self._eventos: List[EventoDominio] = []
    
    def __enter__(self):
        """Inicia la transacción."""
        logger.info("🚀 UOW: Iniciando transacción")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Finaliza la transacción."""
        if exc_type is None:
            logger.info("✅ UOW: Transacción exitosa, ejecutando commit")
            self.commit()
        else:
            logger.error(f"❌ UOW: Error en transacción: {exc_type.__name__}: {exc_val}")
            self.rollback()
    
    def commit(self) -> None:
        """Confirma la transacción."""
        try:
            logger.info("🔄 UOW: Verificando objetos en sesión antes del commit")
            logger.info(f"🔄 UOW: Objetos nuevos: {len(self.session.new)}")
            logger.info(f"🔄 UOW: Objetos modificados: {len(self.session.dirty)}")
            logger.info(f"🔄 UOW: Objetos eliminados: {len(self.session.deleted)}")
            
            for obj in self.session.new:
                logger.info(f"🔄 UOW: Objeto nuevo: {type(obj).__name__} - ID: {getattr(obj, 'id', 'N/A')}")
            
            logger.info("🔄 UOW: Ejecutando commit...")
            self.session.commit()
            logger.info("✅ UOW: Commit ejecutado exitosamente")
            
            # Los eventos se podrían publicar aquí si tuviéramos un despachador
            # Por ahora solo los limpiamos
            self._eventos.clear()
            logger.info("✅ UOW: Eventos limpiados")
            
        except Exception as e:
            logger.error(f"❌ UOW: Error durante commit: {e}")
            self.rollback()
            raise
    
    def rollback(self) -> None:
        """Revierte la transacción."""
        logger.warning("🔄 UOW: Ejecutando rollback...")
        self.session.rollback()
        self._eventos.clear()
        logger.warning("⚠️ UOW: Rollback completado")
    
    def agregar_eventos(self, eventos: List[EventoDominio]):
        """Agrega eventos para ser publicados."""
        self._eventos.extend(eventos)
    
    @property
    def eventos(self) -> List[EventoDominio]:
        """Obtiene los eventos pendientes."""
        return self._eventos.copy()
