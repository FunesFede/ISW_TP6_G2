import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { crearInscripcion } from '../api/cliente'
import ContadorPersonas from '../components/ContadorPersonas'
import DialogoTerminos from '../components/DialogoTerminos'
import Encabezado from '../components/Encabezado'
import Paso from '../components/Paso'
import ResumenReserva from '../components/ResumenReserva'
import SelectorActividad from '../components/SelectorActividad'
import SelectorDia from '../components/SelectorDia'
import SelectorTurno from '../components/SelectorTurno'
import TarjetaVisitante from '../components/TarjetaVisitante'
import { USUARIO_ACTUAL } from '../datos/usuario'
import { useActividades } from '../hooks/useActividades'
import { useAhora } from '../hooks/useAhora'
import { useTurnos } from '../hooks/useTurnos'
import { desdeFechaIso, desdeHorarioIso, estadoTurno } from '../utilidades/calendario'
import { diaLargo, hora, personas } from '../utilidades/formato'
import {
  emailValido,
  hayErrores,
  validarVisitantes,
  visitanteVacio
} from '../utilidades/validaciones'
import '../styles/inscripcion.css'

export default function InscripcionView () {
  const navigate = useNavigate()
  const ahora = useAhora()
  const { actividades, cargando: cargandoActividades, error: errorActividades } = useActividades()

  const [fecha, setFecha] = useState(null)
  const [nombreActividad, setNombreActividad] = useState(null)
  const [horario, setHorario] = useState(null)
  const [visitantes, setVisitantes] = useState([visitanteVacio()])
  const [abierta, setAbierta] = useState(0)
  const [email, setEmail] = useState(USUARIO_ACTUAL.email)
  const [aceptaTerminos, setAceptaTerminos] = useState(false)
  const [dialogoAbierto, setDialogoAbierto] = useState(false)
  const [intentoConfirmar, setIntentoConfirmar] = useState(false)
  const [enviando, setEnviando] = useState(false)
  const [errorEnvio, setErrorEnvio] = useState(null)

  const actividad = actividades.find((a) => a.nombre === nombreActividad)
  const turnos = useTurnos(nombreActividad, fecha)
  const turno = turnos.turnos.find((t) => t.horario === horario)
  const turnoValido = turno && estadoTurno(turno, visitantes.length, ahora) === 'disponible'
  const erroresVisitantes = validarVisitantes(visitantes, actividad)

  const faltantes = []
  if (!fecha) faltantes.push('elegir el día')
  if (!actividad) faltantes.push('elegir la actividad')
  if (!turnoValido) faltantes.push('elegir un horario disponible')
  if (hayErrores(erroresVisitantes)) faltantes.push('completar los datos de cada persona')
  if (!emailValido(email)) faltantes.push('ingresar un correo válido')
  if (!aceptaTerminos) faltantes.push('aceptar los términos y condiciones')

  function elegirFecha (iso) {
    setFecha(iso)
    setHorario(null)
    setErrorEnvio(null)
  }

  function elegirActividad (nombre) {
    if (nombre === nombreActividad) return
    setNombreActividad(nombre)
    setHorario(null)
    setAceptaTerminos(false)
    setErrorEnvio(null)
  }

  function cambiarCantidad (cantidad) {
    setVisitantes((actuales) => {
      if (cantidad > actuales.length) return [...actuales, visitanteVacio()]
      return actuales.slice(0, cantidad)
    })
    setAbierta(cantidad - 1)
  }

  function cambiarVisitante (indice, campo, valor) {
    setVisitantes((actuales) => actuales.map((v, i) => (i === indice ? { ...v, [campo]: valor } : v)))
  }

  async function confirmar () {
    setIntentoConfirmar(true)
    setErrorEnvio(null)
    if (faltantes.length > 0) {
      const primerConError = erroresVisitantes.findIndex((e) => Object.keys(e).length > 0)
      if (primerConError >= 0) setAbierta(primerConError)
      return
    }
    setEnviando(true)
    try {
      const inscripcion = await crearInscripcion({
        actividad: actividad.nombre,
        horario,
        email,
        acepta_terminos: aceptaTerminos,
        visitantes: visitantes.map((v) => ({
          nombre: v.nombre.trim(),
          dni: v.dni,
          edad: Number(v.edad),
          talle: actividad.requiere_talle ? v.talle : null
        }))
      })
      navigate(`/confirmacion/${inscripcion.codigo}`, {
        state: { inscripcion, visitantes, email }
      })
    } catch (error) {
      setErrorEnvio(error.message)
      if (error.estado === 409 || error.estado === 422) turnos.recargar()
    } finally {
      setEnviando(false)
    }
  }

  return (
    <>
      <Encabezado />
      <main className='inscripcion'>
        <div className='inscripcion__intro'>
          <h1>Inscribite a una actividad</h1>
          <p>Reservá tu lugar en la Tirolesa, el Safari, la Palestra o el taller de Jardinería.</p>
        </div>

        <div className='inscripcion__pasos'>
          <Paso
            numero={1}
            titulo='Elegí el día'
            resumen={fecha && diaLargo(desdeFechaIso(fecha))}
            habilitado
          >
            <SelectorDia ahora={ahora} fecha={fecha} onElegir={elegirFecha} />
          </Paso>

          <Paso numero={2} titulo='Elegí la actividad' resumen={nombreActividad} habilitado={Boolean(fecha)}>
            {cargandoActividades && <p className='nota'>Cargando actividades…</p>}
            {errorActividades && <p className='aviso aviso--error' role='alert'>{errorActividades}</p>}
            <SelectorActividad
              actividades={actividades}
              elegida={nombreActividad}
              onElegir={elegirActividad}
            />
          </Paso>

          <Paso
            numero={3}
            titulo='Elegí el horario'
            resumen={turnoValido && hora(desdeHorarioIso(horario))}
            habilitado={Boolean(fecha && actividad)}
          >
            {actividad && (
              <SelectorTurno
                fecha={fecha}
                ahora={ahora}
                turnos={turnos.turnos}
                cargando={turnos.cargando}
                error={turnos.error}
                cupoPorTurno={actividad.cupo_por_turno}
                cantidadPersonas={visitantes.length}
                elegido={horario}
                onElegir={setHorario}
              />
            )}
          </Paso>

          <Paso
            numero={4}
            titulo='Cargá los participantes'
            resumen={turnoValido && personas(visitantes.length)}
            habilitado={Boolean(turnoValido)}
          >
            {turno && (
              <ContadorPersonas
                cantidad={visitantes.length}
                maximo={turno.cupos_disponibles}
                onCambiar={cambiarCantidad}
              />
            )}
            <div className='visitantes'>
              {visitantes.map((visitante, indice) => (
                <TarjetaVisitante
                  key={indice}
                  indice={indice}
                  visitante={visitante}
                  actividad={actividad}
                  errores={erroresVisitantes[indice]}
                  mostrarErrores={intentoConfirmar}
                  abierta={abierta === indice}
                  onAlternar={(i) => setAbierta(abierta === i ? -1 : i)}
                  onCambiar={cambiarVisitante}
                />
              ))}
            </div>
          </Paso>

          <Paso numero={5} titulo='Confirmá tus datos' habilitado={Boolean(turnoValido)}>
            <div className={`campo ${intentoConfirmar && !emailValido(email) ? 'campo--error' : ''}`}>
              <label htmlFor='email'>Correo para recibir la confirmación y el QR</label>
              <input
                id='email'
                type='email'
                autoComplete='email'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              {intentoConfirmar && !emailValido(email) && (
                <span className='campo__error'>Revisá el correo: no tiene un formato válido.</span>
              )}
            </div>
            {actividad && (
              <div className={`terminos ${intentoConfirmar && !aceptaTerminos ? 'terminos--error' : ''}`}>
                <label className='terminos__aceptar'>
                  <input
                    type='checkbox'
                    checked={aceptaTerminos}
                    onChange={(e) => setAceptaTerminos(e.target.checked)}
                  />
                  <span>Acepto los términos y condiciones de {actividad.nombre}</span>
                </label>
                <button type='button' className='enlace' onClick={() => setDialogoAbierto(true)}>
                  Leer los términos de {actividad.nombre}
                </button>
              </div>
            )}
          </Paso>
        </div>

        <div className='inscripcion__lateral'>
          {errorEnvio && (
            <p className='aviso aviso--error' role='alert'>{errorEnvio}</p>
          )}
          <ResumenReserva
            fecha={fecha}
            actividad={nombreActividad}
            horario={turnoValido ? horario : null}
            cantidad={visitantes.length}
            faltantes={intentoConfirmar ? faltantes : []}
            enviando={enviando}
            onConfirmar={confirmar}
          />
        </div>
      </main>

      {actividad && (
        <DialogoTerminos
          actividad={actividad.nombre}
          abierto={dialogoAbierto}
          onCerrar={() => setDialogoAbierto(false)}
          onAceptar={() => {
            setAceptaTerminos(true)
            setDialogoAbierto(false)
          }}
        />
      )}
    </>
  )
}
