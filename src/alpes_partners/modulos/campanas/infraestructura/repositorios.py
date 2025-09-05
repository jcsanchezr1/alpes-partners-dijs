"""
Implementación de repositorios para campañas usando SQLAlchemy.
"""

import json
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

logger = logging.getLogger(__name__)

from alpes_partners.modulos.campanas.dominio.repositorios import RepositorioCampanas
from alpes_partners.modulos.campanas.dominio.entidades import Campaña
from alpes_partners.modulos.campanas.dominio.objetos_valor import (
    TipoComision, EstadoCampaña, TerminosComision, PeriodoCampaña,
    MaterialPromocional, CriteriosAfiliado, MetricasCampaña
)
from alpes_partners.seedwork.dominio.objetos_valor import Dinero
from .schema.campanas import Campanas as CampanaSchema, EstadoCampanaEnum, TipoComisionEnum


class RepositorioCampanasSQLAlchemy(RepositorioCampanas):
    """Implementación del repositorio de campañas usando SQLAlchemy."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def obtener_por_id(self, campaña_id: str) -> Optional[Campaña]:
        """Obtiene una campaña por su ID."""
        schema = self.session.query(CampanaSchema).filter(CampanaSchema.id == campaña_id).first()
        if schema:
            return self._schema_a_entidad(schema)
        return None
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Campaña]:
        """Obtiene una campaña por su nombre."""
        schema = self.session.query(CampanaSchema).filter(CampanaSchema.nombre == nombre).first()
        if schema:
            return self._schema_a_entidad(schema)
        return None
    
    def obtener_activas(self) -> List[Campaña]:
        """Obtiene todas las campañas activas."""
        schemas = self.session.query(CampanaSchema).filter(
            CampanaSchema.estado == EstadoCampanaEnum.ACTIVA
        ).all()
        return [self._schema_a_entidad(schema) for schema in schemas]
    
    def obtener_por_categoria(self, categoria: str) -> List[Campaña]:
        """Obtiene campañas que incluyan una categoría específica."""
        # Buscar en el JSON de criterios_afiliado
        schemas = self.session.query(CampanaSchema).filter(
            CampanaSchema.criterios_afiliado.op('->>')('categorias_requeridas').like(f'%{categoria}%')
        ).all()
        return [self._schema_a_entidad(schema) for schema in schemas]
    
    def obtener_por_influencer_origen(self, influencer_id: str) -> List[Campaña]:
        """Obtiene campañas creadas para un influencer específico."""
        schemas = self.session.query(CampanaSchema).filter(
            CampanaSchema.influencer_origen_id == influencer_id
        ).all()
        return [self._schema_a_entidad(schema) for schema in schemas]
    
    def obtener_todas(self, limite: int = 100, offset: int = 0) -> List[Campaña]:
        """Obtiene todas las campañas con paginación."""
        schemas = self.session.query(CampanaSchema).offset(offset).limit(limite).all()
        return [self._schema_a_entidad(schema) for schema in schemas]
    
    def agregar(self, campaña: Campaña) -> None:
        """Agrega una nueva campaña."""
        logger.info(f"💾 CAMPAÑAS: Agregando campaña '{campaña.nombre}' al repositorio")
        schema = self._entidad_a_schema(campaña)
        self.session.add(schema)
        self.session.flush()  # Para obtener el ID generado
        logger.info(f"✅ CAMPAÑAS: Campaña '{campaña.nombre}' agregada a la sesión con ID: {schema.id}")
    
    def actualizar(self, campaña: Campaña) -> None:
        """Actualiza una campaña existente."""
        schema = self.session.query(CampanaSchema).filter(CampanaSchema.id == campaña.id).first()
        if schema:
            self._actualizar_schema_desde_entidad(schema, campaña)
            self.session.flush()
    
    def eliminar(self, campaña_id: str) -> None:
        """Elimina una campaña."""
        schema = self.session.query(CampanaSchema).filter(CampanaSchema.id == campaña_id).first()
        if schema:
            self.session.delete(schema)
            self.session.flush()
    
    def existe_con_nombre(self, nombre: str, excluir_id: Optional[str] = None) -> bool:
        """Verifica si existe una campaña con el nombre dado."""
        query = self.session.query(CampanaSchema).filter(CampanaSchema.nombre == nombre)
        if excluir_id:
            query = query.filter(CampanaSchema.id != excluir_id)
        return query.first() is not None
    
    def _schema_a_entidad(self, schema: CampanaSchema) -> Campaña:
        """Convierte un schema de base de datos a entidad de dominio."""
        
        # Crear objetos valor
        tipo_comision = TipoComision(schema.tipo_comision.value)
        dinero_comision = Dinero(schema.valor_comision, schema.moneda)
        terminos_comision = TerminosComision(
            tipo_comision, 
            dinero_comision, 
            schema.descripcion_comision or ""
        )
        
        periodo = PeriodoCampaña(schema.fecha_inicio, schema.fecha_fin)
        
        # Material promocional
        material_data = schema.material_promocional or {}
        material = MaterialPromocional(
            titulo=material_data.get('titulo', ''),
            descripcion=material_data.get('descripcion', ''),
            enlaces=material_data.get('enlaces', []),
            imagenes=material_data.get('imagenes', []),
            banners=material_data.get('banners', [])
        )
        
        # Criterios de afiliado
        criterios_data = schema.criterios_afiliado or {}
        criterios = CriteriosAfiliado(
            tipos_permitidos=criterios_data.get('tipos_permitidos', []),
            categorias_requeridas=criterios_data.get('categorias_requeridas', []),
            paises_permitidos=criterios_data.get('paises_permitidos', []),
            metricas_minimas=criterios_data.get('metricas_minimas', {})
        )
        
        # Crear la entidad
        campaña = Campaña(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            terminos_comision=terminos_comision,
            periodo=periodo,
            material_promocional=material,
            criterios_afiliado=criterios,
            id=str(schema.id)
        )
        
        # Establecer estado y fechas
        campaña.estado = EstadoCampaña(schema.estado.value)
        campaña.fecha_activacion = schema.fecha_activacion
        campaña.fecha_pausa = schema.fecha_pausa
        
        # Métricas
        metricas_data = schema.metricas or {}
        campaña.metricas = MetricasCampaña(
            afiliados_asignados=metricas_data.get('afiliados_asignados', 0),
            clics_totales=metricas_data.get('clics_totales', 0),
            conversiones_totales=metricas_data.get('conversiones_totales', 0),
            inversion_total=metricas_data.get('inversion_total', 0.0),
            ingresos_generados=metricas_data.get('ingresos_generados', 0.0)
        )
        
        # Afiliados asignados
        campaña.afiliados_asignados = set(schema.afiliados_asignados or [])
        
        # Establecer versión
        campaña.version = schema.version
        
        return campaña
    
    def _entidad_a_schema(self, campaña: Campaña) -> CampanaSchema:
        """Convierte una entidad de dominio a schema de base de datos."""
        
        # Preparar datos JSON
        material_data = {
            'titulo': campaña.material_promocional.titulo,
            'descripcion': campaña.material_promocional.descripcion,
            'enlaces': campaña.material_promocional.enlaces,
            'imagenes': campaña.material_promocional.imagenes,
            'banners': campaña.material_promocional.banners
        }
        
        criterios_data = {
            'tipos_permitidos': campaña.criterios_afiliado.tipos_permitidos,
            'categorias_requeridas': campaña.criterios_afiliado.categorias_requeridas,
            'paises_permitidos': campaña.criterios_afiliado.paises_permitidos,
            'metricas_minimas': campaña.criterios_afiliado.metricas_minimas
        }
        
        metricas_data = {
            'afiliados_asignados': campaña.metricas.afiliados_asignados,
            'clics_totales': campaña.metricas.clics_totales,
            'conversiones_totales': campaña.metricas.conversiones_totales,
            'inversion_total': campaña.metricas.inversion_total,
            'ingresos_generados': campaña.metricas.ingresos_generados
        }
        
        return CampanaSchema(
            id=campaña.id,
            nombre=campaña.nombre,
            descripcion=campaña.descripcion,
            tipo_comision=TipoComisionEnum(campaña.terminos_comision.tipo.value),
            valor_comision=campaña.terminos_comision.valor.cantidad,
            moneda=campaña.terminos_comision.valor.moneda,
            descripcion_comision=campaña.terminos_comision.descripcion,
            fecha_inicio=campaña.periodo.fecha_inicio,
            fecha_fin=campaña.periodo.fecha_fin,
            estado=EstadoCampanaEnum(campaña.estado.value),
            fecha_activacion=campaña.fecha_activacion,
            fecha_pausa=campaña.fecha_pausa,
            material_promocional=material_data,
            criterios_afiliado=criterios_data,
            metricas=metricas_data,
            afiliados_asignados=list(campaña.afiliados_asignados),
            version=campaña.version
        )
    
    def _actualizar_schema_desde_entidad(self, schema: CampanaSchema, campaña: Campaña) -> None:
        """Actualiza un schema existente con datos de la entidad."""
        
        # Actualizar campos básicos
        schema.nombre = campaña.nombre
        schema.descripcion = campaña.descripcion
        schema.tipo_comision = TipoComisionEnum(campaña.terminos_comision.tipo.value)
        schema.valor_comision = campaña.terminos_comision.valor.cantidad
        schema.moneda = campaña.terminos_comision.valor.moneda
        schema.descripcion_comision = campaña.terminos_comision.descripcion
        schema.fecha_inicio = campaña.periodo.fecha_inicio
        schema.fecha_fin = campaña.periodo.fecha_fin
        schema.estado = EstadoCampanaEnum(campaña.estado.value)
        schema.fecha_activacion = campaña.fecha_activacion
        schema.fecha_pausa = campaña.fecha_pausa
        
        # Actualizar datos JSON
        schema.material_promocional = {
            'titulo': campaña.material_promocional.titulo,
            'descripcion': campaña.material_promocional.descripcion,
            'enlaces': campaña.material_promocional.enlaces,
            'imagenes': campaña.material_promocional.imagenes,
            'banners': campaña.material_promocional.banners
        }
        
        schema.criterios_afiliado = {
            'tipos_permitidos': campaña.criterios_afiliado.tipos_permitidos,
            'categorias_requeridas': campaña.criterios_afiliado.categorias_requeridas,
            'paises_permitidos': campaña.criterios_afiliado.paises_permitidos,
            'metricas_minimas': campaña.criterios_afiliado.metricas_minimas
        }
        
        schema.metricas = {
            'afiliados_asignados': campaña.metricas.afiliados_asignados,
            'clics_totales': campaña.metricas.clics_totales,
            'conversiones_totales': campaña.metricas.conversiones_totales,
            'inversion_total': campaña.metricas.inversion_total,
            'ingresos_generados': campaña.metricas.ingresos_generados
        }
        
        schema.afiliados_asignados = list(campaña.afiliados_asignados)
        schema.version = campaña.version
