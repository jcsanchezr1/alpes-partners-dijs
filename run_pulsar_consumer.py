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
suscribirse_a_eventos_influencers_desde_campañas = None

try:
    logger.info("🔍 PULSAR: Intentando importar módulo de campañas...")
    logger.info("🔍 PULSAR: Paso 1 - Importando consumidores...")
    from alpes_partners.modulos.campanas.infraestructura.consumidores import suscribirse_a_eventos_influencers_desde_campañas
    logger.info("✅ PULSAR: Módulo de campañas importado exitosamente")
except ImportError as e:
    logger.error(f"❌ PULSAR: Error detallado importando campañas: {e}")
    logger.error(f"❌ PULSAR: Tipo de error: {type(e).__name__}")
    import traceback
    logger.error(f"❌ PULSAR: Traceback completo:\n{traceback.format_exc()}")
    logger.info("💡 PULSAR: El consumidor funcionará solo con influencers")



def ejecutar_consumidor_campañas():
    """Ejecuta el consumidor de campañas."""
    if suscribirse_a_eventos_influencers_desde_campañas is None:
        logger.warning("⚠️ PULSAR: Consumidor de campañas no disponible - módulo no importado")
        return
    
    try:
        logger.info("🚀 PULSAR: Iniciando consumidor de campañas...")
        suscribirse_a_eventos_influencers_desde_campañas()
    except Exception as e:
        logger.error(f"❌ PULSAR: Error en consumidor de campañas: {e}")


def main():
    """Ejecuta los consumidores de Pulsar en threads separados."""
    logger.info("🚀 PULSAR: Iniciando consumidores de Apache Pulsar...")
    
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
        
        thread_eventos_campañas = threading.Thread(
            target=ejecutar_consumidor_campañas,
            name="EventosCampañas",
            daemon=True
        )
        
        # Iniciar threads
        thread_eventos_influencers.start()
        thread_comandos_influencers.start()
        thread_eventos_campañas.start()
        
        logger.info("✅ PULSAR: Consumidores iniciados exitosamente")
        logger.info("📡 PULSAR: Escuchando eventos y comandos...")
        logger.info("   🔹 Influencers: eventos y comandos")
        logger.info("   🔹 Campañas: eventos de influencers")
        
        # Mantener el proceso principal vivo
        try:
            thread_eventos_influencers.join()
            thread_comandos_influencers.join()
            thread_eventos_campañas.join()
        except KeyboardInterrupt:
            logger.info("🛑 PULSAR: Deteniendo consumidores...")
            
    except Exception as e:
        logger.error(f"❌ PULSAR: Error iniciando consumidores: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
