class InscripcionError(Exception):
    """Error base de las reglas de negocio de la inscripción."""


class ActividadInexistenteError(InscripcionError):
    pass


class SinCupoError(InscripcionError):
    pass


class ActividadNoDisponibleError(InscripcionError):
    pass


class ParqueCerradoError(InscripcionError):
    pass


class TerminosNoAceptadosError(InscripcionError):
    pass


class TalleRequeridoError(InscripcionError):
    pass


class DatosVisitanteInvalidosError(InscripcionError):
    pass


class EdadInsuficienteError(InscripcionError):
    pass


class InscripcionNoHabilitadaError(InscripcionError):
    pass


class InscripcionCerradaError(InscripcionError):
    pass


class VisitanteConInscripcionSuperpuestaError(InscripcionError):
    pass


class InscripcionInexistenteError(InscripcionError):
    pass
