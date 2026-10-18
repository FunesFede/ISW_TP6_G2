import { desdeFechaIso, desdeHorarioIso } from '../utilidades/calendario'
import { diaLargo, hora, personas } from '../utilidades/formato'

export default function ResumenReserva ({
  fecha, actividad, horario, cantidad, faltantes, enviando, onConfirmar
}) {
  const filas = [
    ['Día', fecha ? diaLargo(desdeFechaIso(fecha)) : '—'],
    ['Actividad', actividad ?? '—'],
    ['Horario', horario ? `${hora(desdeHorarioIso(horario))} a ${hora(new Date(desdeHorarioIso(horario).getTime() + 3600000))}` : '—'],
    ['Participantes', personas(cantidad)]
  ]
  const listo = faltantes.length === 0

  return (
    <aside className='resumen' aria-label='Resumen de la inscripción'>
      <h2 className='resumen__titulo'>Tu inscripción</h2>
      <dl className='resumen__datos'>
        {filas.map(([etiqueta, valor]) => (
          <div key={etiqueta} className='resumen__fila'>
            <dt>{etiqueta}</dt>
            <dd>{valor}</dd>
          </div>
        ))}
      </dl>
      {!listo && (
        <p className='resumen__faltante'>Falta: {faltantes.join(', ')}.</p>
      )}
      <button
        type='button'
        className='boton boton--ancho'
        onClick={onConfirmar}
        disabled={enviando}
      >
        {enviando ? 'Confirmando…' : 'Confirmar inscripción'}
      </button>
    </aside>
  )
}
