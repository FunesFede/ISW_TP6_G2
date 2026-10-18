# EcoHarmony Park — Inscribirme a actividad (TDD)

Trabajo Práctico N° 6 · Grupo N° 2 · 4K1 · Ingeniería y Calidad de
Software. Implementación de la User Story **Inscribirme a actividad**
aplicando Desarrollo Conducido por Pruebas (Red-Green-Refactor).

> COMO visitante QUIERO inscribirme a una actividad PARA reservar mi
> lugar en la misma.

Repositorio: https://github.com/FunesFede/ISW_TP6_G2

| Capa | Tecnología | Estilo de código |
|---|---|---|
| Backend | Python 3.11+, FastAPI, pytest | PEP 8 (flake8) |
| Frontend | JavaScript, React + Vite | Reglas de React (ESLint) |

El detalle de los estilos está en
[ESTILOS_DE_CODIGO.md](ESTILOS_DE_CODIGO.md) y la justificación del
diseño en [docs/Decisiones_de_diseno.pdf](docs/Decisiones_de_diseno.pdf).

## Cómo correrlo

Backend (queda en `http://127.0.0.1:8000`, con la documentación
interactiva de la API en `/docs`):

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Frontend, en otra terminal (queda en `http://localhost:5173`):

```bash
cd frontend
npm install
npm run dev
```

Si el backend corre en otra dirección, copiar `frontend/.env.example`
a `frontend/.env` y ajustar `VITE_API_URL`.

Pruebas y estilos:

```bash
cd backend
python -m pytest           # las 94 pruebas automatizadas
python -m flake8 app tests # PEP 8
cd ../frontend
npm run lint               # Reglas de React con ESLint
```

## Correo de confirmación y QR

El backend genera un QR real en PNG y arma el correo completo con el QR
adjunto. Al confirmar, el frontend ofrece abrir el correo en una ventana
aparte que replica un cliente de correo, con el mensaje que devuelve
`GET /inscripciones/{codigo}/correo`.

Sin configuración, cada correo también se guarda como archivo `.eml` en
`backend/bandeja_salida/`. Para enviarlo por SMTP real se definen las
variables `SMTP_HOST`, `SMTP_PUERTO`, `SMTP_USUARIO`, `SMTP_CLAVE` y
`MAIL_REMITENTE`.

## API

| Método y ruta | Uso |
|---|---|
| `GET /actividades` | Actividades con talle requerido, edad mínima y cupo por turno |
| `GET /actividades/{actividad}/turnos?fecha=AAAA-MM-DD` | Turnos del día con lugares disponibles y si la inscripción está abierta |
| `POST /inscripciones` | Registra la inscripción y envía el correo |
| `GET /inscripciones/{codigo}/correo` | Correo de confirmación con el QR adjunto |

Errores: 404 para actividad o inscripción inexistente, 409 para falta
de cupo o inscripción superpuesta, 422 para el resto de las reglas.

## Evidencia del ciclo TDD

El historial tiene un commit por fase del ciclo:

- `test(red)`: las 94 pruebas automatizadas, que fallan porque todavía
  no existe el código.
- `feat(green)`: el código que hace pasar todas las pruebas, y el
  frontend.
- `refactor`: las mejoras de diseño con todas las pruebas en verde
  (validaciones en `Visitante`, cupos y ventana de inscripción en
  `Turno`, conversiones en los esquemas de la API, dobles de prueba
  compartidos), y la documentación.

```bash
git log --oneline --reverse
```

## Trazabilidad con la User Story

