import {
  APERTURA_PARQUE,
  CIERRE_PARQUE,
  desdeFechaIso
} from '../utilidades/calendario'
import { hora } from '../utilidades/formato'

const INICIO = APERTURA_PARQUE.horas * 60 + APERTURA_PARQUE.minutos
const FIN = CIERRE_PARQUE.horas * 60 + CIERRE_PARQUE.minutos
const MARCAS = [11, 13, 15, 17, 19]

function posicion (minutos) {
  return `${((minutos - INICIO) / (FIN - INICIO)) * 100}%`
}

// Franja horaria del parque (8:30 a 19:00) con la hora actual marcada.
// Muestra de un vistazo qué parte del día ya pasó para el día elegido.
export default function ReglaDelDia ({ fecha, ahora }) {
  const dia = desdeFechaIso(fecha)
  const esHoy = dia.toDateString() === ahora.toDateString()
  const minutosAhora = ahora.getHours() * 60 + ahora.getMinutes()
  const dentro = esHoy && minutosAhora > INICIO && minutosAhora < FIN
  const pasado = esHoy ? Math.min(Math.max(minutosAhora, INICIO), FIN) : INICIO

  return (
    <div className='regla' aria-hidden='true'>
      <div className='regla__franja'>
        <div className='regla__pasado' style={{ width: posicion(pasado) }} />
        {dentro && (
          <div className='regla__ahora' style={{ left: posicion(minutosAhora) }}>
            <span className='regla__ahora-texto'>Ahora {hora(ahora)}</span>
          </div>
        )}
      </div>
      <div className='regla__marcas'>
        <span className='regla__marca' style={{ left: 0 }}>8:30</span>
        {MARCAS.map((marca) => (
          <span key={marca} className='regla__marca' style={{ left: posicion(marca * 60) }}>
            {marca}
          </span>
        ))}
      </div>
    </div>
  )
}
