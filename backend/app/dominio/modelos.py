import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

from app.dominio.excepciones import DatosVisitanteInvalidosError, SinCupoError

PATRON_DNI = re.compile(r"^\d{7,8}$")
TALLES_VALIDOS = ("XS", "S", "M", "L", "XL", "XXL")
APERTURA_INSCRIPCION = timedelta(hours=24)
CIERRE_INSCRIPCION = timedelta(minutes=15)


@dataclass
class Visitante:
    nombre: str
    dni: str
    edad: int
    talle: Optional[str] = None

    def validar(self) -> None:
        if not self.nombre.strip():
            raise DatosVisitanteInvalidosError(
                "El nombre del visitante es obligatorio."
            )
        if not PATRON_DNI.match(self.dni):
            raise DatosVisitanteInvalidosError(
                "El DNI debe tener 7 u 8 dígitos, sin puntos."
            )
        if self.edad < 0:
            raise DatosVisitanteInvalidosError(
                "La edad del visitante no puede ser negativa."
            )
        if self.talle is not None and self.talle not in TALLES_VALIDOS:
            raise DatosVisitanteInvalidosError(
                "El talle debe ser uno de: " + ", ".join(TALLES_VALIDOS) + "."
            )


@dataclass
class Turno:
    actividad: str
    inicio: datetime
    cupo_total: int
    ocupados: int = 0

    @property
    def cupos_disponibles(self) -> int:
        return self.cupo_total - self.ocupados

    @property
    def apertura_inscripcion(self) -> datetime:
        return self.inicio - APERTURA_INSCRIPCION

    @property
    def cierre_inscripcion(self) -> datetime:
        return self.inicio - CIERRE_INSCRIPCION

    def inscripcion_abierta(self, ahora: datetime) -> bool:
        return self.apertura_inscripcion <= ahora <= self.cierre_inscripcion

    def reservar(self, cantidad: int) -> None:
        if cantidad > self.cupos_disponibles:
            raise SinCupoError(
                "No hay cupos suficientes para el horario seleccionado."
            )
        self.ocupados += cantidad


@dataclass
class SolicitudInscripcion:
    actividad: str
    horario: datetime
    visitantes: List[Visitante]
    acepta_terminos: bool
    email: str


def generar_codigo() -> str:
    return uuid.uuid4().hex[:10].upper()


@dataclass
class Inscripcion:
    actividad: str
    horario: datetime
    visitantes: List[Visitante]
    email: str = ""
    codigo: str = field(default_factory=generar_codigo)