| Prueba de usuario / criterio | Prueba automatizada |
|---|---|
| Inscripción válida con cupo, horario, datos, términos y mail (pasa) | `test_inscripcion_valida_devuelve_inscripcion_confirmada`, `test_inscripcion_exitosa_envia_mail_de_confirmacion_con_qr`, `test_post_inscripcion_valida_responde_201` |
| Actividad sin cupo en el horario (falla) | `test_inscripcion_sin_cupo_en_el_horario_falla`, `test_inscripcion_de_grupo_mayor_a_los_cupos_restantes_falla`, `test_post_inscripcion_sin_cupo_responde_409` |
| Sin talle cuando la actividad no lo requiere (pasa) | `test_inscripcion_sin_talle_a_actividad_que_no_lo_requiere_pasa` |
| Parque cerrado en el horario (falla) | `test_inscripcion_con_el_parque_cerrado_falla`, `tests/test_calendario_parque.py` |
| Actividad no disponible en el horario (falla) | `test_inscripcion_en_horario_sin_turno_de_la_actividad_falla` |
| Sin aceptar términos y condiciones (falla) | `test_inscripcion_sin_aceptar_terminos_y_condiciones_falla` |
| Sin talle cuando la actividad lo requiere (falla) | `test_inscripcion_sin_talle_a_actividad_que_lo_requiere_falla` |
| Solo actividades del listado | `test_inscripcion_a_actividad_fuera_del_listado_falla` |
| Cantidad de personas y datos de cada visitante | `test_inscripcion_sin_visitantes_falla`, `test_inscripcion_con_datos_de_visitante_invalidos_falla` |
| Reservar el lugar | `test_inscripcion_exitosa_descuenta_los_cupos_del_turno`, `test_inscripcion_fallida_no_descuenta_cupos` |
| Mail con código QR | `test_inscripcion_exitosa_envia_mail_de_confirmacion_con_qr`, `tests/test_notificacion.py` |

Reglas que surgen de las respuestas de los PO (FAQ):

| Regla (FAQ) | Prueba automatizada |
|---|---|
| Parque abierto de martes a domingo de 8:30 a 19; cerrado 25/12 y 1/1 (1 y 11) | `tests/test_calendario_parque.py` |
| Turnos de 9 a 17, uno por hora; cupos Safari 8, Palestra 12, Jardinería 12, Tirolesa 10 (12 y 13) | `tests/test_datos_iniciales.py` |
| Talles XS, S, M, L, XL, XXL (14) | `test_inscripcion_con_talle_valido_pasa`, `test_inscripcion_con_talle_fuera_de_la_lista_falla` |
| Edad mínima: Palestra 12, Tirolesa 8 (15) | `test_inscripcion_con_visitante_menor_a_la_edad_minima_falla`, `test_inscripcion_con_visitante_de_la_edad_minima_pasa` |
| Inscripción desde 24 hs hasta 15 min antes del turno (23 y 30) | `test_inscripcion_dentro_de_la_ventana_pasa`, `test_inscripcion_con_mas_de_24_horas_de_anticipacion_falla`, `test_inscripcion_a_menos_de_15_minutos_del_turno_falla` |
| El visitante ve los cupos disponibles (8) | `test_get_turnos_de_una_actividad_en_una_fecha`, `test_get_turnos_indica_si_la_inscripcion_esta_abierta` |
| Una persona no puede estar en dos turnos del mismo horario (29) | `test_visitante_ya_inscripto_en_otra_actividad_del_mismo_horario_falla`, `test_visitante_ya_inscripto_en_el_mismo_turno_falla`, `test_post_inscripcion_superpuesta_responde_409` |
| Sin máximo de personas por inscripción, solo el cupo (31) | `test_inscripcion_de_grupo_mayor_a_los_cupos_restantes_falla` |

## Diseño

