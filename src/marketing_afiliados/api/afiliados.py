from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

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


# Dependencias (estas deberían ser inyectadas desde un contenedor DI)
async def obtener_mediador():
    # Aquí se inyectaría el mediador real
    pass


@router.post("/", response_model=RespuestaAPI, status_code=status.HTTP_201_CREATED)
async def registrar_afiliado(
    datos: RegistrarAfiliadoDTO,
    mediador = Depends(obtener_mediador)
):
    """Registra un nuevo afiliado."""
    try:
        comando = RegistrarAfiliado(datos)
        await mediador.enviar_comando(comando)
        
        return RespuestaAPI(
            mensaje="Afiliado registrado exitosamente",
            datos={"afiliado_id": comando.id}
        )
    except EmailYaRegistrado as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/", response_model=List[AfiliadoDTO])
async def listar_afiliados(
    estado: Optional[EstadoAfiliado] = None,
    tipo: Optional[TipoAfiliado] = None,
    categoria: Optional[str] = None,
    limite: int = 100,
    offset: int = 0,
    mediador = Depends(obtener_mediador)
):
    """Lista afiliados con filtros opcionales."""
    try:
        query = ObtenerTodosAfiliados(
            estado=estado,
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
