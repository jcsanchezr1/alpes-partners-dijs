"""
Handlers para comandos y eventos del módulo de campanas.
Siguiendo principios DDD y el patrón establecido en influencers.
"""

import logging
from typing import List, Optional

from alpes_partners.seedwork.aplicacion.handlers import ManejadorComando
from alpes_partners.seedwork.infraestructura.uow import UnidadTrabajo
from alpes_partners.modulos.campanas.dominio.repositorios import RepositorioCampanas
from alpes_partners.modulos.campanas.dominio.entidades import Campana
from alpes_partners.modulos.campanas.dominio.excepciones import CampanaYaExisteExcepcion

from alpes_partners.modulos.campanas.aplicacion.comandos.crear_campana import RegistrarCampana

logger = logging.getLogger(__name__)


# ============= COMMAND HANDLERS =============

class ManejadorRegistrarCampana(ManejadorComando[RegistrarCampana]):
    """Handler para registrar una campana."""
    
    def __init__(self, repositorio: RepositorioCampanas, uow: UnidadTrabajo):
        self.repositorio = repositorio
        self.uow = uow
    
    def handle(self, comando: RegistrarCampana) -> None:
        logger.info(f"HANDLER: Iniciando registro de campana - Nombre: {comando.nombre}")
        
        # Verificar si el nombre ya existe
        logger.info(f"HANDLER: Verificando si nombre existe: {comando.nombre}")
        if self.repositorio.existe_con_nombre(comando.nombre):
            logger.warning(f"HANDLER: Nombre ya registrado: {comando.nombre}")
            raise CampanaYaExisteExcepcion(f"Ya existe una campana con el nombre {comando.nombre}")
        
        logger.info(f"HANDLER: Nombre disponible: {comando.nombre}")
        
        # Crear entidad campana usando la fábrica
        logger.info(f"HANDLER: Creando entidad campana...")
        from alpes_partners.modulos.campanas.aplicacion.dto import RegistrarCampanaDTO
        from alpes_partners.modulos.campanas.aplicacion.mapeadores import MapeadorCampana
        from alpes_partners.modulos.campanas.dominio.fabricas import FabricaCampanas
        
        # Convertir comando a DTO
        campana_dto = RegistrarCampanaDTO(
            fecha_actualizacion=comando.fecha_actualizacion,
            fecha_creacion=comando.fecha_creacion,
            id=comando.id,
            nombre=comando.nombre,
            descripcion=comando.descripcion,
            tipo_comision=comando.tipo_comision,
            valor_comision=comando.valor_comision,
            moneda=comando.moneda,
            fecha_inicio=comando.fecha_inicio,
            fecha_fin=comando.fecha_fin,
            titulo_material=comando.titulo_material,
            descripcion_material=comando.descripcion_material,
            categorias_objetivo=comando.categorias_objetivo or [],
            tipos_afiliado_permitidos=comando.tipos_afiliado_permitidos or [],
            paises_permitidos=comando.paises_permitidos or [],
            enlaces_material=comando.enlaces_material or [],
            imagenes_material=comando.imagenes_material or [],
            banners_material=comando.banners_material or [],
            metricas_minimas=comando.metricas_minimas or {},
            auto_activar=comando.auto_activar,
            influencer_origen_id=comando.influencer_origen_id,
            categoria_origen=comando.categoria_origen
        )
        
        # Crear campana usando la fábrica
        fabrica_campanas = FabricaCampanas()
        campana: Campana = fabrica_campanas.crear_objeto(campana_dto, MapeadorCampana())
        
        logger.info(f"HANDLER: Campana creada - ID: {campana.id}, Eventos: {len(campana.eventos)}")
        
        # Agregar al repositorio usando UoW
        logger.info(f"HANDLER: Registrando operación en UoW...")
        self.uow.registrar_batch(self.repositorio.agregar, campana)
        logger.info(f"HANDLER: Operación registrada en UoW")
        
        # Los eventos se publican automáticamente por la UoW
        # Limpiar eventos después del registro
        campana.limpiar_eventos()
        
        logger.info(f"HANDLER: Handler completado - Campana ID: {campana.id}")


logger.info("HANDLERS: Handlers de aplicación de campanas cargados")
