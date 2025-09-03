from typing import List
import logging
from ....seedwork.aplicacion.handlers import ManejadorComando, ManejadorQuery
from ....seedwork.aplicacion.queries import ResultadoQuery
from ....seedwork.infraestructura.uow_sincrono import UnidadDeTrabajoSincrona

logger = logging.getLogger(__name__)
from .comandos.registrar_afiliado import RegistrarAfiliado
from .comandos.activar_afiliado import ActivarAfiliado
from .comandos.desactivar_afiliado import DesactivarAfiliado
from .comandos.actualizar_perfil_afiliado import ActualizarPerfilAfiliado
from .queries.obtener_afiliado import ObtenerAfiliado, ObtenerAfiliadoPorEmail
from .queries.obtener_todos_afiliados import ObtenerTodosAfiliados
from .queries.obtener_afiliados_activos import ObtenerAfiliadosActivos
from .dto import AfiliadoDTO
from ..dominio.entidades import Afiliado
from ..dominio.repositorios import RepositorioAfiliados
from ..dominio.excepciones import AfiliadoNoEncontrado, EmailYaRegistrado
from ..dominio.objetos_valor import EstadoAfiliado


class ManejadorRegistrarAfiliado(ManejadorComando[RegistrarAfiliado]):
    """Manejador para registrar afiliado."""
    
    def __init__(self, repositorio: RepositorioAfiliados, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: RegistrarAfiliado) -> None:
        logger.info(f"🎯 HANDLER: Iniciando registro de afiliado - Email: {comando.email}")
        
        # Verificar que el email no esté registrado
        logger.info(f"🔍 HANDLER: Verificando si email existe: {comando.email}")
        if self.repositorio.existe_email(comando.email):
            logger.warning(f"⚠️ HANDLER: Email ya registrado: {comando.email}")
            raise EmailYaRegistrado(f"Ya existe un afiliado con el email {comando.email}")
        
        logger.info(f"✅ HANDLER: Email disponible: {comando.email}")
        
        # Crear afiliado
        logger.info(f"🔄 HANDLER: Creando entidad afiliado...")
        logger.info(f"🔄 HANDLER: Tipo afiliado recibido: {comando.tipo_afiliado} (tipo: {type(comando.tipo_afiliado)})")
        afiliado = Afiliado.crear(
            nombre=comando.nombre,
            email=comando.email,
            tipo_afiliado=comando.tipo_afiliado,
            categorias=comando.categorias,
            descripcion=comando.descripcion,
            sitio_web=comando.sitio_web,
            telefono=comando.telefono,
            redes_sociales=comando.redes_sociales
        )
        
        logger.info(f"✅ HANDLER: Afiliado creado - ID: {afiliado.id}, Eventos: {len(afiliado.eventos)}")
        
        # Guardar
        logger.info(f"🔄 HANDLER: Llamando repositorio.agregar()...")
        self.repositorio.agregar(afiliado)
        logger.info(f"✅ HANDLER: Repositorio.agregar() completado")
        
        # Agregar eventos al UoW
        logger.info(f"🔄 HANDLER: Agregando {len(afiliado.eventos)} eventos a UoW")
        self.uow.agregar_eventos(afiliado.eventos)
        afiliado.limpiar_eventos()
        logger.info(f"✅ HANDLER: Handler completado - Afiliado ID: {afiliado.id}")


class ManejadorActivarAfiliado(ManejadorComando[ActivarAfiliado]):
    """Manejador para activar afiliado."""
    
    def __init__(self, repositorio: RepositorioAfiliados, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: ActivarAfiliado) -> None:
        afiliado = self.repositorio.obtener_por_id(comando.afiliado_id)
        if not afiliado:
            raise AfiliadoNoEncontrado(f"Afiliado {comando.afiliado_id} no encontrado")
        
        afiliado.activar()
        self.repositorio.actualizar(afiliado)
        
        # Agregar eventos al UoW
        self.uow.agregar_eventos(afiliado.eventos)
        afiliado.limpiar_eventos()


class ManejadorDesactivarAfiliado(ManejadorComando[DesactivarAfiliado]):
    """Manejador para desactivar afiliado."""
    
    def __init__(self, repositorio: RepositorioAfiliados, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: DesactivarAfiliado) -> None:
        afiliado = self.repositorio.obtener_por_id(comando.afiliado_id)
        if not afiliado:
            raise AfiliadoNoEncontrado(f"Afiliado {comando.afiliado_id} no encontrado")
        
        afiliado.desactivar(comando.motivo)
        self.repositorio.actualizar(afiliado)
        
        # Agregar eventos al UoW
        self.uow.agregar_eventos(afiliado.eventos)
        afiliado.limpiar_eventos()


