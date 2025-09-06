"""
Consumidores de Apache Pulsar para eventos de influencers.
"""

import pulsar
import _pulsar  
from pulsar.schema import *
import uuid
import time
import logging

from alpes_partners.modulos.influencers.infraestructura.schema.v1.eventos import (
    EventoInfluencerRegistrado
)
from alpes_partners.modulos.influencers.infraestructura.schema.v1.comandos import (
    ComandoRegistrarInfluencer
)
from alpes_partners.seedwork.infraestructura import utils

logger = logging.getLogger(__name__)


def suscribirse_a_eventos_influencers():
    """
    Suscribirse a eventos de influencers desde Pulsar.
    Este consumidor puede ser usado por otros microservicios
    para reaccionar a eventos de influencers.
    """
    cliente = None
    try:
        logger.info("🔌 PULSAR: Conectando a eventos de influencers...")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        
        logger.info("PULSAR: Módulo de influencers NO se suscribe a sus propios eventos")
        logger.info("PULSAR: Los eventos son procesados por otros módulos (campanas, etc.)")
                
    except Exception as e:
        logger.error(f"PULSAR: Error en consumidor de eventos: {e}")
    finally:
        if cliente:
            cliente.close()


def suscribirse_a_comandos_influencers():
    """
    Suscribirse a comandos de influencers desde Pulsar.
    Este consumidor procesa comandos enviados desde otros servicios.
    """
    cliente = None
    try:
        logger.info("🔌 PULSAR: Conectando a comandos de influencers...")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        
        consumidor_comandos = cliente.subscribe(
            'comandos-influencers', 
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='alpes-partners-sub-comandos-influencers', 
            schema=AvroSchema(ComandoRegistrarInfluencer)
        )

        logger.info("PULSAR: Suscrito a comandos de influencers")
        
        while True:
            try:
                mensaje = consumidor_comandos.receive()
                logger.info(f"PULSAR: Comando recibido - {mensaje.value()}")
                
                # Procesar el comando aquí
                comando = mensaje.value()
                procesar_comando_influencer(comando)
                
                # Confirmar procesamiento
                consumidor_comandos.acknowledge(mensaje)
                logger.info("PULSAR: Comando procesado y confirmado")
                
            except Exception as e:
                logger.error(f"PULSAR: Error procesando comando: {e}")
                time.sleep(5)
                
    except Exception as e:
        logger.error(f"PULSAR: Error en consumidor de comandos: {e}")
    finally:
        if cliente:
            cliente.close()


def procesar_evento_influencer(evento):
    """
    Procesa eventos de influencers recibidos desde Pulsar.
    Aquí puedes implementar lógica de negocio que reaccione a eventos.
    """
    logger.info(f"PROCESANDO: Evento de influencer - Tipo: {type(evento).__name__}")
    
    if hasattr(evento, 'data'):
        data = evento.data
        logger.info(f"DATOS: {data}")
        
    logger.info("PROCESADO: Evento de influencer procesado exitosamente")


def procesar_comando_influencer(comando):
    """
    Procesa comandos de influencers recibidos desde Pulsar.
    Aquí puedes implementar lógica para ejecutar comandos remotos.
    """
    logger.info(f"PROCESANDO: Comando de influencer - Tipo: {type(comando).__name__}")
    
    if hasattr(comando, 'data'):
        data = comando.data
        logger.info(f"DATOS: {data}")
        
        # Ejemplo: Ejecutar comando usando el mediador local
        # from alpes_partners.seedwork.aplicacion.comandos import ejecutar_commando
        # ejecutar_commando(convertir_a_comando_local(comando))
        
    logger.info("PROCESADO: Comando de influencer procesado exitosamente")