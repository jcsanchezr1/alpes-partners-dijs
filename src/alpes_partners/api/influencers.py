import alpes_partners.seedwork.presentacion.api as api
import json
from typing import List, Optional
import logging

from flask import request, Response
from ..modulos.influencers.aplicacion.dto import InfluencerDTO
from ..modulos.influencers.aplicacion.servicios import ServicioInfluencer
from ..modulos.influencers.dominio.objetos_valor import TipoInfluencer, EstadoInfluencer, Plataforma
from ..modulos.influencers.dominio.excepciones import InfluencerNoEncontrado, EmailYaRegistrado
from ..seedwork.aplicacion.comandos import ejecutar_commando
from ..seedwork.dominio.excepciones import ExcepcionDominio

# Importar el comando DIRECTAMENTE para registrarlo (como en el tutorial)
from ..modulos.influencers.aplicacion.comandos.registrar_influencer import RegistrarInfluencer
from ..modulos.influencers.aplicacion.queries.obtener_influencer import ObtenerInfluencer
from ..seedwork.aplicacion.queries import ejecutar_query

logger = logging.getLogger(__name__)

# Crear blueprint siguiendo el patrón del tutorial
bp = api.crear_blueprint('influencers', '/influencers')

# Importaciones para el servicio
from ..seedwork.infraestructura.uow_sincrono import UnidadDeTrabajoSincrona
from ..seedwork.infraestructura.database import get_db_session
from ..modulos.influencers.infraestructura.repositorio_sqlalchemy import RepositorioInfluencersSQLAlchemy


def obtener_servicio_influencer():
    """Función helper para obtener el servicio de influencers."""
    session_db = next(get_db_session())
    repositorio = RepositorioInfluencersSQLAlchemy(session_db)
    uow = UnidadDeTrabajoSincrona(session_db)
    return ServicioInfluencer(repositorio, uow), session_db


@bp.route('/registrar', methods=('POST',))
def registrar_influencer():
    """Registra un nuevo influencer usando el servicio."""
    try:
        datos_dict = request.json
        logger.info(f"🚀 API: Iniciando registro de influencer - Email: {datos_dict.get('email')}")
        
        servicio, session_db = obtener_servicio_influencer()
        try:
            # Crear objeto de datos desde el request
            class RegistrarInfluencerRequest:
                def __init__(self, **kwargs):
                    self.nombre = kwargs.get('nombre')
                    self.email = kwargs.get('email')
                    self.categorias = kwargs.get('categorias', [])
                    self.descripcion = kwargs.get('descripcion', '')
                    self.biografia = kwargs.get('biografia', '')
                    self.sitio_web = kwargs.get('sitio_web', '')
                    self.telefono = kwargs.get('telefono', '')
            
            datos = RegistrarInfluencerRequest(**datos_dict)
            influencer_id = servicio.registrar_influencer(datos)
            
            logger.info(f"✅ API: Influencer registrado exitosamente - ID: {influencer_id}")
            return Response(
                json.dumps({
                    "mensaje": "Influencer registrado exitosamente",
                    "datos": {"influencer_id": influencer_id}
                }),
                status=201,
                mimetype='application/json'
            )
        finally:
            session_db.close()
            
    except EmailYaRegistrado as e:
        logger.warning(f"⚠️ API: Email ya registrado: {e}")
        return Response(
            json.dumps({"error": str(e)}),
            status=409,
            mimetype='application/json'
        )
    except ExcepcionDominio as e:
        logger.error(f"❌ API: Error de dominio: {e}")
        return Response(
            json.dumps({"error": str(e)}),
            status=400,
            mimetype='application/json'
        )
    except Exception as e:
        logger.error(f"❌ API: Error interno: {e}", exc_info=True)
        return Response(
            json.dumps({"error": "Error interno del servidor"}),
            status=500,
            mimetype='application/json'
        )


@bp.route('/registrar-comando', methods=('POST',))
def registrar_influencer_asincrono():
    """Registra un nuevo influencer usando el patrón de comandos asíncrono."""
    try:
        datos_dict = request.json
        logger.info(f"🚀 API: Iniciando registro asíncrono de influencer - Email: {datos_dict.get('email')}")
        
        from datetime import datetime
        import uuid
        
        # Crear comando (siguiendo el patrón de CrearReserva)
        comando = RegistrarInfluencer(
            fecha_creacion=datetime.utcnow().isoformat(),
            fecha_actualizacion=datetime.utcnow().isoformat(),
            id=str(uuid.uuid4()),
            nombre=datos_dict.get('nombre'),
            email=datos_dict.get('email'),
            categorias=datos_dict.get('categorias', []),
            descripcion=datos_dict.get('descripcion', ''),
            biografia=datos_dict.get('biografia', ''),
            sitio_web=datos_dict.get('sitio_web', ''),
            telefono=datos_dict.get('telefono', '')
        )
        
        # TODO: Reemplazar este código síncrono y usar el broker de eventos para propagar este comando de forma asíncrona
        # Revisar la clase Despachador de la capa de infraestructura
        ejecutar_commando(comando)
        
        logger.info(f"✅ API: Comando enviado exitosamente - Comando ID: {comando.id}")
        return Response(
            json.dumps({"mensaje": "Comando procesado", "comando_id": comando.id}),
            status=202,
            mimetype='application/json'
        )
        
    except ExcepcionDominio as e:
        logger.error(f"❌ API: Error de dominio: {e}")
        return Response(
            json.dumps({"error": str(e)}),
            status=400,
            mimetype='application/json'
        )
    except Exception as e:
        logger.error(f"❌ API: Error interno: {e}", exc_info=True)
        return Response(
            json.dumps({"error": "Error interno del servidor"}),
            status=500,
            mimetype='application/json'
        )


