import pytest
from datetime import datetime
from src.alpes_partners.modulos.afiliados.dominio.entidades import Afiliado
from src.alpes_partners.modulos.afiliados.dominio.objetos_valor import TipoAfiliado, EstadoAfiliado
from src.alpes_partners.seedwork.dominio.excepciones import ExcepcionReglaDeNegocio


class TestAfiliado:
    """Tests para la entidad Afiliado."""
    
    def test_crear_afiliado_exitoso(self):
        """Test crear afiliado con datos válidos."""
        afiliado = Afiliado.crear(
            nombre="Juan Pérez",
            email="juan@example.com",
            tipo_afiliado=TipoAfiliado.TRADICIONAL,
            categorias=["tecnologia", "electronica"],
            descripcion="Sitio de comparación de precios",
            sitio_web="https://juan-comparador.com"
        )
        
        assert afiliado.nombre == "Juan Pérez"
        assert afiliado.email.valor == "juan@example.com"
        assert afiliado.perfil.tipo == TipoAfiliado.TRADICIONAL
        assert afiliado.estado == EstadoAfiliado.PENDIENTE
        assert len(afiliado.eventos) == 1  # Evento AfiliadoRegistrado
    
    def test_activar_afiliado(self):
        """Test activar afiliado."""
        afiliado = Afiliado.crear(
            nombre="María García",
            email="maria@example.com",
            tipo_afiliado=TipoAfiliado.INFLUENCER,
            categorias=["moda", "lifestyle"],
            descripcion="Influencer de moda"
        )
        
        afiliado.limpiar_eventos()  # Limpiar evento de registro
        afiliado.activar()
        
        assert afiliado.estado == EstadoAfiliado.ACTIVO
        assert afiliado.fecha_activacion is not None
        assert len(afiliado.eventos) == 1  # Evento AfiliadoActivado
    
    def test_desactivar_afiliado(self):
        """Test desactivar afiliado."""
        afiliado = Afiliado.crear(
            nombre="Carlos López",
            email="carlos@example.com",
            tipo_afiliado=TipoAfiliado.PARTNER_B2B,
            categorias=["software", "saas"],
            descripcion="Integrador SaaS"
        )
        
        afiliado.activar()
        afiliado.limpiar_eventos()
        afiliado.desactivar("Incumplimiento de términos")
        
        assert afiliado.estado == EstadoAfiliado.INACTIVO
        assert afiliado.fecha_desactivacion is not None
        assert len(afiliado.eventos) == 1  # Evento AfiliadoDesactivado
    
    def test_crear_afiliado_sin_nombre_falla(self):
        """Test que falla al crear afiliado sin nombre."""
        with pytest.raises(ExcepcionReglaDeNegocio):
            Afiliado.crear(
                nombre="",
                email="test@example.com",
                tipo_afiliado=TipoAfiliado.TRADICIONAL,
                categorias=["tecnologia"],
                descripcion="Descripción"
            )
    
    def test_actualizar_perfil_afiliado(self):
        """Test actualizar perfil de afiliado."""
        afiliado = Afiliado.crear(
            nombre="Ana Rodríguez",
            email="ana@example.com",
            tipo_afiliado=TipoAfiliado.MEDIO_EDITORIAL,
            categorias=["noticias", "tecnologia"],
            descripcion="Portal de noticias tech"
        )
        
        afiliado.limpiar_eventos()
        afiliado.actualizar_perfil(
            descripcion="Portal líder en noticias de tecnología",
            sitio_web="https://tech-news.com"
        )
        
        assert "Portal líder" in afiliado.perfil.descripcion
        assert afiliado.perfil.sitio_web == "https://tech-news.com"
        assert len(afiliado.eventos) == 1  # Evento PerfilAfiliadoActualizado


if __name__ == "__main__":
    pytest.main([__file__])
