import { TALLES } from '../utilidades/validaciones'

function Campo ({ id, etiqueta, error, mostrarError, children }) {
  return (
    <div className={`campo ${mostrarError && error ? 'campo--error' : ''}`}>
      <label htmlFor={id}>{etiqueta}</label>
      {children}
      {mostrarError && error && (
        <span className='campo__error' id={`${id}-error`}>{error}</span>
      )}
    </div>
  )
}

export default function TarjetaVisitante ({
  indice, visitante, actividad, errores, mostrarErrores, abierta, onAlternar, onCambiar
}) {
  const prefijo = `visitante-${indice}`
  const conError = mostrarErrores && Object.keys(errores).length > 0
  const completo = Object.keys(errores).length === 0
  const atributos = (campo) => ({
    id: `${prefijo}-${campo}`,
    'aria-invalid': mostrarErrores && Boolean(errores[campo]),
    'aria-describedby': mostrarErrores && errores[campo] ? `${prefijo}-${campo}-error` : undefined
  })

  return (
    <article className={`visitante ${conError ? 'visitante--error' : ''}`}>
      <button
        type='button'
        className='visitante__encabezado'
        aria-expanded={abierta}
        aria-controls={`${prefijo}-datos`}
        onClick={() => onAlternar(indice)}
      >
        <span className='visitante__titulo'>
          Persona {indice + 1}
          <span className='visitante__nombre'>{visitante.nombre || 'Sin nombre'}</span>
        </span>
        <span className={`visitante__estado ${completo ? 'visitante__estado--ok' : ''}`}>
          {completo ? 'Completo' : conError ? 'Revisar' : 'Pendiente'}
        </span>
      </button>

      <div className='visitante__datos' id={`${prefijo}-datos`} hidden={!abierta}>
        <Campo id={`${prefijo}-nombre`} etiqueta='Nombre y apellido' error={errores.nombre} mostrarError={mostrarErrores}>
          <input
            {...atributos('nombre')}
            type='text'
            autoComplete='name'
            value={visitante.nombre}
            onChange={(e) => onCambiar(indice, 'nombre', e.target.value)}
          />
        </Campo>
        <div className='campos-en-linea'>
          <Campo id={`${prefijo}-dni`} etiqueta='DNI' error={errores.dni} mostrarError={mostrarErrores}>
            <input
              {...atributos('dni')}
              type='text'
              inputMode='numeric'
              maxLength={8}
              placeholder='Sin puntos'
              value={visitante.dni}
              onChange={(e) => onCambiar(indice, 'dni', e.target.value.replace(/\D/g, ''))}
            />
          </Campo>
          <Campo id={`${prefijo}-edad`} etiqueta='Edad' error={errores.edad} mostrarError={mostrarErrores}>
            <input
              {...atributos('edad')}
              type='text'
              inputMode='numeric'
              maxLength={3}
              value={visitante.edad}
              onChange={(e) => onCambiar(indice, 'edad', e.target.value.replace(/\D/g, ''))}
            />
          </Campo>
        </div>
        {actividad?.requiere_talle && (
          <fieldset className={`campo talles ${mostrarErrores && errores.talle ? 'campo--error' : ''}`}>
            <legend>Talle de vestimenta</legend>
            <div className='talles__opciones'>
              {TALLES.map((talle) => (
                <label key={talle} className='talle'>
                  <input
                    type='radio'
                    name={`${prefijo}-talle`}
                    value={talle}
                    checked={visitante.talle === talle}
                    onChange={() => onCambiar(indice, 'talle', talle)}
                  />
                  <span>{talle}</span>
                </label>
              ))}
            </div>
            {mostrarErrores && errores.talle && (
              <span className='campo__error'>{errores.talle}</span>
            )}
          </fieldset>
        )}
      </div>
    </article>
  )
}
