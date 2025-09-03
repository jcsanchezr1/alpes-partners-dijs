from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

from ..modulos.afiliados.aplicacion.dto import RegistrarAfiliadoDTO, AfiliadoDTO, ActualizarPerfilAfiliadoDTO
from ..modulos.afiliados.aplicacion.comandos.registrar_afiliado import RegistrarAfiliado
from ..modulos.afiliados.aplicacion.comandos.activar_afiliado import ActivarAfiliado
from ..modulos.afiliados.aplicacion.comandos.desactivar_afiliado import DesactivarAfiliado
from ..modulos.afiliados.aplicacion.comandos.actualizar_perfil_afiliado import ActualizarPerfilAfiliado
from ..modulos.afiliados.aplicacion.queries.obtener_afiliado import ObtenerAfiliado
from ..modulos.afiliados.aplicacion.queries.obtener_todos_afiliados import ObtenerTodosAfiliados
from ..modulos.afiliados.aplicacion.queries.obtener_afiliados_activos import ObtenerAfiliadosActivos
from ..modulos.afiliados.dominio.objetos_valor import TipoAfiliado, EstadoAfiliado
from ..modulos.afiliados.dominio.excepciones import AfiliadoNoEncontrado, EmailYaRegistrado

router = APIRouter(prefix="/api/v1/afiliados", tags=["afiliados"])


class DesactivarAfiliadoRequest(BaseModel):
    motivo: str


class RespuestaAPI(BaseModel):
    mensaje: str
    datos: Optional[dict] = None


# Importaciones adicionales para el mediador
from ..seedwork.aplicacion.mediador import MediadorMemoria
from ..seedwork.infraestructura.uow_sincrono import UnidadDeTrabajoSincrona
from ..seedwork.infraestructura.database import get_db_session
from ..modulos.afiliados.infraestructura.repositorio_sqlalchemy import RepositorioAfiliadosSQLAlchemy
from ..modulos.afiliados.aplicacion.handlers import (
    ManejadorRegistrarAfiliado, ManejadorActivarAfiliado, ManejadorDesactivarAfiliado,
    ManejadorActualizarPerfilAfiliado, ManejadorObtenerAfiliado, ManejadorObtenerTodosAfiliados
)

# Cache del mediador (se recrea para cada request con nueva sesión DB)
_mediador_cache = None

def _configurar_mediador(repositorio: RepositorioAfiliadosSQLAlchemy, uow: UnidadDeTrabajoSincrona):
    """Configura el mediador con todos los manejadores."""
    
    # Siempre creamos un nuevo mediador para cada request (con nueva sesión DB)
    mediador = MediadorMemoria()
    
    # Registrar manejadores de comandos
    mediador.registrar_manejador_comando(
        RegistrarAfiliado, 
        ManejadorRegistrarAfiliado(repositorio, uow)
    )
    mediador.registrar_manejador_comando(
        ActivarAfiliado, 
        ManejadorActivarAfiliado(repositorio, uow)
    )
    mediador.registrar_manejador_comando(
        DesactivarAfiliado, 
        ManejadorDesactivarAfiliado(repositorio, uow)
    )
    mediador.registrar_manejador_comando(
        ActualizarPerfilAfiliado, 
        ManejadorActualizarPerfilAfiliado(repositorio, uow)
    )
    
    # Registrar manejadores de queries
    mediador.registrar_manejador_query(
        ObtenerAfiliado, 
        ManejadorObtenerAfiliado(repositorio)
    )
    mediador.registrar_manejador_query(
        ObtenerTodosAfiliados, 
        ManejadorObtenerTodosAfiliados(repositorio)
    )
    
    # Importar y registrar ManejadorObtenerAfiliadosActivos
    from ..modulos.afiliados.aplicacion.handlers import ManejadorObtenerAfiliadosActivos
    mediador.registrar_manejador_query(
        ObtenerAfiliadosActivos, 
        ManejadorObtenerAfiliadosActivos(repositorio)
    )
    
    return mediador

# Dependencia para obtener sesión de base de datos
def obtener_session_db():
    for session in get_db_session():
        yield session

# Dependencias (estas deberían ser inyectadas desde un contenedor DI)
def obtener_mediador(session_db = Depends(obtener_session_db)):
    # Crear repositorio y UoW con la sesión de base de datos
    repositorio = RepositorioAfiliadosSQLAlchemy(session_db)
    uow = UnidadDeTrabajoSincrona(session_db)
    
    # Configurar y retornar el mediador
    return _configurar_mediador(repositorio, uow)


