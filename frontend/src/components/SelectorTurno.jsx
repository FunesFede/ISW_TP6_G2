import ReglaDelDia from './ReglaDelDia'
import {
  aperturaInscripcion,
  desdeHorarioIso,
  estadoTurno
} from '../utilidades/calendario'
import { fechaHora, hora } from '../utilidades/formato'

function detalle (estado, turno) {
  const inicio = desdeHorarioIso(turno.horario)
  switch (estado) {
    case 'por-abrir':
      return `Abre ${fechaHora(aperturaInscripcion(inicio))}`
    case 'cerrado':
      return 'Inscripción cerrada'
    case 'agotado':
      return 'Sin lugares'
    case 'insuficiente':
      return `Quedan ${turno.cupos_disponibles}`
    default:
      return turno.cupos_disponibles === 1
        ? 'Queda 1 lugar'
        : `${turno.cupos_disponibles} lugares`
  }
}

export default function SelectorTurno ({
  fecha, ahora, turnos, cargando, error, cupoPorTurno, cantidadPersonas, elegido, onElegir
}) {
  if (cargando && turnos.length === 0) {
    return <p className='nota'>Buscando horarios…</p>
  }
  if (error) {
    return <p className='aviso aviso--error' role='alert'>{error}</p>
  }
  if (turnos.length === 0) {
    return <p className='nota'>No hay turnos para este día.</p>
  }

  return (
    <>
      <ReglaDelDia fecha={fecha} ahora={ahora} />
      <div className='turnos' role='radiogroup' aria-label='Horario'>
        {turnos.map((turno) => {
          const estado = estadoTurno(turno, cantidadPersonas, ahora)
          const seleccionado = turno.horario === elegido
          const ocupacion = 1 - turno.cupos_disponibles / cupoPorTurno
          const elegible = estado === 'disponible'
          return (
            <button
              key={turno.horario}
              type='button'
              role='radio'
              aria-checked={seleccionado}
              className={`turno turno--${estado} ${seleccionado ? 'turno--elegido' : ''}`}
              disabled={!elegible}
              onClick={() => onElegir(turno.horario)}
            >
              <span className='turno__hora'>{hora(desdeHorarioIso(turno.horario))}</span>
              <span
                className='turno__cupo'
                style={{ '--ocupacion': ocupacion }}
                aria-hidden='true'
              />
              <span className='turno__detalle'>{detalle(estado, turno)}</span>
            </button>
          )
        })}
      </div>
      <p className='nota'>
        La barra de cada horario muestra cuántos lugares ya están reservados.
      </p>
    </>
  )
}
