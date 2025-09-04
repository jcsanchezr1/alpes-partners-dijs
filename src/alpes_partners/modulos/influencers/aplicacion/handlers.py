import logging
from typing import List, Optional

from ....seedwork.aplicacion.handlers import ManejadorComando, ManejadorQuery
from ....seedwork.infraestructura.uow_sincrono import UnidadDeTrabajoSincrona
from ..dominio.repositorios import RepositorioInfluencers
from ..dominio.entidades import Influencer
from ..dominio.objetos_valor import DatosAudiencia, Demografia
from ..dominio.excepciones import InfluencerNoEncontrado, EmailYaRegistrado

from .comandos.registrar_influencer import RegistrarInfluencer
from .comandos.activar_influencer import ActivarInfluencer
from .comandos.desactivar_influencer import DesactivarInfluencer
from .comandos.actualizar_perfil_influencer import ActualizarPerfilInfluencer
from .comandos.agregar_plataforma import AgregarPlataforma

from .queries.obtener_influencer import ObtenerInfluencer, ObtenerInfluencerPorEmail
from .queries.obtener_todos_influencers import ObtenerTodosInfluencers
from .queries.obtener_influencers_activos import ObtenerInfluencersActivos

from .dto import InfluencerDTO

logger = logging.getLogger(__name__)


# ============= COMMAND HANDLERS =============

class ManejadorRegistrarInfluencer(ManejadorComando[RegistrarInfluencer]):
    """Handler para registrar un influencer."""
    
    def __init__(self, repositorio: RepositorioInfluencers, uow: UnidadDeTrabajoSincrona):
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
        
        # Agregar al repositorio
        logger.info(f"🔄 HANDLER: Llamando repositorio.agregar()...")
        self.repositorio.agregar(influencer)
        logger.info(f"✅ HANDLER: Repositorio.agregar() completado")
        
        # Agregar eventos a UoW
        logger.info(f"🔄 HANDLER: Agregando {len(influencer.eventos)} eventos a UoW")
        self.uow.agregar_eventos(influencer.eventos)
        influencer.limpiar_eventos()
        
        logger.info(f"✅ HANDLER: Handler completado - Influencer ID: {influencer.id}")


class ManejadorActivarInfluencer(ManejadorComando[ActivarInfluencer]):
    """Handler para activar un influencer."""
    
    def __init__(self, repositorio: RepositorioInfluencers, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: ActivarInfluencer) -> None:
        logger.info(f"🎯 HANDLER: Activando influencer - ID: {comando.influencer_id}")
        
        influencer = self.repositorio.obtener_por_id(comando.influencer_id)
        if not influencer:
            logger.warning(f"⚠️ HANDLER: Influencer no encontrado: {comando.influencer_id}")
            raise InfluencerNoEncontrado(f"Influencer con ID {comando.influencer_id} no encontrado")
        
        logger.info(f"🔄 HANDLER: Activando influencer: {influencer.nombre}")
        influencer.activar()
        
        self.repositorio.actualizar(influencer)
        self.uow.agregar_eventos(influencer.eventos)
        influencer.limpiar_eventos()
        
        logger.info(f"✅ HANDLER: Influencer activado - ID: {comando.influencer_id}")


class ManejadorDesactivarInfluencer(ManejadorComando[DesactivarInfluencer]):
    """Handler para desactivar un influencer."""
    
    def __init__(self, repositorio: RepositorioInfluencers, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: DesactivarInfluencer) -> None:
        logger.info(f"🎯 HANDLER: Desactivando influencer - ID: {comando.influencer_id}")
        
        influencer = self.repositorio.obtener_por_id(comando.influencer_id)
        if not influencer:
            logger.warning(f"⚠️ HANDLER: Influencer no encontrado: {comando.influencer_id}")
            raise InfluencerNoEncontrado(f"Influencer con ID {comando.influencer_id} no encontrado")
        
        logger.info(f"🔄 HANDLER: Desactivando influencer: {influencer.nombre}")
        influencer.desactivar(comando.motivo)
        
        self.repositorio.actualizar(influencer)
        self.uow.agregar_eventos(influencer.eventos)
        influencer.limpiar_eventos()
        
        logger.info(f"✅ HANDLER: Influencer desactivado - ID: {comando.influencer_id}")


