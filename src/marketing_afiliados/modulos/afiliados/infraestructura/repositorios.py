from typing import List, Optional, Dict
from ..dominio.repositorios import RepositorioAfiliados
from ..dominio.entidades import Afiliado
from ..dominio.objetos_valor import TipoAfiliado, EstadoAfiliado


class RepositorioAfiliadosMemoria(RepositorioAfiliados):
    """Implementación en memoria del repositorio de afiliados."""
    
    def __init__(self):
        self._afiliados: Dict[str, Afiliado] = {}
    
    async def obtener_por_id(self, id: str) -> Optional[Afiliado]:
        """Obtiene un afiliado por su ID."""
        return self._afiliados.get(id)
    
    async def agregar(self, entidad: Afiliado) -> None:
        """Agrega un nuevo afiliado."""
        self._afiliados[entidad.id] = entidad
    
    async def actualizar(self, entidad: Afiliado) -> None:
        """Actualiza un afiliado existente."""
        if entidad.id in self._afiliados:
            self._afiliados[entidad.id] = entidad
    
    async def eliminar(self, entidad: Afiliado) -> None:
        """Elimina un afiliado."""
        if entidad.id in self._afiliados:
            del self._afiliados[entidad.id]
    
    async def obtener_todos(self) -> List[Afiliado]:
        """Obtiene todos los afiliados."""
        return list(self._afiliados.values())
    
    async def obtener_por_email(self, email: str) -> Optional[Afiliado]:
        """Obtiene un afiliado por su email."""
        for afiliado in self._afiliados.values():
            if afiliado.email == email:
                return afiliado
        return None
    
    async def obtener_por_estado(self, estado: EstadoAfiliado) -> List[Afiliado]:
        """Obtiene afiliados por estado."""
        return [afiliado for afiliado in self._afiliados.values() 
                if afiliado.estado == estado]
    
    async def obtener_por_tipo(self, tipo: TipoAfiliado) -> List[Afiliado]:
        """Obtiene afiliados por tipo."""
        return [afiliado for afiliado in self._afiliados.values() 
                if afiliado.tipo_afiliado == tipo]
    
    async def obtener_por_categoria(self, categoria: str) -> List[Afiliado]:
        """Obtiene afiliados que manejan una categoría específica."""
        return [afiliado for afiliado in self._afiliados.values() 
                if categoria in afiliado.categorias]
    
    async def buscar_por_nombre(self, nombre: str) -> List[Afiliado]:
        """Busca afiliados por nombre (búsqueda parcial)."""
        nombre_lower = nombre.lower()
        return [afiliado for afiliado in self._afiliados.values() 
                if nombre_lower in afiliado.nombre.lower()]
    
    async def existe_email(self, email: str) -> bool:
        """Verifica si existe un afiliado con el email dado."""
        return await self.obtener_por_email(email) is not None
