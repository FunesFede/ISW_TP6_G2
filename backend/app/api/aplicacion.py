from datetime import date
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.esquemas import (
    ActividadSalida,
    CorreoSalida,
    InscripcionEntrada,
    InscripcionSalida,
    TurnoSalida,
)
from app.dominio.excepciones import (
    ActividadInexistenteError,
    InscripcionError,
    InscripcionInexistenteError,
    SinCupoError,
    VisitanteConInscripcionSuperpuestaError,
)
from app.dominio.puertos import (
    CalendarioParque,
    GeneradorQR,
    NotificadorInscripcion,
    Reloj,
    RepositorioInscripciones,
    RepositorioTurnos,
)
from app.infraestructura.notificador_mail import construir_mensaje
from app.servicios.servicio_inscripcion import ServicioInscripcion

ESTADO_POR_ERROR = {
    ActividadInexistenteError: 404,
    InscripcionInexistenteError: 404,
    SinCupoError: 409,
    VisitanteConInscripcionSuperpuestaError: 409,
}
ESTADO_POR_DEFECTO = 422
REMITENTE_POR_DEFECTO = "inscripciones@ecoharmony.park"


def crear_aplicacion(
    repositorio_turnos: RepositorioTurnos,
    calendario_parque: CalendarioParque,
    notificador: NotificadorInscripcion,
    generador_qr: GeneradorQR,
    reloj: Reloj,
    repositorio_inscripciones: RepositorioInscripciones,
    remitente: str = REMITENTE_POR_DEFECTO,
) -> FastAPI:
    aplicacion = FastAPI(title="EcoHarmony Park - Inscripciones")
    servicio = ServicioInscripcion(
        repositorio_turnos=repositorio_turnos,
        calendario_parque=calendario_parque,
        notificador=notificador,
        generador_qr=generador_qr,
        reloj=reloj,
        repositorio_inscripciones=repositorio_inscripciones,
    )

    @aplicacion.exception_handler(InscripcionError)
    def manejar_error_de_inscripcion(
        request: Request, error: InscripcionError
    ) -> JSONResponse:
        estado = ESTADO_POR_ERROR.get(type(error), ESTADO_POR_DEFECTO)
        return JSONResponse(
            status_code=estado, content={"detail": str(error)}
        )

    @aplicacion.get("/actividades", response_model=List[ActividadSalida])
    def listar_actividades() -> List[ActividadSalida]:
        return [
            ActividadSalida(
                nombre=actividad.nombre,
                requiere_talle=actividad.requiere_talle,
                edad_minima=actividad.edad_minima,
                cupo_por_turno=actividad.cupo_por_turno,
            )
            for actividad in servicio.listar_actividades()
        ]

    @aplicacion.get(
        "/actividades/{actividad}/turnos", response_model=List[TurnoSalida]
    )
    def listar_turnos(actividad: str, fecha: date) -> List[TurnoSalida]:
        return [
            TurnoSalida(
                horario=turno.inicio,
                cupos_disponibles=turno.cupos_disponibles,
                inscripcion_abierta=servicio.inscripcion_abierta(turno),
            )
            for turno in servicio.listar_turnos(actividad, fecha)
        ]

    @aplicacion.post(
        "/inscripciones", response_model=InscripcionSalida, status_code=201
    )
    def inscribir(entrada: InscripcionEntrada) -> InscripcionSalida:
        inscripcion = servicio.inscribir(entrada.a_solicitud())
        return InscripcionSalida(
            codigo=inscripcion.codigo,
            actividad=inscripcion.actividad,
            horario=inscripcion.horario,
            cantidad_personas=len(inscripcion.visitantes),
        )

    @aplicacion.get(
        "/inscripciones/{codigo}/correo", response_model=CorreoSalida
    )
    def ver_correo(codigo: str) -> CorreoSalida:
        inscripcion = servicio.buscar_inscripcion(codigo)
        qr_png = generador_qr.generar(inscripcion.codigo)
        mensaje = construir_mensaje(
            inscripcion.email, inscripcion, qr_png, remitente
        )
        return CorreoSalida.desde_mensaje(mensaje)

    return aplicacion