class ManejadorActualizarPerfilInfluencer(ManejadorComando[ActualizarPerfilInfluencer]):
    """Handler para actualizar perfil de influencer."""
    
    def __init__(self, repositorio: RepositorioInfluencers, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: ActualizarPerfilInfluencer) -> None:
        logger.info(f"🎯 HANDLER: Actualizando perfil - ID: {comando.influencer_id}")
        
        influencer = self.repositorio.obtener_por_id(comando.influencer_id)
        if not influencer:
            logger.warning(f"⚠️ HANDLER: Influencer no encontrado: {comando.influencer_id}")
            raise InfluencerNoEncontrado(f"Influencer con ID {comando.influencer_id} no encontrado")
        
        logger.info(f"🔄 HANDLER: Actualizando perfil de: {influencer.nombre}")
        influencer.actualizar_perfil(
            descripcion=comando.descripcion,
            biografia=comando.biografia,
            sitio_web=comando.sitio_web
        )
        
        self.repositorio.actualizar(influencer)
        self.uow.agregar_eventos(influencer.eventos)
        influencer.limpiar_eventos()
        
        logger.info(f"✅ HANDLER: Perfil actualizado - ID: {comando.influencer_id}")


class ManejadorAgregarPlataforma(ManejadorComando[AgregarPlataforma]):
    """Handler para agregar plataforma a influencer."""
    
    def __init__(self, repositorio: RepositorioInfluencers, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: AgregarPlataforma) -> None:
        logger.info(f"🎯 HANDLER: Agregando plataforma - ID: {comando.influencer_id}")
        
        influencer = self.repositorio.obtener_por_id(comando.influencer_id)
        if not influencer:
            logger.warning(f"⚠️ HANDLER: Influencer no encontrado: {comando.influencer_id}")
            raise InfluencerNoEncontrado(f"Influencer con ID {comando.influencer_id} no encontrado")
        
        # Crear objeto de valor DatosAudiencia
        datos_audiencia = DatosAudiencia(
            plataforma=comando.datos_audiencia.plataforma,
            seguidores=comando.datos_audiencia.seguidores,
            engagement_rate=comando.datos_audiencia.engagement_rate,
            alcance_promedio=comando.datos_audiencia.alcance_promedio
        )
        
        logger.info(f"🔄 HANDLER: Agregando plataforma {datos_audiencia.plataforma.value} a: {influencer.nombre}")
        influencer.agregar_plataforma(datos_audiencia)
        
        self.repositorio.actualizar(influencer)
        self.uow.agregar_eventos(influencer.eventos)
        influencer.limpiar_eventos()
        
        logger.info(f"✅ HANDLER: Plataforma agregada - ID: {comando.influencer_id}")


# ============= QUERY HANDLERS =============

class ManejadorObtenerInfluencer(ManejadorQuery[ObtenerInfluencer]):
    """Handler para obtener un influencer por ID."""
    
    def __init__(self, repositorio: RepositorioInfluencers):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerInfluencer) -> Optional[InfluencerDTO]:
        logger.info(f"🎯 HANDLER: Obteniendo influencer - ID: {query.influencer_id}")
        
        influencer = self.repositorio.obtener_por_id(query.influencer_id)
        if not influencer:
            logger.info(f"❌ HANDLER: Influencer no encontrado: {query.influencer_id}")
            return None
        
        logger.info(f"✅ HANDLER: Influencer encontrado: {influencer.nombre}")
        return self._convertir_a_dto(influencer)


