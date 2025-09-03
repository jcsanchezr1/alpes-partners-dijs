from typing import Dict, Any
from ...seedwork.infraestructura.eventos import ConsumidorEventos
from ..aplicacion.comandos.registrar_afiliado import RegistrarAfiliado
from ..aplicacion.dto import RegistrarAfiliadoDTO
from ..dominio.objetos_valor import TipoAfiliado


class ConsumidorEventosCampañas:
    """Consumidor de eventos del módulo Campañas."""
    
    def __init__(self, mediador):
        self.mediador = mediador
    
    async def cuando_campaña_creada(self, evento: Dict[str, Any]) -> None:
        """Maneja el evento CampañaCreada."""
        # Lógica para notificar a afiliados sobre nueva campaña
        # Por ejemplo, buscar afiliados compatibles y notificarles
        print(f"Nueva campaña creada: {evento['nombre']}")
        print(f"Categorías objetivo: {evento['categorias_objetivo']}")
        
        # Aquí se podría implementar lógica para:
        # 1. Buscar afiliados activos compatibles
        # 2. Enviar notificaciones
        # 3. Crear oportunidades de campaña
    
    async def cuando_afiliado_asignado_a_campaña(self, evento: Dict[str, Any]) -> None:
        """Maneja el evento AfiliadoAsignadoACampaña."""
        print(f"Afiliado {evento['nombre_afiliado']} asignado a campaña {evento['nombre_campaña']}")
        
        # Aquí se podría implementar lógica para:
        # 1. Actualizar métricas del afiliado
        # 2. Enviar confirmación al afiliado
        # 3. Generar materiales promocionales personalizados