class ManejadorActualizarPerfilAfiliado(ManejadorComando[ActualizarPerfilAfiliado]):
    """Manejador para actualizar perfil de afiliado."""
    
    def __init__(self, repositorio: RepositorioAfiliados, uow: UnidadDeTrabajoSincrona):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: ActualizarPerfilAfiliado) -> None:
        afiliado = self.repositorio.obtener_por_id(comando.afiliado_id)
        if not afiliado:
            raise AfiliadoNoEncontrado(f"Afiliado {comando.afiliado_id} no encontrado")
        
        afiliado.actualizar_perfil(
            descripcion=comando.descripcion,
            sitio_web=comando.sitio_web,
            redes_sociales=comando.redes_sociales
        )
        self.repositorio.actualizar(afiliado)
        
        # Agregar eventos al UoW
        self.uow.agregar_eventos(afiliado.eventos)
        afiliado.limpiar_eventos()


class ManejadorObtenerAfiliado(ManejadorQuery[ObtenerAfiliado]):
    """Manejador para obtener afiliado por ID."""
    
    def __init__(self, repositorio: RepositorioAfiliados):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerAfiliado) -> ResultadoQuery:
        afiliado = self.repositorio.obtener_por_id(query.afiliado_id)
        if not afiliado:
            return ResultadoQuery(None, False, "Afiliado no encontrado")
        
        dto = self._convertir_a_dto(afiliado)
        return ResultadoQuery(dto, True)
    
    def _convertir_a_dto(self, afiliado: Afiliado) -> AfiliadoDTO:
        return AfiliadoDTO(
            id=afiliado.id,
            nombre=afiliado.nombre,
            email=afiliado.email.valor,
            tipo_afiliado=afiliado.perfil.tipo,
            estado=afiliado.estado,
            categorias=afiliado.perfil.categorias.categorias,
            descripcion=afiliado.perfil.descripcion,
            sitio_web=afiliado.perfil.sitio_web,
            telefono=afiliado.telefono.numero if afiliado.telefono else "",
            redes_sociales=afiliado.perfil.redes_sociales,
            fecha_creacion=afiliado.fecha_creacion.isoformat(),
            fecha_activacion=afiliado.fecha_activacion.isoformat() if afiliado.fecha_activacion else None,
            clics_totales=afiliado.metricas.clics_totales,
            conversiones_totales=afiliado.metricas.conversiones_totales,
            ingresos_generados=afiliado.metricas.ingresos_generados,
            tasa_conversion=afiliado.metricas.calcular_tasa_conversion()
        )


class ManejadorObtenerAfiliadosActivos(ManejadorQuery[ObtenerAfiliadosActivos]):
    """Manejador para obtener afiliados activos."""
    
    def __init__(self, repositorio: RepositorioAfiliados):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerAfiliadosActivos) -> ResultadoQuery:
        # Obtener afiliados activos
        afiliados = self.repositorio.obtener_por_estado(EstadoAfiliado.ACTIVO)
        
        # Aplicar filtros adicionales
        if query.tipo:
            afiliados = [a for a in afiliados if a.perfil.tipo == query.tipo]
        
        if query.categoria:
            afiliados = [a for a in afiliados if a.es_compatible_con_categoria(query.categoria)]
        
        # Aplicar paginación (simplificada)
        afiliados_paginados = afiliados[query.offset:query.offset + query.limite]
        
        dtos = [self._convertir_a_dto(afiliado) for afiliado in afiliados_paginados]
        return ResultadoQuery(dtos, True)
    
    def _convertir_a_dto(self, afiliado: Afiliado) -> AfiliadoDTO:
        return AfiliadoDTO(
            id=afiliado.id,
            nombre=afiliado.nombre,
            email=afiliado.email.valor,
            tipo_afiliado=afiliado.perfil.tipo,
            estado=afiliado.estado,
            categorias=afiliado.perfil.categorias.categorias,
            descripcion=afiliado.perfil.descripcion,
            sitio_web=afiliado.perfil.sitio_web,
            telefono=afiliado.telefono.numero if afiliado.telefono else "",
            redes_sociales=afiliado.perfil.redes_sociales,
            fecha_creacion=afiliado.fecha_creacion.isoformat(),
            fecha_activacion=afiliado.fecha_activacion.isoformat() if afiliado.fecha_activacion else None,
            clics_totales=afiliado.metricas.clics_totales,
            conversiones_totales=afiliado.metricas.conversiones_totales,
            ingresos_generados=afiliado.metricas.ingresos_generados,
            tasa_conversion=afiliado.metricas.calcular_tasa_conversion()
        )


