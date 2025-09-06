import logging
from typing import List, Optional

from ....seedwork.aplicacion.handlers import ManejadorComando
from ....seedwork.infraestructura.uow import UnidadTrabajo
from ..dominio.repositorios import RepositorioInfluencers
from ..dominio.entidades import Influencer
from ..dominio.excepciones import EmailYaRegistrado

from .comandos.registrar_influencer import RegistrarInfluencer

logger = logging.getLogger(__name__)


# ============= COMMAND HANDLERS =============

class ManejadorRegistrarInfluencer(ManejadorComando[RegistrarInfluencer]):
    """Handler para registrar un influencer."""
    
    def __init__(self, repositorio: RepositorioInfluencers, uow: UnidadTrabajo):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: RegistrarInfluencer) -> None:
        logger.info(f"🎯 HANDLER: Iniciando registro de influencer - Email: {comando.email}")
        
        # Verificar si el email ya existe
        logger.info(f"🔍 HANDLER: Verificando si email existe: {comando.email}")
        if self.repositorio.existe_email(comando.email):
            logger.warning(f"⚠️ HANDLER: Email ya registrado: {comando.email}")
            raise EmailYaRegistrado(f"Ya existe un influencer con el email {comando.email}")
        
        logger.info(f"✅ HANDLER: Email disponible: {comando.email}")
        
        # Crear entidad influencer
        logger.info(f"🔄 HANDLER: Creando entidad influencer...")
        influencer = Influencer.crear(
            nombre=comando.nombre,
            email=comando.email,
            categorias=comando.categorias,
            descripcion=comando.descripcion,
            biografia=comando.biografia,
            sitio_web=comando.sitio_web,
            telefono=comando.telefono
        )
        
        logger.info(f"✅ HANDLER: Influencer creado - ID: {influencer.id}, Eventos: {len(influencer.eventos)}")
        
        # Agregar al repositorio usando UoW
        logger.info(f"🔄 HANDLER: Registrando operación en UoW...")
        self.uow.registrar_batch(self.repositorio.agregar, influencer)
        logger.info(f"✅ HANDLER: Operación registrada en UoW")
        
        # Los eventos se publican automáticamente por la UoW
        # Limpiar eventos después del registro
        influencer.limpiar_eventos()
        
        logger.info(f"✅ HANDLER: Handler completado - Influencer ID: {influencer.id}")


logger.info("🔧 HANDLERS: Handlers de aplicación de influencers cargados")