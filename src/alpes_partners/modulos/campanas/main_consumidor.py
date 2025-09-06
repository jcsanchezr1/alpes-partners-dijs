"""
Script principal para ejecutar el consumidor de eventos de influencers.
Implementación mejorada siguiendo principios DDD.

Uso:
    python -m alpes_partners.modulos.campanas.main_consumidor
"""

import logging
import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importaciones
src_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_path))

from alpes_partners.modulos.campanas.infraestructura.consumidores import suscribirse_a_eventos_influencers_desde_campanas

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Función principal del consumidor de eventos.
    
    Implementación mejorada que:
    1. Maneja errores de conexión
    2. Permite reintentos
    3. Logging estructurado
    4. Cierre limpio de recursos
    """
    
    logger.info("🚀 MAIN: Iniciando consumidor de eventos de influencers para campanas")
    logger.info("=" * 80)
    logger.info("📋 CONFIGURACIÓN:")
    logger.info(f"   🌐 PULSAR_ADDRESS: {os.getenv('PULSAR_ADDRESS', 'localhost')}")
    logger.info(f"   📊 Módulo: Campanas")
    logger.info(f"   🎯 Eventos: InfluencerRegistrado")
    logger.info("=" * 80)
    
    try:
        # Iniciar consumo de eventos
        logger.info("🎯 MAIN: Iniciando consumo de eventos...")
        logger.info("   💡 Presiona Ctrl+C para detener el consumidor")
        logger.info("=" * 80)
        
        suscribirse_a_eventos_influencers_desde_campanas()
        
    except KeyboardInterrupt:
        logger.info("🛑 MAIN: Deteniendo consumidor por solicitud del usuario")
        
    except Exception as e:
        logger.error(f"❌ MAIN: Error fatal: {e}")
        logger.error("   💡 Verifica que Pulsar esté ejecutándose y accesible")
        logger.error(f"   🌐 Host configurado: {os.getenv('PULSAR_ADDRESS', 'localhost')}")
        sys.exit(1)
        
    finally:
        logger.info("🏁 MAIN: Consumidor finalizado")


if __name__ == "__main__":
    main()