@bp.route('/', methods=('GET',))
def listar_influencers():
    """Lista influencers con filtros opcionales."""
    try:
        logger.info("🔍 API: Iniciando consulta de influencers")
        
        # Obtener parámetros de query
        estado = request.args.get('estado')
        tipo = request.args.get('tipo')
        categoria = request.args.get('categoria')
        plataforma = request.args.get('plataforma')
        min_seguidores = request.args.get('min_seguidores', type=int)
        max_seguidores = request.args.get('max_seguidores', type=int)
        engagement_minimo = request.args.get('engagement_minimo', type=float)
        limite = request.args.get('limite', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Convertir strings a enums si es necesario
        if estado:
            estado = EstadoInfluencer(estado)
        if tipo:
            tipo = TipoInfluencer(tipo)
        if plataforma:
            plataforma = Plataforma(plataforma)
        
        servicio, session_db = obtener_servicio_influencer()
        try:
            resultado = servicio.listar_influencers(
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
            
            logger.info(f"✅ API: Consulta exitosa - {len(resultado)} influencers encontrados")
            
            # Convertir DTOs a diccionarios para JSON
            resultado_dict = []
            for influencer_dto in resultado:
                resultado_dict.append({
                    'id': influencer_dto.id,
                    'nombre': influencer_dto.nombre,
                    'email': influencer_dto.email,
                    'categorias': influencer_dto.categorias,
                    'descripcion': influencer_dto.descripcion,
                    'biografia': influencer_dto.biografia,
                    'sitio_web': influencer_dto.sitio_web,
                    'telefono': influencer_dto.telefono,
                    'estado': influencer_dto.estado.value if influencer_dto.estado else None,
                    'tipo': influencer_dto.tipo.value if influencer_dto.tipo else None,
                    'fecha_creacion': influencer_dto.fecha_creacion,
                    'fecha_actualizacion': influencer_dto.fecha_actualizacion
                })
            
            return Response(
                json.dumps(resultado_dict),
                status=200,
                mimetype='application/json'
            )
        finally:
            session_db.close()
            
    except Exception as e:
        logger.error(f"❌ API: Error en consulta: {e}", exc_info=True)
        return Response(
            json.dumps({"error": "Error interno del servidor"}),
            status=500,
            mimetype='application/json'
        )


@bp.route('/<influencer_id>', methods=('GET',))
def obtener_influencer(influencer_id):
    """Obtiene un influencer por ID."""
    try:
        logger.info(f"🔍 API: Obteniendo influencer - ID: {influencer_id}")
        
        servicio, session_db = obtener_servicio_influencer()
        try:
            resultado = servicio.obtener_influencer_por_id(influencer_id)
            logger.info(f"✅ API: Influencer encontrado - ID: {influencer_id}")
            
            # Convertir DTO a diccionario para JSON
            resultado_dict = {
                'id': resultado.id,
                'nombre': resultado.nombre,
                'email': resultado.email,
                'categorias': resultado.categorias,
                'descripcion': resultado.descripcion,
                'biografia': resultado.biografia,
                'sitio_web': resultado.sitio_web,
                'telefono': resultado.telefono,
                'estado': resultado.estado.value if resultado.estado else None,
                'tipo': resultado.tipo.value if resultado.tipo else None,
                'fecha_creacion': resultado.fecha_creacion,
                'fecha_actualizacion': resultado.fecha_actualizacion
            }
            
            return Response(
                json.dumps(resultado_dict),
                status=200,
                mimetype='application/json'
            )
        finally:
            session_db.close()
            
    except InfluencerNoEncontrado as e:
        logger.warning(f"⚠️ API: Influencer no encontrado: {e}")
        return Response(
            json.dumps({"error": str(e)}),
            status=404,
            mimetype='application/json'
        )
    except Exception as e:
        logger.error(f"❌ API: Error interno: {e}", exc_info=True)
        return Response(
            json.dumps({"error": "Error interno del servidor"}),
            status=500,
            mimetype='application/json'
        )


@bp.route('/query/<influencer_id>', methods=('GET',))
def obtener_influencer_usando_query(influencer_id):
    """Obtiene un influencer por ID usando el patrón de queries."""
    try:
        logger.info(f"🔍 API: Obteniendo influencer con query - ID: {influencer_id}")
        
        query_resultado = ejecutar_query(ObtenerInfluencer(influencer_id))
        
        logger.info(f"✅ API: Influencer encontrado con query - ID: {influencer_id}")
        
        # Convertir resultado a diccionario para JSON
        resultado = query_resultado.resultado
        resultado_dict = {
            'id': resultado.id,
            'nombre': resultado.nombre,
            'email': resultado.email,
            'categorias': resultado.categorias,
            'descripcion': resultado.descripcion,
            'biografia': resultado.biografia,
            'sitio_web': resultado.sitio_web,
            'telefono': resultado.telefono,
            'estado': resultado.estado.value if resultado.estado else None,
            'tipo': resultado.tipo.value if resultado.tipo else None,
            'fecha_creacion': resultado.fecha_creacion,
            'fecha_actualizacion': resultado.fecha_actualizacion
        }
        
        return Response(
            json.dumps(resultado_dict),
            status=200,
            mimetype='application/json'
        )
        
    except InfluencerNoEncontrado as e:
        logger.warning(f"⚠️ API: Influencer no encontrado: {e}")
        return Response(
            json.dumps({"error": str(e)}),
            status=404,
            mimetype='application/json'
        )
    except Exception as e:
        logger.error(f"❌ API: Error interno: {e}", exc_info=True)
        return Response(
            json.dumps({"error": "Error interno del servidor"}),
            status=500,
            mimetype='application/json'
        )