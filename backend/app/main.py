"""Punto de entrada: arma las dependencias concretas y expone la app.

Ejecutar con:  uvicorn app.main:app --reload
"""
import os

from fastapi.middleware.cors import CORSMiddleware

from app.api.aplicacion import crear_aplicacion
from app.infraestructura.calendario_parque import CalendarioParqueSemanal
from app.infraestructura.datos_iniciales import generar_turnos
from app.infraestructura.generador_qr import GeneradorQRPng
from app.infraestructura.notificador_mail import (
    NotificadorBandejaLocal,
    NotificadorSMTP,
)
from app.infraestructura.reloj import RelojSistema
from app.infraestructura.repositorio_inscripciones import (
    RepositorioInscripcionesEnMemoria,
)
from app.infraestructura.repositorio_turnos import (
    RepositorioTurnosEnMemoria,
)

REMITENTE = os.getenv("MAIL_REMITENTE", "inscripciones@ecoharmony.park")
ORIGENES_FRONTEND = os.getenv(
    "ORIGENES_FRONTEND", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")


def crear_notificador():
    host = os.getenv("SMTP_HOST")
    if not host:
        return NotificadorBandejaLocal("bandeja_salida", remitente=REMITENTE)
    return NotificadorSMTP(
        host=host,
        puerto=int(os.getenv("SMTP_PUERTO", "587")),
        usuario=os.getenv("SMTP_USUARIO", ""),
        clave=os.getenv("SMTP_CLAVE", ""),
        remitente=REMITENTE,
    )


calendario = CalendarioParqueSemanal()
reloj = RelojSistema()
app = crear_aplicacion(
    repositorio_turnos=RepositorioTurnosEnMemoria(
        generar_turnos(
            desde=reloj.ahora().date(), dias=30, calendario=calendario
        )
    ),
    calendario_parque=calendario,
    notificador=crear_notificador(),
    generador_qr=GeneradorQRPng(),
    reloj=reloj,
    repositorio_inscripciones=RepositorioInscripcionesEnMemoria(),
    remitente=REMITENTE,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES_FRONTEND,
    allow_methods=["*"],
    allow_headers=["*"],
)
