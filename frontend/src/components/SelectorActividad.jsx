import terminos from '../datos/terminos.json'

function requisitos (actividad) {
  const etiquetas = [
    actividad.edad_minima > 0 ? `Desde ${actividad.edad_minima} años` : 'Todas las edades'
  ]
  if (actividad.requiere_talle) etiquetas.push('Pide talle')
  etiquetas.push(`${actividad.cupo_por_turno} lugares por turno`)
  return etiquetas
}

export default function SelectorActividad ({ actividades, elegida, onElegir }) {
  return (
    <div className='actividades' role='radiogroup' aria-label='Actividad'>
      {actividades.map((actividad) => {
        const seleccionada = elegida === actividad.nombre
        return (
          <button
            key={actividad.nombre}
            type='button'
            role='radio'
            aria-checked={seleccionada}
            className={`actividad ${seleccionada ? 'actividad--elegida' : ''}`}
            onClick={() => onElegir(actividad.nombre)}
          >
            <span className='actividad__nombre'>{actividad.nombre}</span>
            <span className='actividad__resumen'>
              {terminos.actividades[actividad.nombre]?.resumen}
            </span>
            <span className='actividad__requisitos'>
              {requisitos(actividad).map((texto) => (
                <span key={texto} className='etiqueta'>{texto}</span>
              ))}
            </span>
          </button>
        )
      })}
    </div>
  )
}
