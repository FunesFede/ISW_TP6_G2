import { Link, useLocation, useParams } from 'react-router-dom'
import Encabezado from '../components/Encabezado'
import { desdeHorarioIso } from '../utilidades/calendario'
import { diaLargo, hora } from '../utilidades/formato'
import '../styles/confirmacion.css'

function abrirCorreo (codigo) {
  window.open(
    `/correo/${codigo}`,
    `correo-${codigo}`,
    'width=1000,height=760'
  )
}

export default function ConfirmacionView () {
  const { codigo } = useParams()
  const { state } = useLocation()
  const inscripcion = state?.inscripcion
  const inicio = inscripcion && desdeHorarioIso(inscripcion.horario)

  return (
    <>
      <Encabezado />
      <main className='confirmacion'>
        <section className='confirmacion__tarjeta' aria-labelledby='confirmacion-titulo'>
          <p className='confirmacion__eyebrow'>Inscripción confirmada</p>
          <h1 id='confirmacion-titulo'>
            {inscripcion
              ? `Tenés lugar en ${inscripcion.actividad}`
              : 'Tu inscripción está confirmada'}
          </h1>

          {inscripcion && (
            <dl className='confirmacion__datos'>
              <div>
                <dt>Día</dt>
                <dd>{diaLargo(inicio)}</dd>
              </div>
              <div>
                <dt>Horario</dt>
                <dd>{hora(inicio)} a {hora(new Date(inicio.getTime() + 3600000))}</dd>
              </div>
              <div>
                <dt>Participantes</dt>
                <dd>
                  <ul className='confirmacion__personas'>
                    {state.visitantes.map((v) => (
                      <li key={v.dni}>{v.nombre} <span>DNI {v.dni}</span></li>
                    ))}
                  </ul>
                </dd>
              </div>
            </dl>
          )}

          <div className='confirmacion__codigo'>
            <span>Código de inscripción</span>
            <strong>{codigo}</strong>
          </div>

          <p className='confirmacion__correo'>
            Te enviamos el resumen y el código QR
            {state?.email ? <> a <strong>{state.email}</strong></> : null}.
            Presentalo junto con el DNI de cada participante 10 minutos antes del turno.
          </p>

          <div className='confirmacion__acciones'>
            <button type='button' className='boton' onClick={() => abrirCorreo(codigo)}>
              Ver el correo de confirmación
            </button>
            <Link className='boton boton--secundario' to='/'>
              Hacer otra inscripción
            </Link>
          </div>
        </section>
      </main>
    </>
  )
}
