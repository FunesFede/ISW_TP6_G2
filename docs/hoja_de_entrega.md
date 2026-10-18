# Inscribirme a actividad

**User Story:** COMO visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.

| Capa | Lenguaje | Framework | Estilo de código |
|---|---|---|---|
| Backend | Python 3.11+ | FastAPI, pruebas con pytest | PEP 8, verificado con flake8 |
| Frontend | JavaScript | React + Vite | Reglas de React, verificadas con ESLint |

**Repositorio:** https://github.com/FunesFede/ISW_TP6_G2

## Pasos para ejecutar la User Story

**Paso 1.** Clonar el repositorio y entrar a la carpeta:

```bash
git clone [https://github.com/FunesFede/ISW_TP6_G2.git](https://github.com/FunesFede/ISW_TP6_G2.git)
cd ISW_TP6_G2
```

**Paso 2.** Instalar las dependencias y levantar el backend, que queda en http://127.0.0.1:8000:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Paso 3.** En otra terminal, desde la carpeta del repositorio, instalar las dependencias y levantar el frontend, que queda en http://localhost:5173:
```bash
cd frontend
npm install
npm run dev
```

**Paso 4.** Ejecutar las pruebas automatizadas y verificar los estilos de código:
```bash
cd backend
python -m pytest
python -m flake8 app tests
cd ../frontend
npm run lint
```

## Evidencia del ciclo TDD

El desarrollo se estructuró de forma incremental a lo largo de **6 ciclos completos de TDD (`Red -> Green -> Refactor`)**, sumando las 94 pruebas automatizadas progresivamente a medida que emergía el diseño de cada componente:

1. **Ciclo 1 (Calendario y Reloj):** Pruebas y lógica de días/horarios de apertura del parque, feriados y zona horaria (`test(red)` -> `feat(green)` -> `refactor` de puertos).
2. **Ciclo 2 (Dominio y Turnos Iniciales):** Catálogo de actividades, cupos por defecto, modelos de dominio y repositorios en memoria.
3. **Ciclo 3 (Servicio de Inscripción - Caso feliz y cupos):** Flujo principal de reserva, control de disponibilidad y descuento de cupos con dobles de prueba.
4. **Ciclo 4 (Reglas de Visitantes y Ventana Horaria):** Validaciones de talles, edades mínimas, anticipación de 24 h a 15 min y control de inscripciones superpuestas.
5. **Ciclo 5 (Notificación y Código QR):** Generación del QR en formato PNG y envío de confirmación mediante adaptadores de bandeja local y SMTP.
6. **Ciclo 6 (Capa API REST):** Pruebas de integración con `TestClient`, endpoints en FastAPI y traducción de excepciones de dominio a códigos de estado HTTP.

Una vez consolidada y probada toda la lógica de negocio en el backend, se integró el frontend en commits dedicados (`feat(frontend)`) y finalmente la documentación (`docs`). La traza completa puede verificarse ejecutando `git log --oneline --reverse`.

En la carpeta `docs` se encuentran el documento de decisiones de diseño y los términos y condiciones de cada actividad.

