import {
  aFechaIso,
  inscripcionHabilitadaElDia,
  parqueAbreElDia,
  proximosDias
} from '../utilidades/calendario'
import { diaSemanaCorto } from '../utilidades/formato'

const DIAS_VISIBLES = 7

function motivoDeshabilitado (dia, ahora) {
  if (!parqueAbreElDia(dia)) return 'Cerrado'
  if (!inscripcionHabilitadaElDia(dia, ahora)) {
    return dia > ahora ? 'Aún no' : 'Terminó'
  }
  return null
}

export default function SelectorDia ({ ahora, fecha, onElegir }) {
  const dias = proximosDias(ahora, DIAS_VISIBLES)

  return (
    <>
      <div className='dias' role='radiogroup' aria-label='Día de la actividad'>
        {dias.map((dia) => {
          const iso = aFechaIso(dia)
          const motivo = motivoDeshabilitado(dia, ahora)
          const elegido = iso === fecha
          return (
            <button
              key={iso}
              type='button'
              role='radio'
              aria-checked={elegido}
              className={`dia ${elegido ? 'dia--elegido' : ''}`}
              disabled={motivo !== null}
              title={motivo === 'Aún no' ? 'La inscripción abre 24 horas antes de cada turno' : undefined}
              onClick={() => onElegir(iso)}
            >
              <span className='dia__semana'>{diaSemanaCorto(dia)}</span>
              <span className='dia__numero'>{dia.getDate()}</span>
              <span className='dia__estado'>{motivo ?? 'Abierto'}</span>
            </button>
          )
        })}
      </div>
      <p className='nota'>
        Cada turno se puede reservar desde 24 horas antes hasta 15 minutos antes de
        empezar. El parque cierra los lunes, el 25 de diciembre y el 1 de enero.
      </p>
    </>
  )
}
