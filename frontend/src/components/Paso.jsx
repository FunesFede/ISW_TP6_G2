// Cada paso del formulario. El número indica el orden del proceso que
// describe el dominio: día, actividad, horario, personas y términos.
export default function Paso ({ numero, titulo, resumen, habilitado, children }) {
  return (
    <section
      className={`paso ${habilitado ? '' : 'paso--bloqueado'}`}
      aria-labelledby={`paso-${numero}`}
      aria-disabled={!habilitado}
    >
      <header className='paso__encabezado'>
        <span className='paso__numero' aria-hidden='true'>{numero}</span>
        <h2 id={`paso-${numero}`} className='paso__titulo'>{titulo}</h2>
        {resumen && <span className='paso__resumen'>{resumen}</span>}
      </header>
      {habilitado && <div className='paso__cuerpo'>{children}</div>}
    </section>
  )
}
