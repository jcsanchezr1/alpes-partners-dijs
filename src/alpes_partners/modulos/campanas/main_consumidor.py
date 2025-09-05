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

from alpes_partners.modulos.campanas.infraestructura.consumidores.consumidor_eventos_influencers import ConsumidorEventosInfluencers

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
    
    logger.info("🚀 MAIN: Iniciando consumidor de eventos de influencers para campañas")
    logger.info("=" * 80)
    logger.info("📋 CONFIGURACIÓN:")
    logger.info(f"   🌐 PULSAR_ADDRESS: {os.getenv('PULSAR_ADDRESS', 'localhost')}")
    logger.info(f"   📊 Módulo: Campañas")
    logger.info(f"   🎯 Eventos: InfluencerRegistrado, InfluencerActivado, InfluencerDesactivado")
    logger.info("=" * 80)
    
    consumidor = None
    
    try:
        # Crear e inicializar consumidor
        consumidor = ConsumidorEventosInfluencers()
        
        # Conectar a Pulsar
        logger.info("🔄 MAIN: Conectando a Pulsar...")
        consumidor.conectar()
        
        # Configurar consumidores
        logger.info("🔄 MAIN: Configurando consumidores...")
        consumidor.configurar_consumidores()
        
        # Iniciar consumo
        logger.info("🎯 MAIN: Iniciando consumo de eventos...")
        logger.info("   💡 Presiona Ctrl+C para detener el consumidor")
        logger.info("=" * 80)
        
        consumidor.consumir_eventos()
        
    except KeyboardInterrupt:
        logger.info("🛑 MAIN: Deteniendo consumidor por solicitud del usuario")
        
    except Exception as e:
        logger.error(f"❌ MAIN: Error fatal: {e}")
        logger.error("   💡 Verifica que Pulsar esté ejecutándose y accesible")
        logger.error(f"   🌐 Host configurado: {os.getenv('PULSAR_ADDRESS', 'localhost')}")
        sys.exit(1)
        
    finally:
        if consumidor:
            logger.info("🔄 MAIN: Cerrando recursos...")
            consumidor.cerrar()
        
        logger.info("🏁 MAIN: Consumidor finalizado")


if __name__ == "__main__":
    main()
