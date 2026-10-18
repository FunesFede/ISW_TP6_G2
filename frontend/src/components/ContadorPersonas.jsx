import { personas } from '../utilidades/formato'

export default function ContadorPersonas ({ cantidad, maximo, onCambiar }) {
  return (
    <div className='contador'>
      <span className='contador__etiqueta' id='etiqueta-personas'>
        ¿Cuántas personas participan?
      </span>
      <div className='contador__control' role='group' aria-labelledby='etiqueta-personas'>
        <button
          type='button'
          className='contador__boton'
          onClick={() => onCambiar(cantidad - 1)}
          disabled={cantidad <= 1}
          aria-label='Quitar una persona'
        >
          −
        </button>
        <output className='contador__valor' aria-live='polite'>{personas(cantidad)}</output>
        <button
          type='button'
          className='contador__boton'
          onClick={() => onCambiar(cantidad + 1)}
          disabled={cantidad >= maximo}
          aria-label='Agregar una persona'
        >
          +
        </button>
      </div>
      <span className='contador__ayuda'>
        {cantidad >= maximo
          ? `Es el máximo de lugares que quedan en este horario (${maximo}).`
          : `Quedan ${maximo} lugares en este horario.`}
      </span>
    </div>
  )
}
