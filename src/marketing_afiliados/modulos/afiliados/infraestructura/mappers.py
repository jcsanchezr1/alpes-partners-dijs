from datetime import datetime
from typing import Optional
import logging
from ..dominio.entidades import Afiliado

logger = logging.getLogger(__name__)
from ..dominio.objetos_valor import (
    TipoAfiliado, EstadoAfiliado, PerfilAfiliado, 
    MetricasAfiliado, CategoriaAfiliado
)
from ....seedwork.dominio.objetos_valor import Email, Telefono
from .modelos import AfiliadoModelo


class AfiliadoMapper:
    """Mapper para convertir entre entidad de dominio y modelo SQLAlchemy."""
    
    @staticmethod
    def a_modelo(afiliado: Afiliado) -> AfiliadoModelo:
        """Convierte una entidad de dominio a modelo SQLAlchemy."""
        # Manejar tanto enums como strings
        tipo_valor = afiliado.perfil.tipo.value if hasattr(afiliado.perfil.tipo, 'value') else str(afiliado.perfil.tipo)
        estado_valor = afiliado.estado.value if hasattr(afiliado.estado, 'value') else str(afiliado.estado)
        
        logger.info(f"🔄 MAPPER: Convirtiendo entidad a modelo - Tipo: {tipo_valor}, Estado: {estado_valor}")
        logger.info(f"🔄 MAPPER: Tipos originales - Tipo: {type(afiliado.perfil.tipo)}, Estado: {type(afiliado.estado)}")
        
        return AfiliadoModelo(
            id=afiliado.id,
            nombre=afiliado.nombre,
            email=afiliado.email.valor,
            telefono=afiliado.telefono.numero if afiliado.telefono else None,
            tipo_afiliado=tipo_valor,
            estado=estado_valor,
            categorias=afiliado.perfil.categorias.categorias,
            descripcion=afiliado.perfil.descripcion,
            sitio_web=afiliado.perfil.sitio_web,
            redes_sociales=afiliado.perfil.redes_sociales,
            clics_totales=str(afiliado.metricas.clics_totales),
            conversiones_totales=str(afiliado.metricas.conversiones_totales),
            ingresos_generados=str(afiliado.metricas.ingresos_generados),
            fecha_creacion=afiliado.fecha_creacion,
            fecha_activacion=afiliado.fecha_activacion,
            fecha_desactivacion=afiliado.fecha_desactivacion,
            version=str(afiliado.version)
        )
    
    @staticmethod
    def a_entidad(modelo: AfiliadoModelo) -> Afiliado:
        """Convierte un modelo SQLAlchemy a entidad de dominio."""
        # Crear objetos valor
        email = Email(modelo.email)
        telefono = Telefono(modelo.telefono) if modelo.telefono else None
        categorias = CategoriaAfiliado(modelo.categorias)
        
        perfil = PerfilAfiliado(
            tipo=TipoAfiliado(modelo.tipo_afiliado),
            categorias=categorias,
            descripcion=modelo.descripcion,
            sitio_web=modelo.sitio_web or "",
            redes_sociales=modelo.redes_sociales or {}
        )
        
        metricas = MetricasAfiliado(
            clics_totales=int(modelo.clics_totales),
            conversiones_totales=int(modelo.conversiones_totales),
            ingresos_generados=float(modelo.ingresos_generados)
        )
        
        # Crear la entidad usando el constructor
        afiliado = Afiliado(
            nombre=modelo.nombre,
            email=email,
            perfil=perfil,
            telefono=telefono,
            id=str(modelo.id)
        )
        
        # Establecer propiedades que no se pasan en el constructor
        afiliado.estado = EstadoAfiliado(modelo.estado)
        afiliado.metricas = metricas
        afiliado.fecha_activacion = modelo.fecha_activacion
        afiliado.fecha_desactivacion = modelo.fecha_desactivacion
        
        # Establecer propiedades internas (usando nombres privados correctos)
        afiliado._version = int(modelo.version)
        afiliado.fecha_creacion = modelo.fecha_creacion
        afiliado._eventos = []  # Los eventos no se persisten
        
        return afiliado
    
    @staticmethod
    def actualizar_modelo(modelo: AfiliadoModelo, afiliado: Afiliado) -> None:
        """Actualiza un modelo existente con los datos de la entidad."""
        modelo.nombre = afiliado.nombre
        modelo.email = afiliado.email.valor
        modelo.telefono = afiliado.telefono.numero if afiliado.telefono else None
        modelo.tipo_afiliado = afiliado.perfil.tipo.value if hasattr(afiliado.perfil.tipo, 'value') else str(afiliado.perfil.tipo)
        modelo.estado = afiliado.estado.value if hasattr(afiliado.estado, 'value') else str(afiliado.estado)
        modelo.categorias = afiliado.perfil.categorias.categorias
        modelo.descripcion = afiliado.perfil.descripcion
        modelo.sitio_web = afiliado.perfil.sitio_web
        modelo.redes_sociales = afiliado.perfil.redes_sociales
        modelo.clics_totales = str(afiliado.metricas.clics_totales)
        modelo.conversiones_totales = str(afiliado.metricas.conversiones_totales)
        modelo.ingresos_generados = str(afiliado.metricas.ingresos_generados)
        modelo.fecha_activacion = afiliado.fecha_activacion
        modelo.fecha_desactivacion = afiliado.fecha_desactivacion
        modelo.version = str(afiliado.version)
