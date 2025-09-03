from src.marketing_afiliados.seedwork.dominio.excepciones import ExcepcionDominio


class ExcepcionAfiliado(ExcepcionDominio):
    """Excepción base para el dominio de afiliados."""
    pass


class AfiliadoYaExiste(ExcepcionAfiliado):
    """Excepción cuando se intenta registrar un afiliado que ya existe."""
    pass


class AfiliadoNoEncontrado(ExcepcionAfiliado):
    """Excepción cuando no se encuentra un afiliado."""
    pass


class EmailYaRegistrado(ExcepcionAfiliado):
    """Excepción cuando se intenta usar un email ya registrado."""
    pass


class EstadoAfiliadoInvalido(ExcepcionAfiliado):
    """Excepción cuando se intenta una operación con estado inválido."""
    pass
