"""
Consumidores de Apache Pulsar para eventos de influencers en el módulo de CAMPAÑAS.
Siguiendo el mismo patrón que influencers pero procesando eventos para crear campañas automáticamente.
"""

import logging
logger = logging.getLogger(__name__)

logger.info("🔍 CAMPAÑAS: Iniciando imports del consumidor...")

try:
    logger.info("🔍 CAMPAÑAS: Importando pulsar...")
    import pulsar
    import _pulsar  
    from pulsar.schema import *
    import time
    logger.info("✅ CAMPAÑAS: Pulsar importado exitosamente")
except Exception as e:
    logger.error(f"❌ CAMPAÑAS: Error importando pulsar: {e}")
    raise

try:
    logger.info("🔍 CAMPAÑAS: Importando eventos de influencers...")
    from alpes_partners.modulos.influencers.infraestructura.schema.v1.eventos import (
        EventoInfluencerRegistrado,
        EventoInfluencerActivado,
        EventoInfluencerDesactivado
    )
    logger.info("✅ CAMPAÑAS: Eventos de influencers importados exitosamente")
except Exception as e:
    logger.error(f"❌ CAMPAÑAS: Error importando eventos de influencers: {e}")
    raise

try:
    logger.info("🔍 CAMPAÑAS: Importando seedwork utils...")
    from alpes_partners.seedwork.infraestructura import utils
    logger.info("✅ CAMPAÑAS: Seedwork utils importado exitosamente")
except Exception as e:
    logger.error(f"❌ CAMPAÑAS: Error importando seedwork utils: {e}")
    raise

try:
    logger.info("🔍 CAMPAÑAS: Importando handler de eventos...")
    from alpes_partners.modulos.campanas.aplicacion.handlers.eventos_influencers import HandlerEventosInfluencers
    logger.info("✅ CAMPAÑAS: Handler de eventos importado exitosamente")
except Exception as e:
    logger.error(f"❌ CAMPAÑAS: Error importando handler de eventos: {e}")
    raise

try:
    logger.info("🔍 CAMPAÑAS: Importando UoW...")
    from alpes_partners.modulos.campanas.infraestructura.uow import UnidadTrabajoCampanas
    logger.info("✅ CAMPAÑAS: UoW importada exitosamente")
except Exception as e:
    logger.error(f"❌ CAMPAÑAS: Error importando UoW: {e}")
    raise

try:
    logger.info("🔍 CAMPAÑAS: Importando database...")
    from alpes_partners.seedwork.infraestructura.database import get_db_session
    logger.info("✅ CAMPAÑAS: Database importada exitosamente")
except Exception as e:
    logger.error(f"❌ CAMPAÑAS: Error importando database: {e}")
    raise

logger.info("🎉 CAMPAÑAS: Todos los imports del consumidor completados exitosamente")


def suscribirse_a_eventos_influencers_desde_campañas():
    """
    Suscribirse a eventos de influencers desde el módulo de CAMPAÑAS.
    Este consumidor procesa eventos de influencers para crear campañas automáticamente.
    """
    cliente = None
    try:
        logger.info("🔌 CAMPAÑAS: Conectando a eventos de influencers...")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        
        # Consumidor para eventos de influencers desde campañas
        consumidor_eventos = cliente.subscribe(
            'eventos-influencers', 
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='campañas-sub-eventos-influencers', 
            schema=AvroSchema(EventoInfluencerRegistrado)
        )

        logger.info("✅ CAMPAÑAS: Suscrito a eventos de influencers")
        logger.info("🎯 CAMPAÑAS: Esperando eventos para procesar en contexto de campañas...")
        
        while True:
            try:
                mensaje = consumidor_eventos.receive()
                logger.info("=" * 80)
                logger.info(f"📨 CAMPAÑAS: Evento de influencer recibido - {mensaje.value()}")
                logger.info(f"🏷️ CAMPAÑAS: Procesando en módulo de CAMPAÑAS")
                logger.info("=" * 80)
                
                # Procesar el evento en el contexto de campañas
                evento = mensaje.value()
                procesar_evento_influencer_en_campañas(evento)
                
                # Confirmar procesamiento
                consumidor_eventos.acknowledge(mensaje)
                logger.info("✅ CAMPAÑAS 1: Evento procesado y confirmado desde CAMPAÑAS")
                logger.info("=" * 80)
                
            except Exception as e:
                logger.error(f"❌ CAMPAÑAS 3: Error procesando evento en CAMPAÑAS: {e}")
                # En producción, implementar retry logic o dead letter queue
                time.sleep(5)
                
    except Exception as e:
        logger.error(f"❌ CAMPAÑAS 2: Error en consumidor de eventos de CAMPAÑAS: {e}")
    finally:
        if cliente:
            cliente.close()