class ManejadorObtenerInfluencerPorEmail(ManejadorQuery[ObtenerInfluencerPorEmail]):
    """Handler para obtener un influencer por email."""
    
    def __init__(self, repositorio: RepositorioInfluencers):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerInfluencerPorEmail) -> Optional[InfluencerDTO]:
        logger.info(f"🎯 HANDLER: Obteniendo influencer por email: {query.email}")
        
        influencer = self.repositorio.obtener_por_email(query.email)
        if not influencer:
            logger.info(f"❌ HANDLER: Influencer no encontrado con email: {query.email}")
            return None
        
        logger.info(f"✅ HANDLER: Influencer encontrado: {influencer.nombre}")
        return self._convertir_a_dto(influencer)


class ManejadorObtenerTodosInfluencers(ManejadorQuery[ObtenerTodosInfluencers]):
    """Handler para obtener todos los influencers con filtros."""
    
    def __init__(self, repositorio: RepositorioInfluencers):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerTodosInfluencers) -> List[InfluencerDTO]:
        logger.info("🎯 HANDLER: Obteniendo todos los influencers con filtros")
        
        # Usar el método con filtros del repositorio
        influencers = self.repositorio.obtener_con_filtros(
            estado=query.estado,
            tipo=query.tipo,
            categoria=query.categoria,
            plataforma=query.plataforma,
            min_seguidores=query.min_seguidores,
            max_seguidores=query.max_seguidores,
            engagement_minimo=query.engagement_minimo,
            limite=query.limite,
            offset=query.offset
        )
        
        logger.info(f"✅ HANDLER: {len(influencers)} influencers encontrados")
        return [self._convertir_a_dto(influencer) for influencer in influencers]


class ManejadorObtenerInfluencersActivos(ManejadorQuery[ObtenerInfluencersActivos]):
    """Handler para obtener influencers activos."""
    
    def __init__(self, repositorio: RepositorioInfluencers):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerInfluencersActivos) -> List[InfluencerDTO]:
        logger.info("🎯 HANDLER: Obteniendo influencers activos")
        
        from ..dominio.objetos_valor import EstadoInfluencer
        
        # Usar el método con filtros, forzando estado activo
        influencers = self.repositorio.obtener_con_filtros(
            estado=EstadoInfluencer.ACTIVO,
            tipo=query.tipo,
            categoria=query.categoria,
            plataforma=query.plataforma,
            min_seguidores=query.min_seguidores,
            engagement_minimo=query.engagement_minimo,
            limite=query.limite,
            offset=query.offset
        )
        
        logger.info(f"✅ HANDLER: {len(influencers)} influencers activos encontrados")
        return [self._convertir_a_dto(influencer) for influencer in influencers]


# ============= HELPER METHODS =============

def _convertir_a_dto(influencer: Influencer) -> InfluencerDTO:
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


# ============= INTEGRATION HANDLERS =============

class HandlerInfluencerIntegracion:
    """Handler para eventos de integración de influencers."""
    
    @staticmethod
    def handle_influencer_registrado(evento):
        """Maneja el evento de influencer registrado."""
        logger.info(f"🔔 INTEGRACIÓN: Influencer registrado - ID: {evento.id}")
        # TODO: Implementar lógica de integración
        pass
    
    @staticmethod
    def handle_influencer_activado(evento):
        """Maneja el evento de influencer activado."""
        logger.info(f"🔔 INTEGRACIÓN: Influencer activado - ID: {evento.id}")
        # TODO: Implementar lógica de integración
        pass
    
    @staticmethod
    def handle_influencer_desactivado(evento):
        """Maneja el evento de influencer desactivado."""
        logger.info(f"🔔 INTEGRACIÓN: Influencer desactivado - ID: {evento.id}")
        # TODO: Implementar lógica de integración
        pass


# Agregar método helper a las clases que lo necesitan
ManejadorObtenerInfluencer._convertir_a_dto = staticmethod(_convertir_a_dto)
ManejadorObtenerInfluencerPorEmail._convertir_a_dto = staticmethod(_convertir_a_dto)
ManejadorObtenerTodosInfluencers._convertir_a_dto = staticmethod(_convertir_a_dto)
ManejadorObtenerInfluencersActivos._convertir_a_dto = staticmethod(_convertir_a_dto)
