import { useEffect, useRef } from 'react'
import terminos from '../datos/terminos.json'
import { seccionesDeTerminos } from '../utilidades/terminos'

export default function DialogoTerminos ({ actividad, abierto, onCerrar, onAceptar }) {
  const dialogo = useRef(null)

  useEffect(() => {
    const elemento = dialogo.current
    if (!elemento) return
    if (abierto && !elemento.open) elemento.showModal()
    if (!abierto && elemento.open) elemento.close()
  }, [abierto])

  return (
    <dialog
      ref={dialogo}
      className='dialogo'
      aria-labelledby='terminos-titulo'
      onClose={onCerrar}
    >
      <header className='dialogo__encabezado'>
        <p className='dialogo__eyebrow'>Términos y condiciones · versión {terminos.version}</p>
        <h2 id='terminos-titulo'>{actividad}</h2>
      </header>
      <div className='dialogo__cuerpo'>
        {seccionesDeTerminos(actividad).map((seccion) => (
          <section key={seccion.titulo}>
            <h3>{seccion.titulo}</h3>
            <ol>
              {seccion.puntos.map((punto) => <li key={punto}>{punto}</li>)}
            </ol>
          </section>
        ))}
      </div>
      <footer className='dialogo__pie'>
        <button type='button' className='boton boton--secundario' onClick={onCerrar}>
          Cerrar
        </button>
        <button type='button' className='boton' onClick={onAceptar}>
          Acepto los términos
        </button>
      </footer>
    </dialog>
  )
}
