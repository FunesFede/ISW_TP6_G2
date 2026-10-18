# Estilos de código

Usamos las reglas de estilo definidas por la comunidad de cada lenguaje,
sin modificaciones propias salvo las aclaradas abajo.

## Backend (Python)

Usamos las reglas **PEP 8** definidas por la comunidad de Python:
https://peps.python.org/pep-0008/

El cumplimiento se verifica automáticamente con **flake8**, configurado
en `backend/.flake8` con el largo de línea de PEP 8 (79 caracteres):

```bash
cd backend
python -m flake8 app tests
```

Convenciones que aplicamos dentro de PEP 8:

- Nombres de clases en `PascalCase` (`ServicioInscripcion`), funciones,
  métodos y variables en `snake_case` (`validar_talles`), constantes en
  `MAYUSCULAS` (`HORA_APERTURA`).
- Métodos internos de una clase con prefijo `_` (`_obtener_turno`).
- Imports agrupados en este orden, separados por una línea en blanco:
  biblioteca estándar, bibliotecas de terceros, módulos del proyecto.
- Anotaciones de tipo en las firmas públicas.
- Nombres del dominio en español, igual que en la User Story
  (`Visitante`, `Turno`, `Inscripcion`).

### Pruebas

- Archivos `test_<modulo>.py` dentro de `backend/tests/`.
- Cada prueba se nombra por el comportamiento que verifica y su
  resultado esperado: `test_inscripcion_sin_cupo_en_el_horario_falla`.
- Cada prueba sigue la estructura Preparar, Actuar, Verificar, separando
  cada parte con una línea en blanco.

## Frontend (React + Vite)

Usamos las **Reglas de React** definidas por la comunidad de React:
https://react.dev/reference/rules

- Los componentes y hooks son funciones puras: mismo resultado para las
  mismas props y estado, sin efectos secundarios durante el render.
- Las props y el estado se tratan como inmutables.
- Los hooks se llaman solo en el nivel superior de componentes o de
  otros hooks, nunca dentro de condiciones o bucles.
- Los componentes se usan en JSX y no se llaman como funciones comunes.

Convenciones de nombres de la comunidad:

- Componentes en `PascalCase`, un componente por archivo con el mismo
  nombre (`TarjetaVisitante.jsx`).
- Hooks propios con prefijo `use` (`useTurnos`).

El cumplimiento se verifica con ESLint y el plugin oficial
`eslint-plugin-react-hooks`, configurados en `frontend/eslint.config.js`:

```bash
cd frontend
npm run lint
```

## Mensajes de commit

Formato `tipo(fase): descripción`. El historial tiene un commit por fase
del ciclo TDD:

- `test(red)`: las pruebas, que fallan porque todavía no existe el
  código.
- `feat(green)`: el código mínimo para que las pruebas pasen.
- `refactor`: las mejoras de diseño sin cambiar el comportamiento, con
  todas las pruebas en verde.
