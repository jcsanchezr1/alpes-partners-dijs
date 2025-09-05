"""
Handler para los comandos de creación de campañas.
"""

import logging
from typing import List
from datetime import datetime

from alpes_partners.seedwork.aplicacion.handlers import ManejadorComando
from alpes_partners.seedwork.dominio.excepciones import ExcepcionReglaDeNegocio
from ..comandos.crear_campana import CrearCampana, CrearCampanaPorCategoria
from alpes_partners.modulos.campanas.dominio.entidades import Campaña
from alpes_partners.modulos.campanas.dominio.repositorios import RepositorioCampanas
from alpes_partners.modulos.campanas.dominio.objetos_valor import TipoComision
from alpes_partners.modulos.campanas.dominio.plantillas_campanas import GeneradorCampanasPorCategoria

logger = logging.getLogger(__name__)


class CrearCampanaHandler(ManejadorComando):
    """Handler para crear una campaña individual."""
    
    def __init__(self, repositorio_campanas: RepositorioCampanas):
        self.repositorio_campanas = repositorio_campanas
    
    def handle(self, comando: CrearCampana) -> str:
        """Maneja el comando de crear campaña."""
        logger.info(f"🎯 CAMPAÑAS: Creando campaña '{comando.nombre}'")
        
        # Validar que no exista una campaña con el mismo nombre
        if self.repositorio_campanas.existe_con_nombre(comando.nombre):
            raise ExcepcionReglaDeNegocio(f"Ya existe una campaña con el nombre '{comando.nombre}'")
        
        # Convertir tipo de comisión
        try:
            tipo_comision = TipoComision(comando.tipo_comision.lower())
        except ValueError:
            raise ExcepcionReglaDeNegocio(f"Tipo de comisión inválido: {comando.tipo_comision}")
        
        # Crear la campaña usando el factory method
        campaña = Campaña.crear(
            nombre=comando.nombre,
            descripcion=comando.descripcion,
            tipo_comision=tipo_comision,
            valor_comision=comando.valor_comision,
            moneda=comando.moneda,
            fecha_inicio=comando.fecha_inicio,
            fecha_fin=comando.fecha_fin,
            titulo_material=comando.titulo_material,
            descripcion_material=comando.descripcion_material,
            categorias_objetivo=comando.categorias_objetivo,
            tipos_afiliado_permitidos=comando.tipos_afiliado_permitidos
        )
        
        # Actualizar material promocional con enlaces e imágenes adicionales
        if comando.enlaces_material or comando.imagenes_material or comando.banners_material:
            from alpes_partners.modulos.campanas.dominio.objetos_valor import MaterialPromocional
            material_actualizado = MaterialPromocional(
                titulo=campaña.material_promocional.titulo,
                descripcion=campaña.material_promocional.descripcion,
                enlaces=comando.enlaces_material,
                imagenes=comando.imagenes_material,
                banners=comando.banners_material
            )
            campaña.material_promocional = material_actualizado
        
        # Actualizar criterios de afiliado con países y métricas
        if comando.paises_permitidos or comando.metricas_minimas:
            from alpes_partners.modulos.campanas.dominio.objetos_valor import CriteriosAfiliado
            criterios_actualizados = CriteriosAfiliado(
                tipos_permitidos=campaña.criterios_afiliado.tipos_permitidos,
                categorias_requeridas=campaña.criterios_afiliado.categorias_requeridas,
                paises_permitidos=comando.paises_permitidos,
                metricas_minimas=comando.metricas_minimas
            )
            campaña.criterios_afiliado = criterios_actualizados
        
        # Auto-activar si se solicita
        if comando.auto_activar:
            try:
                campaña.activar()
                logger.info(f"✅ CAMPAÑAS: Campaña '{comando.nombre}' activada automáticamente")
            except Exception as e:
                logger.warning(f"⚠️ CAMPAÑAS: No se pudo activar automáticamente la campaña: {e}")
        
        # Guardar en repositorio
        self.repositorio_campanas.agregar(campaña)
        
        logger.info(f"✅ CAMPAÑAS: Campaña '{comando.nombre}' creada exitosamente con ID: {campaña.id}")
        
        # Log adicional para campañas automáticas
        if comando.influencer_origen_id:
            logger.info(f"🤖 CAMPAÑAS: Campaña automática creada para influencer {comando.influencer_origen_id} en categoría {comando.categoria_origen}")
        
        return campaña.id


class CrearCampanaPorCategoriaHandler(ManejadorComando):
    """Handler para crear campañas automáticamente basadas en categorías de influencers."""
    
    def __init__(self, repositorio_campanas: RepositorioCampanas):
        self.repositorio_campanas = repositorio_campanas
        self.crear_campana_handler = CrearCampanaHandler(repositorio_campanas)
    
    def handle(self, comando: CrearCampanaPorCategoria) -> List[str]:
        """Maneja el comando de crear campañas por categoría."""
        logger.info(f"🤖 CAMPAÑAS: Creando campañas automáticas para influencer {comando.nombre_influencer}")
        logger.info(f"📋 CAMPAÑAS: Categorías del influencer: {comando.categorias_influencer}")
        
        campanas_creadas = []
        
        # Generar campañas para cada categoría
        campanas_data = GeneradorCampanasPorCategoria.generar_campanas_para_influencer(
            influencer_id=comando.influencer_id,
            nombre_influencer=comando.nombre_influencer,
            categorias=comando.categorias_influencer
        )
        
        for campana_data in campanas_data:
            try:
                # Crear comando individual
                comando_crear = CrearCampana(
                    nombre=campana_data['nombre'],
                    descripcion=campana_data['descripcion'],
                    tipo_comision=campana_data['tipo_comision'],
                    valor_comision=campana_data['valor_comision'],
                    moneda=campana_data['moneda'],
                    fecha_inicio=campana_data['fecha_inicio'],
                    fecha_fin=campana_data['fecha_fin'],
                    titulo_material=campana_data['titulo_material'],
                    descripcion_material=campana_data['descripcion_material'],
                    categorias_objetivo=campana_data['categorias_objetivo'],
                    tipos_afiliado_permitidos=campana_data['tipos_afiliado_permitidos'],
                    enlaces_material=campana_data['enlaces_material'],
                    imagenes_material=campana_data['imagenes_material'],
                    metricas_minimas=campana_data['metricas_minimas'],
                    auto_activar=campana_data['auto_activar'],
                    influencer_origen_id=campana_data['influencer_origen_id'],
                    categoria_origen=campana_data['categoria_origen']
                )
                
                # Ejecutar creación
                campaña_id = self.crear_campana_handler.handle(comando_crear)
                campanas_creadas.append(campaña_id)
                
                logger.info(f"✅ CAMPAÑAS: Campaña automática creada: {campana_data['nombre']} (ID: {campaña_id})")
                
            except Exception as e:
                logger.error(f"❌ CAMPAÑAS: Error creando campaña para categoría {campana_data['categoria_origen']}: {e}")
                # Continuar con las demás campañas aunque una falle
                continue
        
        logger.info(f"🎉 CAMPAÑAS: Proceso completado. {len(campanas_creadas)} campañas creadas para {comando.nombre_influencer}")
        
        return campanas_creadas
