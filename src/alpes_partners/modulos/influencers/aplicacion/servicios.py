from typing import List, Optional
import logging

# Servicio de aplicación sin clase base
from ..dominio.entidades import Influencer
from ..dominio.repositorios import RepositorioInfluencers
from ..dominio.excepciones import InfluencerNoEncontrado, EmailYaRegistrado
from ..dominio.objetos_valor import EstadoInfluencer, TipoInfluencer, Plataforma
from ..infraestructura.repositorio_sqlalchemy import RepositorioInfluencersSQLAlchemy
# Importaciones usando el path correcto para el contexto de ejecución
import sys
import os

# Agregar el directorio src al path si no está
src_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from alpes_partners.seedwork.infraestructura.uow_sincrono import UnidadDeTrabajoSincrona

from .dto import InfluencerDTO, RegistrarInfluencerDTO
from typing import Union

logger = logging.getLogger(__name__)


class ServicioInfluencer:
    """Servicio de aplicación para operaciones de influencers."""
    
    def __init__(self, repositorio: RepositorioInfluencers, uow: UnidadDeTrabajoSincrona):
        self._repositorio = repositorio
        self._uow = uow
    
    @property
    def repositorio(self):
        return self._repositorio
    
    @property
    def uow(self):
        return self._uow
    
    def registrar_influencer(self, datos) -> str:
        """Registra un nuevo influencer."""
        logger.info(f"🚀 SERVICIO: Iniciando registro de influencer - Email: {datos.email}")
        
        # Verificar si el email ya existe
        if self.repositorio.existe_email(datos.email):
            logger.warning(f"⚠️ SERVICIO: Email ya registrado: {datos.email}")
            raise EmailYaRegistrado(f"Ya existe un influencer con el email {datos.email}")
        
        # Crear entidad influencer
        influencer = Influencer.crear(
            nombre=datos.nombre,
            email=datos.email,
            categorias=datos.categorias,
            descripcion=datos.descripcion,
            biografia=datos.biografia,
            sitio_web=datos.sitio_web,
            telefono=datos.telefono
        )
        
        logger.info(f"✅ SERVICIO: Influencer creado - ID: {influencer.id}")
        
        # Usar transacción
        with self.uow:
            self.repositorio.agregar(influencer)
            self.uow.agregar_eventos(influencer.eventos)
            influencer.limpiar_eventos()
        
        logger.info(f"✅ SERVICIO: Influencer registrado exitosamente - ID: {influencer.id}")
        return influencer.id
    
    def crear_influencer_desde_dto(self, datos) -> Influencer:
        """Crea una entidad Influencer desde un DTO sin persistirla."""
        logger.info(f"🏭 SERVICIO: Creando influencer desde DTO - Email: {datos.email}")
        
        # Verificar si el email ya existe
        if self.repositorio.existe_email(datos.email):
            logger.warning(f"⚠️ SERVICIO: Email ya registrado: {datos.email}")
            raise EmailYaRegistrado(f"Ya existe un influencer con el email {datos.email}")
        
        # Crear entidad influencer
        influencer = Influencer.crear(
            nombre=datos.nombre,
            email=datos.email,
            categorias=datos.categorias,
            descripcion=datos.descripcion,
            biografia=datos.biografia,
            sitio_web=datos.sitio_web,
            telefono=datos.telefono
        )
        
        logger.info(f"✅ SERVICIO: Influencer creado desde DTO - ID: {influencer.id}")
        return influencer
    
    def obtener_influencer_por_id(self, influencer_id: str) -> Optional[InfluencerDTO]:
        """Obtiene un influencer por ID."""
        logger.info(f"🔍 SERVICIO: Obteniendo influencer - ID: {influencer_id}")
        
        influencer = self.repositorio.obtener_por_id(influencer_id)
        if not influencer:
            logger.info(f"❌ SERVICIO: Influencer no encontrado: {influencer_id}")
            raise InfluencerNoEncontrado(f"Influencer con ID {influencer_id} no encontrado")
        
        logger.info(f"✅ SERVICIO: Influencer encontrado: {influencer.nombre}")
        return self._convertir_a_dto(influencer)
    
    def obtener_influencer_por_email(self, email: str) -> Optional[InfluencerDTO]:
        """Obtiene un influencer por email."""
        logger.info(f"🔍 SERVICIO: Obteniendo influencer - Email: {email}")
        
        influencer = self.repositorio.obtener_por_email(email)
        if not influencer:
            logger.info(f"❌ SERVICIO: Influencer no encontrado con email: {email}")
            raise InfluencerNoEncontrado(f"Influencer con email {email} no encontrado")
        
        logger.info(f"✅ SERVICIO: Influencer encontrado: {influencer.nombre}")
        return self._convertir_a_dto(influencer)
    
    def listar_influencers(
        self,
        estado: Optional[EstadoInfluencer] = None,
        tipo: Optional[TipoInfluencer] = None,
        categoria: Optional[str] = None,
        plataforma: Optional[Plataforma] = None,
        min_seguidores: Optional[int] = None,
        max_seguidores: Optional[int] = None,
        engagement_minimo: Optional[float] = None,
        limite: int = 100,
        offset: int = 0
    ) -> List[InfluencerDTO]:
        """Lista influencers con filtros opcionales."""
        logger.info("🔍 SERVICIO: Obteniendo lista de influencers con filtros")
        
        influencers = self.repositorio.obtener_con_filtros(
            estado=estado,
            tipo=tipo,
            categoria=categoria,
            plataforma=plataforma,
            min_seguidores=min_seguidores,
            max_seguidores=max_seguidores,
            engagement_minimo=engagement_minimo,
            limite=limite,
            offset=offset
        )
        
        logger.info(f"✅ SERVICIO: {len(influencers)} influencers encontrados")
        return [self._convertir_a_dto(influencer) for influencer in influencers]
    
    def _convertir_a_dto(self, influencer: Influencer) -> InfluencerDTO:
        """Convierte una entidad Influencer a DTO."""
        
        # Obtener plataformas
        plataformas = [plat.value for plat in influencer.audiencia_por_plataforma.keys()]
        
        # Calcular tipo principal
        tipo_principal = None
        if influencer.obtener_tipo_principal():
            tipo_principal = influencer.obtener_tipo_principal().value
        
        # Convertir demografía si existe
        demografia_dto = None
        if influencer.demografia:
            from .dto import DemografiaDTO
            demografia_dto = DemografiaDTO(
                distribucion_genero=influencer.demografia.distribucion_genero,
                distribucion_edad=influencer.demografia.distribucion_edad,
                paises_principales=influencer.demografia.paises_principales
            )
        
        return InfluencerDTO(
            id=influencer.id,
            nombre=influencer.nombre,
            email=influencer.email.valor,
            estado=influencer.estado,
            categorias=influencer.perfil.categorias.categorias,
            descripcion=influencer.perfil.descripcion,
            biografia=influencer.perfil.biografia,
            sitio_web=influencer.perfil.sitio_web,
            telefono=influencer.telefono.numero if influencer.telefono else None,
            fecha_creacion=influencer.fecha_creacion.isoformat(),
            fecha_activacion=influencer.fecha_activacion.isoformat() if influencer.fecha_activacion else None,
            plataformas=plataformas,
            total_seguidores=influencer.obtener_total_seguidores(),
            engagement_promedio=influencer.obtener_engagement_promedio(),
            tipo_principal=tipo_principal,
            campañas_completadas=influencer.metricas.campañas_completadas,
            cpm_promedio=influencer.metricas.cpm_promedio,
            ingresos_generados=influencer.metricas.ingresos_generados,
            demografia=demografia_dto
        )
