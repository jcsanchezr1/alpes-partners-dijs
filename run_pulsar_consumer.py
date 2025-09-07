#!/usr/bin/env python3
"""
Script para ejecutar consumidores de Apache Pulsar.
"""

import sys
import os
import logging

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

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
    logger.info("PULSAR: El consumidor funcionará solo con campañas")



def main():
    """Ejecuta el consumidor de campañas para escuchar eventos de influencers."""
    logger.info("PULSAR: Iniciando consumidor de Apache Pulsar...")
    
    try:
        if suscribirse_a_eventos_influencers_desde_campanas is None:
            logger.error("PULSAR: No se pudo cargar el consumidor de campañas")
            sys.exit(1)
        
        logger.info("PULSAR: Iniciando consumidor de campañas...")
        logger.info("PULSAR: Escuchando eventos de influencers para procesamiento en campañas...")
        
        # Ejecutar directamente el consumidor de campañas
        suscribirse_a_eventos_influencers_desde_campanas()
        
    except KeyboardInterrupt:
        logger.info("PULSAR: Deteniendo consumidor...")
    except Exception as e:
        logger.error(f"PULSAR: Error en consumidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
