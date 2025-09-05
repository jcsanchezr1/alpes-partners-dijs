"""
Unidad de Trabajo para el módulo de Campañas.
Siguiendo el mismo patrón simple que influencers.
"""

import logging
logger = logging.getLogger(__name__)

logger.info("🔍 UoW CAMPAÑAS: Iniciando imports de UoW...")

try:
    logger.info("🔍 UoW CAMPAÑAS: Importando UnidadTrabajo del seedwork...")
    from alpes_partners.seedwork.infraestructura.uow import UnidadTrabajo
    logger.info("✅ UoW CAMPAÑAS: UnidadTrabajo importada exitosamente")
except Exception as e:
    logger.error(f"❌ UoW CAMPAÑAS: Error importando UnidadTrabajo: {e}")
    import traceback
    logger.error(f"❌ UoW CAMPAÑAS: Traceback:\n{traceback.format_exc()}")
    raise

try:
    logger.info("🔍 UoW CAMPAÑAS: Importando repositorios...")
    from .repositorios import RepositorioCampanasSQLAlchemy
    logger.info("✅ UoW CAMPAÑAS: Repositorios importados exitosamente")
except Exception as e:
    logger.error(f"❌ UoW CAMPAÑAS: Error importando repositorios: {e}")
    import traceback
    logger.error(f"❌ UoW CAMPAÑAS: Traceback:\n{traceback.format_exc()}")
    raise

logger.info("🎉 UoW CAMPAÑAS: Todos los imports de UoW completados exitosamente")


class UnidadTrabajoCampanas(UnidadTrabajo):
    """
    Unidad de Trabajo específica para el módulo de Campañas.
    Maneja transacciones y repositorios del contexto de campañas.
    """
    
    def __init__(self, session):
        self.session = session
        self._repositorio_campanas = None
        self._batches = []
        self._savepoints = []
    
    def __enter__(self):
        """Entrada del context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Salida del context manager - hace commit automático si no hay errores."""
        if exc_type is None:
            # No hubo excepción, hacer commit
            logger.info("💾 CAMPAÑAS: Haciendo commit automático de la transacción")
            self.commit()
        else:
            # Hubo excepción, hacer rollback
            logger.error(f"❌ CAMPAÑAS: Error en transacción, haciendo rollback: {exc_val}")
            self.rollback()
        return False  # No suprimir la excepción
    
    @property
    def repositorio_campanas(self):
        if self._repositorio_campanas is None:
            self._repositorio_campanas = RepositorioCampanasSQLAlchemy(self.session)
        return self._repositorio_campanas
    
    @property
    def batches(self):
        return self._batches
    
    @property 
    def savepoints(self):
        return self._savepoints
    
    def _limpiar_batches(self):
        self._batches = []
    
    def commit(self):
        """Confirma la transacción."""
        try:
            logger.info(f"💾 CAMPAÑAS: Iniciando commit - {len(self._batches)} batches pendientes")
            
            # Ejecutar batches pendientes
            for i, batch in enumerate(self._batches):
                logger.info(f"💾 CAMPAÑAS: Ejecutando batch {i+1}: {batch.operacion.__name__}")
                batch.operacion(*batch.args, **batch.kwargs)
            
            # Confirmar en base de datos
            logger.info("💾 CAMPAÑAS: Ejecutando session.commit() en base de datos")
            self.session.commit()
            logger.info("✅ CAMPAÑAS: Transacción confirmada exitosamente en base de datos")
            
            # Publicar eventos post-commit
            super().commit()
            
            # Limpiar batches
            self._limpiar_batches()
            
        except Exception as e:
            logger.error(f"❌ CAMPAÑAS: Error en commit: {e}")
            self.rollback()
            raise e
    
    def rollback(self, savepoint=None):
        """Revierte la transacción."""
        if savepoint:
            self.session.rollback_to_savepoint(savepoint)
        else:
            self.session.rollback()
        self._limpiar_batches()
    
    def savepoint(self):
        """Crea un savepoint."""
        savepoint = self.session.begin_nested()
        self._savepoints.append(savepoint)
        return savepoint
