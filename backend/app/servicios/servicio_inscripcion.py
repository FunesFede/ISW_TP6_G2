from datetime import date
from typing import List

from app.dominio.actividades import (
    CATALOGO_ACTIVIDADES,
    Actividad,
    buscar_actividad,
)
from app.dominio.excepciones import (
    ActividadInexistenteError,
    ActividadNoDisponibleError,
    DatosVisitanteInvalidosError,
    EdadInsuficienteError,
    InscripcionCerradaError,
    InscripcionInexistenteError,
    InscripcionNoHabilitadaError,
    ParqueCerradoError,
    TalleRequeridoError,
    TerminosNoAceptadosError,
    VisitanteConInscripcionSuperpuestaError,
)
from app.dominio.modelos import Inscripcion, SolicitudInscripcion, Turno
from app.dominio.puertos import (
    CalendarioParque,
    GeneradorQR,
    NotificadorInscripcion,
    Reloj,
    RepositorioInscripciones,
    RepositorioTurnos,
)


class ServicioInscripcion:

    def __init__(
        self,
        repositorio_turnos: RepositorioTurnos,
        calendario_parque: CalendarioParque,
        notificador: NotificadorInscripcion,
        generador_qr: GeneradorQR,
        reloj: Reloj,
        repositorio_inscripciones: RepositorioInscripciones,
    ):
        self._repositorio_turnos = repositorio_turnos
        self._calendario_parque = calendario_parque
        self._notificador = notificador
        self._generador_qr = generador_qr
        self._reloj = reloj
        self._repositorio_inscripciones = repositorio_inscripciones

    def inscribir(self, solicitud: SolicitudInscripcion) -> Inscripcion:
        actividad = self._obtener_actividad(solicitud.actividad)
        self._validar_visitantes(solicitud)
        self._validar_talles(actividad, solicitud)
        self._validar_edades(actividad, solicitud)
        self._validar_terminos(solicitud)
        self._validar_parque_abierto(solicitud)
        turno = self._obtener_turno(solicitud)
        self._validar_ventana_inscripcion(turno)
        self._validar_sin_superposicion(solicitud)
        turno.reservar(len(solicitud.visitantes))
        self._repositorio_turnos.guardar(turno)
        inscripcion = Inscripcion(
            actividad=solicitud.actividad,
            horario=solicitud.horario,
            visitantes=solicitud.visitantes,
            email=solicitud.email,
        )
        self._repositorio_inscripciones.guardar(inscripcion)
        qr_png = self._generador_qr.generar(inscripcion.codigo)
        self._notificador.enviar_confirmacion(
            inscripcion.email, inscripcion, qr_png
        )
        return inscripcion

    def buscar_inscripcion(self, codigo: str) -> Inscripcion:
        inscripcion = self._repositorio_inscripciones.buscar(codigo)
        if inscripcion is None:
            raise InscripcionInexistenteError(
                f"No existe una inscripción con el código {codigo}."
            )
        return inscripcion

    @staticmethod
    def listar_actividades() -> List[Actividad]:
        return list(CATALOGO_ACTIVIDADES.values())

    def listar_turnos(self, actividad: str, fecha: date) -> List[Turno]:
        self._obtener_actividad(actividad)
        return self._repositorio_turnos.listar(actividad, fecha)

    def _obtener_actividad(self, nombre: str) -> Actividad:
        actividad = buscar_actividad(nombre)
        if actividad is None:
            raise ActividadInexistenteError(
                f"La actividad '{nombre}' no existe."
            )
        return actividad

    @staticmethod
    def _validar_visitantes(solicitud: SolicitudInscripcion) -> None:
        if not solicitud.visitantes:
            raise DatosVisitanteInvalidosError(
                "Debe indicar al menos una persona."
            )
        for visitante in solicitud.visitantes:
            visitante.validar()
        dnis = [visitante.dni for visitante in solicitud.visitantes]
        if len(set(dnis)) != len(dnis):
            raise DatosVisitanteInvalidosError(
                "Hay visitantes con el mismo DNI en la inscripción."
            )

    @staticmethod
    def _validar_talles(
        actividad: Actividad, solicitud: SolicitudInscripcion
    ) -> None:
        if not actividad.requiere_talle:
            return
        if any(not visitante.talle for visitante in solicitud.visitantes):
            raise TalleRequeridoError(
                "La actividad requiere el talle de cada visitante."
            )

    @staticmethod
    def _validar_edades(
        actividad: Actividad, solicitud: SolicitudInscripcion
    ) -> None:
        for visitante in solicitud.visitantes:
            if visitante.edad < actividad.edad_minima:
                raise EdadInsuficienteError(
                    f"{actividad.nombre} requiere {actividad.edad_minima} "
                    f"años o más; {visitante.nombre} tiene {visitante.edad}."
                )

    @staticmethod
    def _validar_terminos(solicitud: SolicitudInscripcion) -> None:
        if not solicitud.acepta_terminos:
            raise TerminosNoAceptadosError(
                "Debe aceptar los términos y condiciones de la actividad."
            )

    def _validar_parque_abierto(self, solicitud: SolicitudInscripcion) -> None:
        if not self._calendario_parque.esta_abierto(solicitud.horario):
            raise ParqueCerradoError(
                "El parque está cerrado en el horario seleccionado."
            )

    def _obtener_turno(self, solicitud: SolicitudInscripcion) -> Turno:
        turno = self._repositorio_turnos.obtener(
            solicitud.actividad, solicitud.horario
        )
        if turno is None:
            raise ActividadNoDisponibleError(
                "La actividad no está disponible en el horario seleccionado."
            )
        return turno

    def _validar_ventana_inscripcion(self, turno: Turno) -> None:
        ahora = self._reloj.ahora()
        if ahora < turno.apertura_inscripcion:
            raise InscripcionNoHabilitadaError(
                "La inscripción se habilita 24 horas antes del turno."
            )
        if ahora > turno.cierre_inscripcion:
            raise InscripcionCerradaError(
                "La inscripción cierra 15 minutos antes del turno."
            )

    def inscripcion_abierta(self, turno: Turno) -> bool:
        return turno.inscripcion_abierta(self._reloj.ahora())

    def _validar_sin_superposicion(
        self, solicitud: SolicitudInscripcion
    ) -> None:
        ocupados = self._repositorio_inscripciones.dnis_inscriptos_en(
            solicitud.horario
        )
        for visitante in solicitud.visitantes:
            if visitante.dni in ocupados:
                raise VisitanteConInscripcionSuperpuestaError(
                    f"{visitante.nombre} (DNI {visitante.dni}) ya tiene "
                    "una inscripción en ese horario."
                )
