import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { obtenerCorreo } from '../api/cliente'
import { fechaHora } from '../utilidades/formato'
import '../styles/correo.css'

// Simulación del cliente de correo del visitante (FAQ 5 y respuesta 1 del
// PO). Muestra el mismo mensaje que arma el backend, con el QR adjunto.
export default function CorreoView () {
  const { codigo } = useParams()
  const [correo, setCorreo] = useState(null)
  const [error, setError] = useState(null)
  const [recibido] = useState(() => new Date())

  useEffect(() => {
    let vigente = true
    obtenerCorreo(codigo)
      .then((datos) => { if (vigente) setCorreo(datos) })
      .catch((err) => { if (vigente) setError(err.message) })
    return () => { vigente = false }
  }, [codigo])

  useEffect(() => {
    document.title = correo ? `${correo.asunto} · Correo` : 'Correo'
  }, [correo])

  const qr = correo && `data:${correo.adjunto.tipo};base64,${correo.adjunto.contenido_base64}`

  return (
    <div className='correo'>
      <header className='correo__barra'>
        <span className='correo__app'>Correo</span>
        <span className='correo__cuenta'>{correo?.destinatario ?? '…'}</span>
      </header>

      <div className='correo__cuerpo'>
        <nav className='correo__bandeja' aria-label='Bandeja de entrada'>
          <h2 className='correo__bandeja-titulo'>Recibidos</h2>
          {correo && (
            <div className='correo__item correo__item--activo' aria-current='true'>
              <span className='correo__item-remitente'>EcoHarmony Park</span>
              <span className='correo__item-asunto'>{correo.asunto}</span>
              <span className='correo__item-hora'>{fechaHora(recibido)}</span>
            </div>
          )}
        </nav>

        <main className='correo__lectura'>
          {error && <p className='aviso aviso--error' role='alert'>{error}</p>}
          {!correo && !error && <p className='nota'>Abriendo el correo…</p>}
          {correo && (
            <article>
              <h1 className='correo__asunto'>{correo.asunto}</h1>
              <div className='correo__cabecera'>
                <span className='correo__avatar' aria-hidden='true'>
                  <img src='/simbolo-ecoharmony.png' alt='' />
                </span>
                <div className='correo__participantes'>
                  <p><strong>EcoHarmony Park</strong> &lt;{correo.remitente}&gt;</p>
                  <p>Para: {correo.destinatario}</p>
                </div>
                <time className='correo__fecha'>{fechaHora(recibido)}</time>
              </div>

              <div className='correo__mensaje'>{correo.cuerpo}</div>

              <section className='correo__adjuntos' aria-label='Archivos adjuntos'>
                <h2>1 archivo adjunto</h2>
                <figure className='adjunto'>
                  <img src={qr} alt={`Código QR de la inscripción ${codigo}`} width='180' height='180' />
                  <figcaption>
                    <span className='adjunto__nombre'>{correo.adjunto.nombre}</span>
                    <a href={qr} download={correo.adjunto.nombre}>Descargar</a>
                  </figcaption>
                </figure>
              </section>
            </article>
          )}
        </main>
      </div>
    </div>
  )
}