class ManejadorObtenerTodosAfiliados(ManejadorQuery[ObtenerTodosAfiliados]):
    """Manejador para obtener todos los afiliados."""
    
    def __init__(self, repositorio: RepositorioAfiliados):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerTodosAfiliados) -> ResultadoQuery:
        afiliados = []
        
        if query.estado:
            afiliados = self.repositorio.obtener_por_estado(query.estado)
        elif query.tipo:
            afiliados = self.repositorio.obtener_por_tipo(query.tipo)
        elif query.categoria:
            afiliados = self.repositorio.obtener_por_categoria(query.categoria)
        else:
            afiliados = self.repositorio.obtener_todos()
        
        # Aplicar paginación (simplificada)
        afiliados_paginados = afiliados[query.offset:query.offset + query.limite]
        
        dtos = [self._convertir_a_dto(afiliado) for afiliado in afiliados_paginados]
        return ResultadoQuery(dtos, True)
    
    def _convertir_a_dto(self, afiliado: Afiliado) -> AfiliadoDTO:
        return AfiliadoDTO(
            id=afiliado.id,
            nombre=afiliado.nombre,
            email=afiliado.email.valor,
            tipo_afiliado=afiliado.perfil.tipo,
            estado=afiliado.estado,
            categorias=afiliado.perfil.categorias.categorias,
            descripcion=afiliado.perfil.descripcion,
            sitio_web=afiliado.perfil.sitio_web,
            telefono=afiliado.telefono.numero if afiliado.telefono else "",
            redes_sociales=afiliado.perfil.redes_sociales,
            fecha_creacion=afiliado.fecha_creacion.isoformat(),
            fecha_activacion=afiliado.fecha_activacion.isoformat() if afiliado.fecha_activacion else None,
            clics_totales=afiliado.metricas.clics_totales,
            conversiones_totales=afiliado.metricas.conversiones_totales,
            ingresos_generados=afiliado.metricas.ingresos_generados,
            tasa_conversion=afiliado.metricas.calcular_tasa_conversion()
        )


class ManejadorObtenerAfiliadosActivos(ManejadorQuery[ObtenerAfiliadosActivos]):
    """Manejador para obtener afiliados activos."""
    
    def __init__(self, repositorio: RepositorioAfiliados):
        self.repositorio = repositorio
    
    def handle(self, query: ObtenerAfiliadosActivos) -> ResultadoQuery:
        # Obtener afiliados activos
        afiliados = self.repositorio.obtener_por_estado(EstadoAfiliado.ACTIVO)
        
        # Aplicar filtros adicionales
        if query.tipo:
            afiliados = [a for a in afiliados if a.perfil.tipo == query.tipo]
        
        if query.categoria:
            afiliados = [a for a in afiliados if a.es_compatible_con_categoria(query.categoria)]
        
        # Aplicar paginación (simplificada)
        afiliados_paginados = afiliados[query.offset:query.offset + query.limite]
        
        dtos = [self._convertir_a_dto(afiliado) for afiliado in afiliados_paginados]
        return ResultadoQuery(dtos, True)
    
    def _convertir_a_dto(self, afiliado: Afiliado) -> AfiliadoDTO:
        return AfiliadoDTO(
            id=afiliado.id,
            nombre=afiliado.nombre,
            email=afiliado.email.valor,
            tipo_afiliado=afiliado.perfil.tipo,
            estado=afiliado.estado,
            categorias=afiliado.perfil.categorias.categorias,
            descripcion=afiliado.perfil.descripcion,
            sitio_web=afiliado.perfil.sitio_web,
            telefono=afiliado.telefono.numero if afiliado.telefono else "",
            redes_sociales=afiliado.perfil.redes_sociales,
            fecha_creacion=afiliado.fecha_creacion.isoformat(),
            fecha_activacion=afiliado.fecha_activacion.isoformat() if afiliado.fecha_activacion else None,
            clics_totales=afiliado.metricas.clics_totales,
            conversiones_totales=afiliado.metricas.conversiones_totales,
            ingresos_generados=afiliado.metricas.ingresos_generados,
            tasa_conversion=afiliado.metricas.calcular_tasa_conversion()
        )
