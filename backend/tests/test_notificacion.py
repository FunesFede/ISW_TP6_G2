from datetime import datetime

from app.dominio.modelos import Inscripcion, Visitante
from app.infraestructura.generador_qr import GeneradorQRPng
from app.infraestructura.notificador_mail import (
    NotificadorBandejaLocal,
    NotificadorSMTP,
    construir_mensaje,
)

FIRMA_PNG = b"\x89PNG\r\n\x1a\n"


def crear_inscripcion():
    return Inscripcion(
        actividad="Tirolesa",
        horario=datetime(2026, 10, 14, 10, 0),
        visitantes=[
            Visitante(nombre="Ana", dni="30111222", edad=25, talle="M"),
            Visitante(nombre="Luis", dni="31222333", edad=30, talle="L"),
        ],
        codigo="ABC123",
    )


def test_generador_qr_devuelve_una_imagen_png():
    qr_png = GeneradorQRPng().generar("ABC123")

    assert qr_png.startswith(FIRMA_PNG)


def test_mensaje_de_confirmacion_tiene_destinatario_y_asunto():
    mensaje = construir_mensaje(
        "ana@mail.com", crear_inscripcion(), FIRMA_PNG, remitente="p@eh.com"
    )

    assert mensaje["To"] == "ana@mail.com"
    assert "Tirolesa" in mensaje["Subject"]


def test_mensaje_de_confirmacion_informa_los_datos_de_la_inscripcion():
    mensaje = construir_mensaje(
        "ana@mail.com", crear_inscripcion(), FIRMA_PNG, remitente="p@eh.com"
    )
    cuerpo = mensaje.get_body(preferencelist=("plain",)).get_content()

    assert "ABC123" in cuerpo
    assert "14/10/2026 10:00" in cuerpo
    assert "Ana" in cuerpo and "Luis" in cuerpo


def test_mensaje_de_confirmacion_adjunta_el_qr():
    mensaje = construir_mensaje(
        "ana@mail.com", crear_inscripcion(), FIRMA_PNG, remitente="p@eh.com"
    )
    adjuntos = list(mensaje.iter_attachments())

    assert len(adjuntos) == 1
    assert adjuntos[0].get_content_type() == "image/png"
    assert adjuntos[0].get_content() == FIRMA_PNG


def test_notificador_bandeja_local_guarda_el_mail_como_eml(tmp_path):
    notificador = NotificadorBandejaLocal(tmp_path, remitente="p@eh.com")

    notificador.enviar_confirmacion(
        "ana@mail.com", crear_inscripcion(), FIRMA_PNG
    )

    archivos = list(tmp_path.glob("*.eml"))
    assert len(archivos) == 1
    assert "ABC123" in archivos[0].name


class ConexionSMTPEspia:
    instancias = []

    def __init__(self, host, puerto):
        self.host, self.puerto = host, puerto
        self.login_con = None
        self.mensajes = []
        ConexionSMTPEspia.instancias.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def starttls(self):
        pass

    def login(self, usuario, clave):
        self.login_con = (usuario, clave)

    def send_message(self, mensaje):
        self.mensajes.append(mensaje)


def test_notificador_smtp_envia_el_mensaje_al_servidor_configurado():
    ConexionSMTPEspia.instancias.clear()
    notificador = NotificadorSMTP(
        host="smtp.ejemplo.com",
        puerto=587,
        usuario="parque",
        clave="secreta",
        remitente="p@eh.com",
        fabrica_conexion=ConexionSMTPEspia,
    )

    notificador.enviar_confirmacion(
        "ana@mail.com", crear_inscripcion(), FIRMA_PNG
    )

    conexion = ConexionSMTPEspia.instancias[0]
    assert (conexion.host, conexion.puerto) == ("smtp.ejemplo.com", 587)
    assert conexion.login_con == ("parque", "secreta")
    assert conexion.mensajes[0]["To"] == "ana@mail.com"