```
backend/app/
├── dominio/          reglas de negocio, sin dependencias externas
│   ├── actividades.py    catálogo: Tirolesa, Safari, Palestra, Jardinería
│   ├── modelos.py        Visitante, Turno, SolicitudInscripcion, Inscripcion
│   ├── excepciones.py    un error por regla incumplida
│   └── puertos.py        interfaces que el dominio necesita
├── servicios/
│   └── servicio_inscripcion.py   caso de uso "inscribir"
├── infraestructura/  implementaciones concretas de los puertos
│   ├── repositorio_turnos.py, repositorio_inscripciones.py
│   ├── calendario_parque.py, reloj.py
│   ├── generador_qr.py, notificador_mail.py
│   └── datos_iniciales.py
├── api/              FastAPI: esquemas y endpoints
└── main.py           arma las dependencias concretas

frontend/src/
├── views/            Inscripción, confirmación y ventana del correo
├── components/       Un componente por archivo (pasos, turnos, visitantes)
├── hooks/            useActividades, useTurnos, useAhora
├── utilidades/       Calendario, validaciones y formato
├── datos/            terminos.json y usuario de prueba
└── api/cliente.js    Llamadas al backend

docs/
├── Decisiones_de_diseno.pdf
├── Hoja_de_entrega_TP6_G2.pdf
├── terminos/         Un PDF de términos y condiciones por actividad
└── generar_pdfs.py   Genera los PDF desde sus fuentes
```

**Inyección de dependencias por puertos.** El servicio recibe el
repositorio de turnos, el repositorio de inscripciones, el calendario del
parque, el reloj, el notificador de mails y el generador de QR como
interfaces (`typing.Protocol`). Las pruebas
del dominio usan dobles (fakes y espías) y no necesitan base de datos,
servidor de correo ni red. Esta decisión surgió de TDD: para escribir la
prueba de "parque cerrado" hacía falta controlar el calendario desde el
test.

**Reloj inyectado.** La ventana de inscripción depende de la hora
actual. En lugar de llamar a `datetime.now()` dentro del servicio, la
hora llega por el puerto `Reloj`. Los tests fijan el momento exacto
(24 hs antes, 15 minutos antes, el turno ya empezado) sin esperar ni
depender del día en que se corren. `RelojSistema` devuelve la hora de
Córdoba.

**Responsabilidades en el objeto que tiene la información.** Durante
los refactors, la validación de nombre, DNI, edad y talle pasó al
`Visitante`; la regla de cupos y la ventana de inscripción pasaron a
`Turno`; el requisito de talle, el cupo por turno y la edad mínima son
atributos de `Actividad` en lugar de listas sueltas de nombres.

**Una excepción por regla de negocio.** Todas heredan de
`InscripcionError`. La API las traduce a HTTP en un único manejador:
404 actividad inexistente, 409 sin cupo o inscripción superpuesta,
422 el resto.

**Orden de validación.** Primero las validaciones que no consultan nada
externo (actividad, datos, talle, edad, términos), después calendario,
turno, ventana de inscripción y superposición, y recién al final se
reserva el cupo, se registra la inscripción y se envía el mail. Una solicitud
rechazada no descuenta cupos ni envía correo (hay pruebas para ambos).

## Respuestas del PO a las consultas del equipo

Además del FAQ, el PO respondió el formulario de consultas del equipo:

- El mail de confirmación puede ser simulado, en una ventana aparte que
  replique un cliente de correo. El backend igualmente arma el mail
  completo y puede enviarlo por SMTP.
- El QR se genera de forma real y uno solo por inscripción, que
  identifica la inscripción completa.
- Si el grupo supera los cupos restantes se rechaza la inscripción
  completa.
- El mail se toma del usuario logueado o se pide como un campo más; hoy
  se recibe en la solicitud.
- Exigir una entrada comprada para ese día queda fuera del alcance de
  esta User Story.
- Los menores no necesitan un adulto inscripto en el mismo turno.
- Las actividades no tienen costo aparte de la entrada, por eso el mail
  no incluye montos.
- Los términos y condiciones los redacta el equipo, uno por actividad, y
  se envían al PO para su validación.

## Otros supuestos

- DNI de 7 u 8 dígitos sin puntos (el FAQ 32 confirma que solo se pide
  DNI).
- Turnos e inscripciones se guardan en memoria; para persistir alcanza
  con otras implementaciones de `RepositorioTurnos` y
  `RepositorioInscripciones`.
