import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Callable, Union

from app.dominio.modelos import Inscripcion

FORMATO_HORARIO = "%d/%m/%Y %H:%M"


def construir_mensaje(
    destinatario: str,
    inscripcion: Inscripcion,
    qr_png: bytes,
    remitente: str,
) -> EmailMessage:
    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = (
        f"EcoHarmony Park - Inscripción confirmada: {inscripcion.actividad}"
    )
    mensaje.set_content(_cuerpo(inscripcion))
    mensaje.add_attachment(
        qr_png,
        maintype="image",
        subtype="png",
        filename=f"inscripcion-{inscripcion.codigo}.png",
    )
    return mensaje


def _cuerpo(inscripcion: Inscripcion) -> str:
    participantes = "\n".join(
        f"  - {visitante.nombre} (DNI {visitante.dni})"
        for visitante in inscripcion.visitantes
    )
    return (
        "Tu inscripción en EcoHarmony Park está confirmada.\n\n"
        f"Código: {inscripcion.codigo}\n"
        f"Actividad: {inscripcion.actividad}\n"
        f"Horario: {inscripcion.horario.strftime(FORMATO_HORARIO)}\n"
        f"Participantes:\n{participantes}\n\n"
        "Presentá el código QR adjunto al llegar a la actividad.\n"
    )


class NotificadorBandejaLocal:
    """Guarda cada mail como archivo .eml. Útil en desarrollo y demos."""

    def __init__(self, directorio: Union[str, Path], remitente: str):
        self._directorio = Path(directorio)
        self._remitente = remitente

    def enviar_confirmacion(
        self, destinatario: str, inscripcion: Inscripcion, qr_png: bytes
    ) -> None:
        mensaje = construir_mensaje(
            destinatario, inscripcion, qr_png, self._remitente
        )
        self._directorio.mkdir(parents=True, exist_ok=True)
        ruta = self._directorio / f"inscripcion-{inscripcion.codigo}.eml"
        ruta.write_bytes(mensaje.as_bytes())


class NotificadorSMTP:

    def __init__(
        self,
        host: str,
        puerto: int,
        usuario: str,
        clave: str,
        remitente: str,
        fabrica_conexion: Callable = smtplib.SMTP,
    ):
        self._host = host
        self._puerto = puerto
        self._usuario = usuario
        self._clave = clave
        self._remitente = remitente
        self._fabrica_conexion = fabrica_conexion

    def enviar_confirmacion(
        self, destinatario: str, inscripcion: Inscripcion, qr_png: bytes
    ) -> None:
        mensaje = construir_mensaje(
            destinatario, inscripcion, qr_png, self._remitente
        )
        with self._fabrica_conexion(self._host, self._puerto) as conexion:
            conexion.starttls()
            conexion.login(self._usuario, self._clave)
            conexion.send_message(mensaje)
