import base64
from datetime import datetime
from email.message import EmailMessage
from typing import List, Optional

from pydantic import BaseModel, Field

from app.dominio.modelos import SolicitudInscripcion, Visitante

PATRON_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class VisitanteEntrada(BaseModel):
    nombre: str
    dni: str
    edad: int
    talle: Optional[str] = None


class InscripcionEntrada(BaseModel):
    actividad: str
    horario: datetime
    email: str = Field(pattern=PATRON_EMAIL)
    acepta_terminos: bool
    visitantes: List[VisitanteEntrada]

    def a_solicitud(self) -> SolicitudInscripcion:
        return SolicitudInscripcion(
            actividad=self.actividad,
            horario=self.horario,
            visitantes=[
                Visitante(**visitante.model_dump())
                for visitante in self.visitantes
            ],
            acepta_terminos=self.acepta_terminos,
            email=self.email,
        )


class InscripcionSalida(BaseModel):
    codigo: str
    actividad: str
    horario: datetime
    cantidad_personas: int


class ActividadSalida(BaseModel):
    nombre: str
    requiere_talle: bool
    edad_minima: int
    cupo_por_turno: int


class TurnoSalida(BaseModel):
    horario: datetime
    cupos_disponibles: int
    inscripcion_abierta: bool


class AdjuntoSalida(BaseModel):
    nombre: str
    tipo: str
    contenido_base64: str


class CorreoSalida(BaseModel):
    remitente: str
    destinatario: str
    asunto: str
    cuerpo: str
    adjunto: AdjuntoSalida

    @classmethod
    def desde_mensaje(cls, mensaje: EmailMessage) -> "CorreoSalida":
        adjunto = next(mensaje.iter_attachments())
        return cls(
            remitente=mensaje["From"],
            destinatario=mensaje["To"],
            asunto=mensaje["Subject"],
            cuerpo=mensaje.get_body(preferencelist=("plain",)).get_content(),
            adjunto=AdjuntoSalida(
                nombre=adjunto.get_filename(),
                tipo=adjunto.get_content_type(),
                contenido_base64=base64.b64encode(
                    adjunto.get_content()
                ).decode(),
            ),
        )
