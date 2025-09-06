#!/usr/bin/env python3
"""
Script para ejecutar consumidores de Apache Pulsar.
"""

import sys
import os
import logging
import threading

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from alpes_partners.modulos.influencers.infraestructura.consumidores import (
    suscribirse_a_eventos_influencers,
    suscribirse_a_comandos_influencers
)
# Configurar logging primero
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Import con manejo robusto para Docker
suscribirse_a_eventos_influencers_desde_campanas = None

try:
    logger.info("PULSAR: Intentando importar módulo de campanas...")
    logger.info("PULSAR: Paso 1 - Importando consumidores...")
    from alpes_partners.modulos.campanas.infraestructura.consumidores import suscribirse_a_eventos_influencers_desde_campanas
    logger.info("PULSAR: Módulo de campanas importado exitosamente")
except ImportError as e:
    logger.error(f"PULSAR: Error detallado importando campanas: {e}")
    logger.error(f"PULSAR: Tipo de error: {type(e).__name__}")
    import traceback
    logger.error(f"PULSAR: Traceback completo:\n{traceback.format_exc()}")
    logger.info("PULSAR: El consumidor funcionará solo con influencers")



def ejecutar_consumidor_campanas():
    """Ejecuta el consumidor de campanas."""
    if suscribirse_a_eventos_influencers_desde_campanas is None:
        logger.warning("PULSAR: Consumidor de campanas no disponible - módulo no importado")
        return
    
    try:
        logger.info("PULSAR: Iniciando consumidor de campanas...")
        suscribirse_a_eventos_influencers_desde_campanas()
    except Exception as e:
        logger.error(f"PULSAR: Error en consumidor de campanas: {e}")


def main():
    """Ejecuta los consumidores de Pulsar en threads separados."""
    logger.info("PULSAR: Iniciando consumidores de Apache Pulsar...")
    
    try:
        # Crear threads para cada consumidor
        thread_eventos_influencers = threading.Thread(
            target=suscribirse_a_eventos_influencers,
            name="EventosInfluencers",
            daemon=True
        )
        
        thread_comandos_influencers = threading.Thread(
            target=suscribirse_a_comandos_influencers,
            name="ComandosInfluencers",
            daemon=True
        )
        
        thread_eventos_campanas = threading.Thread(
            target=ejecutar_consumidor_campanas,
            name="EventosCampanas",
            daemon=True
        )
        
        # Iniciar threads
        thread_eventos_influencers.start()
        thread_comandos_influencers.start()
        thread_eventos_campanas.start()
        
        logger.info("PULSAR: Consumidores iniciados exitosamente")
        logger.info("PULSAR: Escuchando eventos y comandos...")
        logger.info("Influencers: eventos y comandos")
        logger.info("Campanas: eventos de influencers")
        
        # Mantener el proceso principal vivo
        try:
            thread_eventos_influencers.join()
            thread_comandos_influencers.join()
            thread_eventos_campanas.join()
        except KeyboardInterrupt:
            logger.info("PULSAR: Deteniendo consumidores...")
            
    except Exception as e:
        logger.error(f"PULSAR: Error iniciando consumidores: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