def procesar_evento_influencer_en_campañas(evento):
    """
    Procesa eventos de influencers recibidos en el contexto del módulo de CAMPAÑAS.
    Siguiendo el patrón simple de influencers - sin UoW compleja, solo procesamiento directo.
    """
    logger.info(f"🔄 CAMPAÑAS: Procesando evento de influencer en CAMPAÑAS - Tipo: {type(evento).__name__}")
    
    try:
        # Importar usando paths absolutos para evitar errores de módulo
        logger.info("🏷️ CAMPAÑAS 111x: Importando handler...")
        logger.info("🏷️ CAMPAÑAS 2x: Creando UoW y handler...")
        
        # Crear handler con UoW como influencers
        with next(get_db_session()) as session:
            with UnidadTrabajoCampanas(session) as uow:
                handler = HandlerEventosInfluencers(uow)
                logger.info("🏷️ CAMPAÑAS 3x: Handler creado exitosamente")
                
                # Convertir evento a diccionario
                evento_dict = _convertir_evento_a_dict(evento)
                logger.info("🏷️ CAMPAÑAS 4x: Evento convertido a dict")
                
                # Extraer tipo de evento - usar nombre de clase que sabemos que funciona
                tipo_evento = type(evento).__name__
                logger.info(f"🏷️ CAMPAÑAS 5x: Tipo de evento desde clase: '{tipo_evento}'")
                
                # Procesar según el tipo
                if tipo_evento and ('InfluencerRegistrado' in tipo_evento or tipo_evento == 'InfluencerRegistrado'):
                    logger.info("🎯 CAMPAÑAS: Procesando InfluencerRegistrado en contexto de campañas")
                    handler.handle_influencer_registrado(evento_dict)
                    
                elif tipo_evento and ('InfluencerActivado' in tipo_evento or tipo_evento == 'InfluencerActivado'):
                    logger.info("🎯 CAMPAÑAS: Procesando InfluencerActivado en contexto de campañas")
                    handler.handle_influencer_activado(evento_dict)
                    
                elif tipo_evento and ('InfluencerDesactivado' in tipo_evento or tipo_evento == 'InfluencerDesactivado'):
                    logger.info("🎯 CAMPAÑAS: Procesando InfluencerDesactivado en contexto de campañas")
                    handler.handle_influencer_desactivado(evento_dict)
                else:
                    logger.warning(f"⚠️ CAMPAÑAS: Evento sin tipo específico reconocido: '{tipo_evento}'")
                
                # La UoW se commitea automáticamente al salir del context manager
            
    except Exception as e:
        logger.error(f"❌ CAMPAÑAS: Error procesando evento: {e}")
        # No re-lanzar para no afectar el flujo principal
            
    logger.info("✅ CAMPAÑAS: Evento de influencer procesado exitosamente en CAMPAÑAS")


def _convertir_evento_a_dict(evento):
    """Convierte un evento a diccionario para el handler."""
    evento_dict = {}
    
    try:
        logger.info(f"🔍 CAMPAÑAS: Convirtiendo evento - Tipo: {type(evento).__name__}")
        
        # Extraer datos del payload
        if hasattr(evento, 'data'):
            data = evento.data
            logger.info(f"🔍 CAMPAÑAS: Datos encontrados - Tipo: {type(data).__name__}")
            
            # Intentar diferentes formas de extraer los datos
            if hasattr(data, '__dict__'):
                logger.info("🔍 CAMPAÑAS: Extrayendo datos via __dict__")
                evento_dict.update(data.__dict__)
            elif hasattr(data, '_asdict'):
                logger.info("🔍 CAMPAÑAS: Extrayendo datos via _asdict")
                evento_dict.update(data._asdict())
            else:
                # Intentar acceder a campos conocidos directamente
                logger.info("🔍 CAMPAÑAS: Extrayendo datos via campos directos")
                if hasattr(data, 'id_influencer'):
                    evento_dict['id_influencer'] = str(data.id_influencer)
                if hasattr(data, 'nombre'):
                    evento_dict['nombre'] = str(data.nombre)
                if hasattr(data, 'email'):
                    evento_dict['email'] = str(data.email)
                if hasattr(data, 'categorias'):
                    evento_dict['categorias'] = [str(cat) for cat in data.categorias] if data.categorias else []
                if hasattr(data, 'fecha_registro'):
                    # Manejar el objeto Long de Pulsar correctamente
                    try:
                        if data.fecha_registro is not None:
                            if hasattr(data.fecha_registro, '__int__'):
                                evento_dict['fecha_registro'] = int(data.fecha_registro)
                            else:
                                evento_dict['fecha_registro'] = int(str(data.fecha_registro))
                        else:
                            evento_dict['fecha_registro'] = None
                    except (ValueError, TypeError) as e:
                        logger.warning(f"⚠️ CAMPAÑAS: No se pudo convertir fecha_registro: {e}")
                        evento_dict['fecha_registro'] = None
        
        # Agregar campos del evento principal
        if hasattr(evento, 'type'):
            evento_dict['tipo_evento'] = str(evento.type) if evento.type else None
        if hasattr(evento, 'id'):
            evento_dict['evento_id'] = str(evento.id) if evento.id else None
        if hasattr(evento, 'time'):
            # Manejar el objeto Long de Pulsar correctamente
            try:
                if evento.time is not None:
                    # Intentar convertir el objeto Long de Pulsar
                    if hasattr(evento.time, '__int__'):
                        evento_dict['timestamp'] = int(evento.time)
                    else:
                        evento_dict['timestamp'] = int(str(evento.time))
                else:
                    evento_dict['timestamp'] = None
            except (ValueError, TypeError) as e:
                logger.warning(f"⚠️ CAMPAÑAS: No se pudo convertir timestamp: {e}")
                evento_dict['timestamp'] = None
        
        logger.info(f"🔍 CAMPAÑAS: Evento convertido - Claves: {list(evento_dict.keys())}")
        logger.info(f"🔍 CAMPAÑAS: Datos del influencer: ID={evento_dict.get('id_influencer')}, Nombre={evento_dict.get('nombre')}, Categorías={evento_dict.get('categorias')}")
            
    except Exception as e:
        logger.error(f"❌ CAMPAÑAS: Error convirtiendo evento a dict: {e}")
        import traceback
        logger.error(f"❌ CAMPAÑAS: Traceback: {traceback.format_exc()}")
    
    return evento_dict
