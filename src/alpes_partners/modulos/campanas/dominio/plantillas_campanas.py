"""
Plantillas de campañas por categoría de influencer.
Define las campañas automáticas que se crean según la categoría del influencer.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from .objetos_valor import TipoComision


class PlantillaCampana:
    """Plantilla para crear campañas automáticamente."""
    
    def __init__(self,
                 nombre_template: str,
                 descripcion_template: str,
                 tipo_comision: TipoComision,
                 valor_comision: float,
                 moneda: str = "USD",
                 duracion_dias: int = 30,
                 titulo_material: str = "",
                 descripcion_material: str = "",
                 tipos_afiliado_permitidos: List[str] = None,
                 enlaces_material: List[str] = None,
                 imagenes_material: List[str] = None,
                 metricas_minimas: Dict[str, Any] = None):
        
        self.nombre_template = nombre_template
        self.descripcion_template = descripcion_template
        self.tipo_comision = tipo_comision
        self.valor_comision = valor_comision
        self.moneda = moneda
        self.duracion_dias = duracion_dias
        self.titulo_material = titulo_material
        self.descripcion_material = descripcion_material
        self.tipos_afiliado_permitidos = tipos_afiliado_permitidos or ["influencer"]
        self.enlaces_material = enlaces_material or []
        self.imagenes_material = imagenes_material or []
        self.metricas_minimas = metricas_minimas or {}
    
    def generar_nombre(self, nombre_influencer: str) -> str:
        """Genera el nombre de la campaña basado en el influencer."""
        return self.nombre_template.format(influencer=nombre_influencer)
    
    def generar_descripcion(self, nombre_influencer: str, categoria: str) -> str:
        """Genera la descripción de la campaña."""
        return self.descripcion_template.format(
            influencer=nombre_influencer,
            categoria=categoria
        )


class GeneradorCampanasPorCategoria:
    """Generador de campañas automáticas basadas en categorías de influencers."""
    
    # Plantillas de campañas por categoría
    PLANTILLAS_POR_CATEGORIA: Dict[str, PlantillaCampana] = {
        
        # Tecnología
        "tecnologia": PlantillaCampana(
            nombre_template="Tech Innovation - {influencer}",
            descripcion_template="Campaña de productos tecnológicos innovadores para {influencer} especializado en {categoria}",
            tipo_comision=TipoComision.CPA,
            valor_comision=50.0,
            duracion_dias=45,
            titulo_material="Últimas Innovaciones Tecnológicas",
            descripcion_material="Descubre los productos tech más innovadores del mercado",
            tipos_afiliado_permitidos=["influencer", "tech_reviewer"],
            enlaces_material=[
                "https://example.com/tech-products",
                "https://example.com/tech-reviews"
            ],
            metricas_minimas={"seguidores_minimos": 1000, "engagement_rate": 3.0}
        ),
        
        # Lifestyle
        "lifestyle": PlantillaCampana(
            nombre_template="Lifestyle Essentials - {influencer}",
            descripcion_template="Campaña de productos lifestyle y bienestar para {influencer} en {categoria}",
            tipo_comision=TipoComision.CPL,
            valor_comision=25.0,
            duracion_dias=60,
            titulo_material="Productos Lifestyle Premium",
            descripcion_material="Mejora tu estilo de vida con productos cuidadosamente seleccionados",
            tipos_afiliado_permitidos=["influencer", "lifestyle_blogger"],
            enlaces_material=[
                "https://example.com/lifestyle-products",
                "https://example.com/wellness-guide"
            ],
            metricas_minimas={"seguidores_minimos": 500, "engagement_rate": 4.0}
        ),
        
        # Moda
        "moda": PlantillaCampana(
            nombre_template="Fashion Forward - {influencer}",
            descripcion_template="Campaña de moda y tendencias para {influencer} especializado en {categoria}",
            tipo_comision=TipoComision.CPA,
            valor_comision=35.0,
            duracion_dias=30,
            titulo_material="Últimas Tendencias de Moda",
            descripcion_material="Descubre las tendencias de moda más actuales y exclusivas",
            tipos_afiliado_permitidos=["influencer", "fashion_blogger"],
            enlaces_material=[
                "https://example.com/fashion-trends",
                "https://example.com/style-guide"
            ],
            metricas_minimas={"seguidores_minimos": 2000, "engagement_rate": 5.0}
        ),
        
        # Fitness
        "fitness": PlantillaCampana(
            nombre_template="Fitness Revolution - {influencer}",
            descripcion_template="Campaña de productos fitness y nutrición para {influencer} en {categoria}",
            tipo_comision=TipoComision.CPA,
            valor_comision=40.0,
            duracion_dias=90,
            titulo_material="Transforma Tu Físico",
            descripcion_material="Productos y suplementos para alcanzar tus objetivos fitness",
            tipos_afiliado_permitidos=["influencer", "fitness_trainer"],
            enlaces_material=[
                "https://example.com/fitness-products",
                "https://example.com/workout-plans"
            ],
            metricas_minimas={"seguidores_minimos": 1500, "engagement_rate": 6.0}
        ),
        
        # Belleza
        "belleza": PlantillaCampana(
            nombre_template="Beauty Secrets - {influencer}",
            descripcion_template="Campaña de productos de belleza y cuidado personal para {influencer} en {categoria}",
            tipo_comision=TipoComision.CPL,
            valor_comision=30.0,
            duracion_dias=45,
            titulo_material="Secretos de Belleza Revelados",
            descripcion_material="Productos de belleza premium para realzar tu belleza natural",
            tipos_afiliado_permitidos=["influencer", "beauty_guru"],
            enlaces_material=[
                "https://example.com/beauty-products",
                "https://example.com/makeup-tutorials"
            ],
            metricas_minimas={"seguidores_minimos": 3000, "engagement_rate": 7.0}
        ),
        
        # Gastronomía
        "gastronomia": PlantillaCampana(
            nombre_template="Culinary Experience - {influencer}",
            descripcion_template="Campaña gastronómica y productos culinarios para {influencer} especializado en {categoria}",
            tipo_comision=TipoComision.CPC,
            valor_comision=15.0,
            duracion_dias=60,
            titulo_material="Experiencias Gastronómicas Únicas",
            descripcion_material="Descubre sabores únicos y productos culinarios excepcionales",
            tipos_afiliado_permitidos=["influencer", "food_blogger"],
            enlaces_material=[
                "https://example.com/gourmet-products",
                "https://example.com/recipes"
            ],
            metricas_minimas={"seguidores_minimos": 800, "engagement_rate": 4.5}
        ),
        
        # Viajes
        "viajes": PlantillaCampana(
            nombre_template="Travel Adventures - {influencer}",
            descripcion_template="Campaña de experiencias de viaje y productos para viajeros para {influencer} en {categoria}",
            tipo_comision=TipoComision.CPA,
            valor_comision=60.0,
            duracion_dias=120,
            titulo_material="Aventuras de Viaje Inolvidables",
            descripcion_material="Experiencias de viaje únicas y productos esenciales para viajeros",
            tipos_afiliado_permitidos=["influencer", "travel_blogger"],
            enlaces_material=[
                "https://example.com/travel-deals",
                "https://example.com/travel-gear"
            ],
            metricas_minimas={"seguidores_minimos": 2500, "engagement_rate": 5.5}
        ),
        
        # Gaming
        "gaming": PlantillaCampana(
            nombre_template="Gaming Elite - {influencer}",
            descripcion_template="Campaña de productos gaming y entretenimiento para {influencer} especializado en {categoria}",
            tipo_comision=TipoComision.CPA,
            valor_comision=45.0,
            duracion_dias=60,
            titulo_material="Gaming Gear Premium",
            descripcion_material="Equipo gaming profesional para llevar tu juego al siguiente nivel",
            tipos_afiliado_permitidos=["influencer", "gamer", "streamer"],
            enlaces_material=[
                "https://example.com/gaming-gear",
                "https://example.com/game-reviews"
            ],
            metricas_minimas={"seguidores_minimos": 5000, "engagement_rate": 8.0}
        ),
        
        # Educación
        "educacion": PlantillaCampana(
            nombre_template="Learning Hub - {influencer}",
            descripcion_template="Campaña de cursos y productos educativos para {influencer} en {categoria}",
            tipo_comision=TipoComision.CPL,
            valor_comision=20.0,
            duracion_dias=90,
            titulo_material="Educación de Calidad",
            descripcion_material="Cursos y recursos educativos para el crecimiento personal y profesional",
            tipos_afiliado_permitidos=["influencer", "educator", "coach"],
            enlaces_material=[
                "https://example.com/online-courses",
                "https://example.com/educational-resources"
            ],
            metricas_minimas={"seguidores_minimos": 1000, "engagement_rate": 3.5}
        ),
        
        # Finanzas
        "finanzas": PlantillaCampana(
            nombre_template="Financial Freedom - {influencer}",
            descripcion_template="Campaña de productos y servicios financieros para {influencer} especializado en {categoria}",
            tipo_comision=TipoComision.CPA,
            valor_comision=80.0,
            duracion_dias=60,
            titulo_material="Libertad Financiera",
            descripcion_material="Herramientas y servicios para alcanzar la independencia financiera",
            tipos_afiliado_permitidos=["influencer", "financial_advisor"],
            enlaces_material=[
                "https://example.com/financial-tools",
                "https://example.com/investment-guide"
            ],
            metricas_minimas={"seguidores_minimos": 3000, "engagement_rate": 4.0}
        )
    }
    
    @classmethod
    def obtener_plantilla(cls, categoria: str) -> PlantillaCampana:
        """Obtiene la plantilla de campaña para una categoría específica."""
        categoria_lower = categoria.lower().strip()
        
        # Buscar coincidencia exacta
        if categoria_lower in cls.PLANTILLAS_POR_CATEGORIA:
            return cls.PLANTILLAS_POR_CATEGORIA[categoria_lower]
        
        # Buscar coincidencia parcial
        for cat_key, plantilla in cls.PLANTILLAS_POR_CATEGORIA.items():
            if categoria_lower in cat_key or cat_key in categoria_lower:
                return plantilla
        
        # Plantilla por defecto si no se encuentra la categoría
        return cls._plantilla_por_defecto()
    
    @classmethod
    def _plantilla_por_defecto(cls) -> PlantillaCampana:
        """Plantilla por defecto para categorías no definidas."""
        return PlantillaCampana(
            nombre_template="General Campaign - {influencer}",
            descripcion_template="Campaña general de productos y servicios para {influencer} en {categoria}",
            tipo_comision=TipoComision.CPL,
            valor_comision=25.0,
            duracion_dias=30,
            titulo_material="Productos Seleccionados",
            descripcion_material="Productos y servicios cuidadosamente seleccionados",
            tipos_afiliado_permitidos=["influencer"],
            metricas_minimas={"seguidores_minimos": 500, "engagement_rate": 2.0}
        )
    
    @classmethod
    def obtener_categorias_disponibles(cls) -> List[str]:
        """Obtiene la lista de categorías disponibles."""
        return list(cls.PLANTILLAS_POR_CATEGORIA.keys())
    
    @classmethod
    def generar_campanas_para_influencer(cls, 
                                        influencer_id: str,
                                        nombre_influencer: str,
                                        categorias: List[str]) -> List[Dict[str, Any]]:
        """Genera las campañas para un influencer basado en sus categorías."""
        campanas_generadas = []
        
        for categoria in categorias:
            plantilla = cls.obtener_plantilla(categoria)
            
            # Calcular fechas
            fecha_inicio = datetime.utcnow()
            fecha_fin = fecha_inicio + timedelta(days=plantilla.duracion_dias)
            
            campana_data = {
                'nombre': plantilla.generar_nombre(nombre_influencer),
                'descripcion': plantilla.generar_descripcion(nombre_influencer, categoria),
                'tipo_comision': plantilla.tipo_comision.value,
                'valor_comision': plantilla.valor_comision,
                'moneda': plantilla.moneda,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'titulo_material': plantilla.titulo_material,
                'descripcion_material': plantilla.descripcion_material,
                'categorias_objetivo': [categoria],
                'tipos_afiliado_permitidos': plantilla.tipos_afiliado_permitidos,
                'enlaces_material': plantilla.enlaces_material,
                'imagenes_material': plantilla.imagenes_material,
                'metricas_minimas': plantilla.metricas_minimas,
                'auto_activar': True,
                'influencer_origen_id': influencer_id,
                'categoria_origen': categoria
            }
            
            campanas_generadas.append(campana_data)
        
        return campanas_generadas
