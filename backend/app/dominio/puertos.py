"""Interfaces (puertos) de las que depende el dominio.

El servicio de inscripción solo conoce estos contratos; las
implementaciones concretas viven en app/infraestructura y se inyectan.
"""
from datetime import date, datetime
from typing import List, Optional, Protocol, Set

from app.dominio.modelos import Inscripcion, Turno


class RepositorioTurnos(Protocol):

    def obtener(self, actividad: str, inicio: datetime) -> Optional[Turno]:
        ...

    def guardar(self, turno: Turno) -> None:
        ...

    def listar(self, actividad: str, fecha: date) -> List[Turno]:
        ...


class CalendarioParque(Protocol):

    def esta_abierto(self, fecha_hora: datetime) -> bool:
        ...


class NotificadorInscripcion(Protocol):

    def enviar_confirmacion(
        self, destinatario: str, inscripcion: Inscripcion, qr_png: bytes
    ) -> None:
        ...


class GeneradorQR(Protocol):

    def generar(self, contenido: str) -> bytes:
        ...


class Reloj(Protocol):

    def ahora(self) -> datetime:
        ...


class RepositorioInscripciones(Protocol):

    def guardar(self, inscripcion: Inscripcion) -> None:
        ...

    def dnis_inscriptos_en(self, horario: datetime) -> Set[str]:
        ...

    def buscar(self, codigo: str) -> Optional[Inscripcion]:
        ...
