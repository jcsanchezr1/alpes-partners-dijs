"""
Handlers para eventos de influencers en el módulo de campañas.
Siguiendo principios DDD, estos handlers representan las reacciones del dominio
de campañas a eventos que ocurren en el dominio de influencers.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..comandos.crear_campana import CrearCampanaPorCategoria
from .crear_campana_handler import CrearCampanaPorCategoriaHandler

logger = logging.getLogger(__name__)


class HandlerEventosInfluencers:
    """
    Handler que procesa eventos de influencers desde la perspectiva del dominio de campañas.
    
    En DDD, este handler representa cómo el bounded context de Campañas
    reacciona a eventos que ocurren en el bounded context de Influencers.
    """
    
    def __init__(self, uow):
        """Inicializa el handler de eventos de influencers con UoW como influencers."""
        self.uow = uow
        self.crear_campana_handler = CrearCampanaPorCategoriaHandler(uow.repositorio_campanas)
        logger.info("🎯 CAMPAÑAS: Handler de eventos de influencers inicializado con UoW")
    
    def handle_influencer_registrado(self, evento_data: Dict[str, Any]) -> None:
        """
        Maneja el evento de influencer registrado.
        
        Desde la perspectiva de campañas, cuando un influencer se registra:
        - Podríamos crear un perfil de influencer para campañas
        - Podríamos evaluar si cumple criterios para campañas automáticas
        - Podríamos notificar a los gestores de campañas
        """
        logger.info("📢 CAMPAÑAS: Procesando evento InfluencerRegistrado")
        logger.info(f"   📋 ID Influencer: {evento_data.get('id_influencer')}")
        logger.info(f"   👤 Nombre: {evento_data.get('nombre')}")
        logger.info(f"   📧 Email: {evento_data.get('email')}")
        logger.info(f"   🏷️ Categorías: {evento_data.get('categorias', [])}")
        logger.info(f"   📅 Fecha Registro: {evento_data.get('fecha_registro')}")
        
        # Crear campañas automáticamente basadas en las categorías del influencer
        self._crear_campañas_automaticas(evento_data)
        
        logger.info("✅ CAMPAÑAS: Evento InfluencerRegistrado procesado exitosamente")
    
    def handle_influencer_activado(self, evento_data: Dict[str, Any]) -> None:
        """
        Maneja el evento de influencer activado.
        
        Desde campañas, cuando un influencer se activa:
        - Podríamos habilitarlo para participar en campañas
        - Podríamos notificar sobre disponibilidad
        """
        logger.info("📢 CAMPAÑAS: Procesando evento InfluencerActivado")
        logger.info(f"   📋 ID Influencer: {evento_data.get('id_influencer')}")
        logger.info(f"   👤 Nombre: {evento_data.get('nombre')}")
        logger.info(f"   📅 Fecha Activación: {evento_data.get('fecha_activacion')}")
        
        # Lógica de dominio para activación
        self._habilitar_para_campañas(evento_data)
        
        logger.info("✅ CAMPAÑAS: Evento InfluencerActivado procesado exitosamente")
    
    def handle_influencer_desactivado(self, evento_data: Dict[str, Any]) -> None:
        """
        Maneja el evento de influencer desactivado.
        
        Desde campañas, cuando un influencer se desactiva:
        - Podríamos suspender campañas activas
        - Podríamos buscar reemplazos
        """
        logger.info("📢 CAMPAÑAS: Procesando evento InfluencerDesactivado")
        logger.info(f"   📋 ID Influencer: {evento_data.get('id_influencer')}")
        logger.info(f"   👤 Nombre: {evento_data.get('nombre')}")
        logger.info(f"   ⚠️ Motivo: {evento_data.get('motivo')}")
        logger.info(f"   📅 Fecha Desactivación: {evento_data.get('fecha_desactivacion')}")
        
        # Lógica de dominio para desactivación
        self._suspender_campañas_activas(evento_data)
        
        logger.info("✅ CAMPAÑAS: Evento InfluencerDesactivado procesado exitosamente")
    
    def _crear_campañas_automaticas(self, evento_data: Dict[str, Any]) -> None:
        """Crea campañas automáticamente basadas en las categorías del influencer."""
        try:
            # Extraer datos del evento
            influencer_id = evento_data.get('id_influencer')
            nombre_influencer = evento_data.get('nombre')
            email_influencer = evento_data.get('email')
            categorias = evento_data.get('categorias', [])
            fecha_registro_str = evento_data.get('fecha_registro')
            
            # Convertir fecha si es string
            if isinstance(fecha_registro_str, str):
                try:
                    fecha_registro = datetime.fromisoformat(fecha_registro_str.replace('Z', '+00:00'))
                except:
                    fecha_registro = datetime.utcnow()
            else:
                fecha_registro = fecha_registro_str or datetime.utcnow()
            
            if not influencer_id or not nombre_influencer or not categorias:
                logger.warning("⚠️ CAMPAÑAS: Datos insuficientes para crear campañas automáticas")
                return
            
            logger.info(f"🤖 CAMPAÑAS: Iniciando creación automática de campañas para {nombre_influencer}")
            logger.info(f"   📋 Categorías a procesar: {categorias}")
            
            # Crear comando para generar campañas por categoría
            comando = CrearCampanaPorCategoria(
                influencer_id=influencer_id,
                nombre_influencer=nombre_influencer,
                email_influencer=email_influencer,
                categorias_influencer=categorias,
                fecha_registro_influencer=fecha_registro
            )
            
            # Ejecutar creación de campañas usando UoW (como influencers)
            campanas_creadas = self.crear_campana_handler.handle(comando)
            
            # La UoW se encarga del commit automáticamente
            
            logger.info(f"🎉 CAMPAÑAS: {len(campanas_creadas)} campañas automáticas creadas y persistidas exitosamente")
            logger.info(f"   📋 IDs de campañas: {campanas_creadas}")
            
        except Exception as e:
            logger.error(f"❌ CAMPAÑAS: Error creando campañas automáticas: {e}")
            # No re-lanzar la excepción para no afectar el procesamiento del evento principal
        
    def _habilitar_para_campañas(self, evento_data: Dict[str, Any]) -> None:
        """Habilita al influencer para participar en campañas."""
        logger.info(f"   ✅ CAMPAÑAS: Habilitando influencer para campañas activas")
        # Lógica para habilitar en campañas
        
    def _suspender_campañas_activas(self, evento_data: Dict[str, Any]) -> None:
        """Suspende las campañas activas del influencer."""
        logger.info(f"   ⏸️ CAMPAÑAS: Suspendiendo campañas activas del influencer")
        # Lógica para suspender campañas