@router.post("/", response_model=RespuestaAPI, status_code=status.HTTP_201_CREATED)
def registrar_afiliado(
    datos: RegistrarAfiliadoDTO,
    session_db = Depends(obtener_session_db)
):
    """Registra un nuevo afiliado."""
    logger.info(f"🚀 API: Iniciando registro de afiliado - Email: {datos.email}")
    
    try:
        # Crear repositorio y UoW
        logger.info("🔄 API: Creando repositorio y UoW...")
        repositorio = RepositorioAfiliadosSQLAlchemy(session_db)
        uow = UnidadDeTrabajoSincrona(session_db)
        
        # Configurar mediador
        logger.info("🔄 API: Configurando mediador...")
        mediador = _configurar_mediador(repositorio, uow)
        
        # Ejecutar comando dentro de transacción
        logger.info("🔄 API: Iniciando transacción...")
        with uow:
            logger.info("🔄 API: Creando comando...")
            comando = RegistrarAfiliado(datos)
            logger.info(f"🔄 API: Enviando comando al mediador - ID: {comando.id}")
            mediador.enviar_comando(comando)
            logger.info("✅ API: Comando procesado por mediador")
        
        logger.info(f"✅ API: Transacción completada - Afiliado ID: {comando.id}")
        
        return RespuestaAPI(
            mensaje="Afiliado registrado exitosamente",
            datos={"afiliado_id": comando.id}
        )
    except EmailYaRegistrado as e:
        logger.warning(f"⚠️ API: Email ya registrado: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"❌ API: Error interno: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/", response_model=List[AfiliadoDTO])
def listar_afiliados(
    estado: Optional[EstadoAfiliado] = None,
    tipo: Optional[TipoAfiliado] = None,
    categoria: Optional[str] = None,
    limite: int = 100,
    offset: int = 0,
    session_db = Depends(obtener_session_db)
):
    """Lista afiliados con filtros opcionales."""
    logger.info("🔍 API: Iniciando consulta de afiliados")
    
    try:
        # Crear repositorio y mediador
        logger.info("🔄 API: Creando repositorio para consulta...")
        repositorio = RepositorioAfiliadosSQLAlchemy(session_db)
        uow = UnidadDeTrabajoSincrona(session_db)
        mediador = _configurar_mediador(repositorio, uow)
        
        logger.info(f"🔄 API: Ejecutando query - Estado: {estado}, Tipo: {tipo}, Categoría: {categoria}")
        query = ObtenerTodosAfiliados(
            estado=estado,
            tipo=tipo,
            categoria=categoria,
            limite=limite,
            offset=offset
        )
        resultado = mediador.enviar_query(query)
        
        if resultado.exitoso:
            logger.info(f"✅ API: Query exitosa - {len(resultado.datos)} afiliados encontrados")
            return resultado.datos
        else:
            logger.error(f"❌ API: Query falló - {resultado.mensaje}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=resultado.mensaje
            )
    except Exception as e:
        logger.error(f"❌ API: Error en consulta: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/activos", response_model=List[AfiliadoDTO])
async def listar_afiliados_activos(
    tipo: Optional[TipoAfiliado] = None,
    categoria: Optional[str] = None,
    limite: int = 100,
    offset: int = 0,
    mediador = Depends(obtener_mediador)
):
    """Lista afiliados activos."""
    try:
        query = ObtenerAfiliadosActivos(
            tipo=tipo,
            categoria=categoria,
            limite=limite,
            offset=offset
        )
        resultado = await mediador.enviar_query(query)
        
        if resultado.exitoso:
            return resultado.datos
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=resultado.mensaje
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{afiliado_id}", response_model=AfiliadoDTO)
async def obtener_afiliado(
    afiliado_id: str,
    mediador = Depends(obtener_mediador)
):
    """Obtiene un afiliado por ID."""
    try:
        query = ObtenerAfiliado(afiliado_id)
        resultado = await mediador.enviar_query(query)
        
        if resultado.exitoso and resultado.datos:
            return resultado.datos
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Afiliado no encontrado"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{afiliado_id}/activar", response_model=RespuestaAPI)
async def activar_afiliado(
    afiliado_id: str,
    mediador = Depends(obtener_mediador)
):
    """Activa un afiliado."""
    try:
        comando = ActivarAfiliado(afiliado_id)
        await mediador.enviar_comando(comando)
        
        return RespuestaAPI(mensaje="Afiliado activado exitosamente")
    except AfiliadoNoEncontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Afiliado no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{afiliado_id}/desactivar", response_model=RespuestaAPI)
async def desactivar_afiliado(
    afiliado_id: str,
    request: DesactivarAfiliadoRequest,
    mediador = Depends(obtener_mediador)
):
    """Desactiva un afiliado."""
    try:
        comando = DesactivarAfiliado(afiliado_id, request.motivo)
        await mediador.enviar_comando(comando)
        
        return RespuestaAPI(mensaje="Afiliado desactivado exitosamente")
    except AfiliadoNoEncontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Afiliado no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{afiliado_id}/perfil", response_model=RespuestaAPI)
async def actualizar_perfil_afiliado(
    afiliado_id: str,
    datos: ActualizarPerfilAfiliadoDTO,
    mediador = Depends(obtener_mediador)
):
    """Actualiza el perfil de un afiliado."""
    try:
        comando = ActualizarPerfilAfiliado(
            afiliado_id=afiliado_id,
            descripcion=datos.descripcion,
            sitio_web=datos.sitio_web,
            redes_sociales=datos.redes_sociales
        )
        await mediador.enviar_comando(comando)
        
        return RespuestaAPI(mensaje="Perfil actualizado exitosamente")
    except AfiliadoNoEncontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Afiliado no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
