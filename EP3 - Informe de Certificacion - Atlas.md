# Informe de seguridad y calidad en el desarrollo de software

## ISY1102 — Seguridad y Calidad en el Desarrollo de Software

### Sección 002V

Carrera: Ingeniería en Desarrollo de Software

Docente: Christian Rodrigo Alvarez Lobos

Fecha: 29 de octubre de 2026 · versión revisada

**Integrantes:**

Luis Tasso

Miguel Arredondo

Nicolas Iturrieta

<!-- pagebreak -->

# ÍNDICE

1. Introducción

1.1. Ajustes según retroalimentación de la EP1

2. Criterios de calidad

2.1. Calidad del producto

2.2. Seguridad

2.3. Cumplimiento normativo

3. Plan de pruebas

3.1. Estrategia de pruebas

3.2. Tipos de prueba

3.3. Criterios de aceptación

3.4. Herramientas utilizadas

3.5. Cronograma de ejecución

4. Diseño de casos de prueba

4.1. Fichas de casos representativos

4.2. Matriz de trazabilidad de requisitos

5. Ejecución de pruebas

5.1. Resumen de ejecución

5.2. Detalle de ejecución de casos

5.3. Criticidad de incidentes

6. Análisis ético y normativo de los resultados

6.1. Consideraciones éticas

6.2. Consideraciones normativas

6.3. Dictamen y acciones correctivas

7. Anexos y evidencias

<!-- pagebreak -->

## 1. Introducción

**Contexto del sistema a evaluar.** Atlas es una plataforma web de gestión de clientes y contratos orientada a pequeñas y medianas empresas (pymes) de Chile. El sistema se estructura en tres capas: un frontend construido con React y Material UI (SPA responsiva), un backend con Express/Node.js que expone una API REST, y una base de datos PostgreSQL. Permite a usuarios registrados por empresa gestionar clientes, contratos y documentos asociados, administrar usuarios y roles (administrador/editor), auditar acciones críticas y gestionar el ciclo de vida de los contratos.

**Propósito del informe.** Este documento presenta los resultados de la verificación de calidad y seguridad del software Atlas, ejecutada sobre el código fuente entregado (Caso A) y el despliegue en Docker de laboratorio. El objetivo es determinar, con evidencias reproducibles, si el sistema cumple los requisitos funcionales y no funcionales del ERS, los estándares de calidad (ISO/IEC 25010), los controles de seguridad (ISO/IEC 27001, OWASP Top 10) y la normativa chilena de protección de datos (Ley 19.628 y Ley 21.719), para sustentar una decisión de certificación.

**Alcance.** Módulos verificados: autenticación y sesión, clientes, contratos y documentos, usuarios y roles, métricas/dashboard y auditoría. Se aplicaron pruebas funcionales y de seguridad sobre la API, revisión manual del código fuente, análisis estático con ESLint 9 y análisis estático con SonarQube 10.6 (backend y frontend).

**Estructura del informe.** El documento se organiza en: criterios de calidad (sección 2); plan de pruebas con estrategia, tipos, criterios de aceptación y herramientas (sección 3); diseño de casos de prueba con sus fichas y trazabilidad al ERS (sección 4); ejecución de pruebas con resumen, detalle y criticidad de incidentes (sección 5); análisis ético y normativo de los resultados con el dictamen final (sección 6); y anexos con las evidencias completas (sección 7).

### 1.1. Ajustes según retroalimentación de la EP1

Sobre la base del feedback entregado por el docente en la Evaluación Parcial N.º 1 (Plan de Pruebas), este informe incorpora los siguientes ajustes:

- **Evidencia dinámica cruda:** cada caso funcional y de seguridad se respalda con la petición `curl` y la respuesta HTTP real del servidor, transcritas en el Anexo F. Los Anexos A y B quedan como síntesis y remiten al Anexo F; ya no son tablas escritas a mano.
- **Trazabilidad con identificadores reales del ERS:** la matriz (sección 4.2) usa los identificadores del ERS (`RF-1.1`, `RF-4`, `RF-5.2`, `RF-6.1`, `NFR-PERF-1`, `NFR-SEG-4`, `RB-2`, etc.) y declara cobertura real (cubierto / parcial / no cubierto). Se elimina la cobertura del 100 %: la cobertura plena alcanza 6 de 21 requisitos identificados (28,6 %).
- **Requisito de documentos corregido:** RF-5.2 admite PDF, DOC, PPT, JPG y PNG. El criterio de aceptación y el caso CP-010 se ajustan a esos cinco formatos; el defecto es aceptar `.exe` y `.html`, no rechazar formatos distintos de PDF.
- **Dos casos no funcionales formalizados:** CP-013 mide el rendimiento con cinco repeticiones y se registra como **FALLÓ**; CP-014 evalúa usabilidad y accesibilidad con una lista de verificación y Lighthouse. Ambos se contabilizan en el resumen de ejecución.
- **Plan con cronograma y ejecución trazable:** se agrega el cronograma de la sección 3.5 y el detalle de ejecución (sección 5.2) incorpora fecha y ejecutor en cada caso.
- **Análisis estático ampliado:** se incorpora SonarQube 10.6 sobre backend y frontend, además de ESLint 9 y la revisión manual, dejando métricas y capturas de pantalla como evidencia (Anexo E).
- **Dictamen formal:** se cierra el ciclo con un veredicto técnico explícito (NO CERTIFICADO) sustentado en criterios de aceptación previamente definidos (sección 6.3).

---

## 2. Criterios de calidad

Los criterios siguientes condicionan la aprobación del software y se derivan del ERS del Sistema Atlas y de los marcos normativos aplicables al contexto chileno.

### 2.1. Calidad del producto

Conforme al modelo ISO/IEC 25010 (SQuaRE), Atlas debe cumplir:

- **Usabilidad y accesibilidad:** interfaz responsiva (desktop, tablet, móvil), tipografía de tamaño de fuente 12 px, contraste suficiente, etiquetas ARIA, navegación por teclado y controles de tamaño mínimo para pantallas táctiles, con especial atención a usuarios adultos mayores (NFR-USAB).
- **Rendimiento:** tiempos de respuesta de operaciones CRUD menores a 300 ms bajo carga normal, carga de página principal menor a 2 s y soporte de 200 usuarios concurrentes (NFR-PERF).
- **Estabilidad y confiabilidad:** disponibilidad objetivo 99,5 % mensual (NFR-DIS-1) y tolerancia a fallos sin pérdida de datos; las operaciones de creación deben ser transaccionales.
- **Confiabilidad:** integridad de la información ante fallos parciales (sin registros huérfanos) y comportamiento predecible ante entradas inválidas.
- **Mantenibilidad:** código legible, modular y documentado en frontend y backend, sin deuda técnica relevante (medible con SonarQube).

### 2.2. Seguridad

Conforme a ISO/IEC 27001, OWASP Top 10 y los requerimientos NFR-SEG del ERS:

- **Protección de datos:** cifrado de comunicaciones (TLS), cifrado de datos sensibles en reposo y almacenamiento seguro de contraseñas (bcrypt/argon2).
- **Control de acceso:** autenticación obligatoria en todos los endpoints que exponen datos, autorización por rol (admin/editor) y por pertenencia a empresa (RB-2, RB-4, RB-5), gestión de sesión JWT de corta vigencia (NFR-SEG-9).
- **Manejo de errores:** respuestas genéricas que no expongan detalles internos del motor de base de datos ni permitan enumeración de usuarios.
- **Integridad de la información:** validación y saneamiento de entradas para prevenir inyección SQL, XSS y CSRF; validación de tipo y contenido en la subida de archivos.
- **Gestión de secretos:** credenciales y claves fuera del código fuente (variables de entorno), registro de actividad segura (NFR-SEG-6) y respaldos (NFR-SEG-7).

### 2.3. Cumplimiento normativo

- **Ley 19.628 y Ley 21.719 (Protección de Datos Personales):** Atlas trata datos personales de clientes y usuarios; se exige consentimiento informado, minimización de datos, cifrado, control de acceso, trazabilidad y respeto al plazo de conservación. El almacenamiento de credenciales en texto claro y la exposición de datos sin autenticación constituyen incumplimientos directos.
- **ISO/IEC 27001:** controles A.9.4 (control de acceso), A.10 (criptografía), A.12.4 (registro de actividad) y A.18.1 (requisitos legales).
- **ISO/IEC 25010:** modelo de calidad aplicado en la sección 2.1.
- **WCAG / inclusión digital:** cumplimiento básico de estándares de accesibilidad.

---

## 3. Plan de pruebas

### 3.1. Estrategia de pruebas

- **Enfoque:** mixto (manual y automatizado). Se ejecutaron pruebas funcionales y de seguridad de forma manual reproducible sobre la API (`curl`), complementadas con análisis estático automatizado (ESLint, SonarQube) y revisión manual de código.
- **Etapas del proceso:**
  1. Definición del alcance y lectura del ERS y del código fuente.
  2. Diseño de casos de prueba con trazabilidad a requerimientos.
  3. Preparación del entorno (Docker Compose: frontend, backend y PostgreSQL con datos semilla).
  4. Ciclo 1: smoke test de las funciones base (si falla, se detiene la ejecución).
  5. Ciclo 2: ejecución de los casos funcionales, de seguridad y de rendimiento.
  6. Análisis estático (ESLint y SonarQube) y revisión manual del código fuente.
  7. Registro de resultados, clasificación de incidentes y generación de evidencias.
- **Priorización:** por impacto y riesgo; prioridad alta a autenticación (RF-1), clientes (RF-4), contratos/documentos (RF-5), auditoría (RF-6) y a los controles de seguridad y control de acceso.
- **Criterios de entrada:** sistema desplegado con Docker, base de datos inicializada con datos de prueba, casos diseñados y revisados, herramientas de análisis disponibles.
- **Criterios de salida:** todos los casos críticos ejecutados y evidenciados; sin defectos de severidad crítica abiertos; análisis estático sin vulnerabilidades BLOCKER/CRITICAL; hallazgos documentados y trazables a requerimientos.

### 3.2. Tipos de prueba

- **Pruebas funcionales (¿qué hace?):** verifican que cada operación cumple el requisito: login y emisión de token, CRUD de clientes, listado y búsqueda, contratos y documentos, dashboard/métricas, usuarios, roles y auditoría.
- **Pruebas de seguridad:** verificación dinámica de control de acceso (endpoints sin token), validación de subida de archivos, intento de inyección SQL en login, configuración CORS y fuerza bruta; complementadas con análisis estático (ESLint, SonarQube) y revisión manual del código fuente. Justificación: el ERS exige NFR-SEG y el código presenta hallazgos de control de acceso detectados en el EP1.
- **Pruebas de integración:** verificación de que frontend, API Express y PostgreSQL interactúan correctamente en los flujos completos (login → cliente → contrato → documento), incluida la documentación Swagger.
- **Pruebas no funcionales de rendimiento (CP-013):** cinco mediciones consecutivas de `GET /clientes` con token válido y red local sin carga, comparadas contra el umbral de 300 ms de NFR-PERF-1; se registran promedio, mínimo y máximo. Se detecta además la latencia artificial de 4 s insertada en el código (`delay(4000)`).
- **Pruebas no funcionales de usabilidad y accesibilidad (CP-014):** lista de verificación sobre la pantalla de inicio de sesión (legibilidad, contraste, etiquetas, idioma, foco y mensajes de error), complementada con una auditoría automática Lighthouse sobre Chromium.

### 3.3. Criterios de aceptación

Un caso se considera aprobado cuando:

- **Funcional:** la acción produce el resultado esperado sin errores; la respuesta es correcta en formato y contenido; las acciones críticas generan registro de auditoría.
- **No funcional (rendimiento):** el promedio de cinco mediciones de los endpoints CRUD debe ser inferior a 300 ms bajo carga normal y la página principal debe cargar en menos de 2 s (NFR-PERF-1/2). Se informa promedio, mínimo y máximo, no una medición única.
- **No funcional (usabilidad):** la pantalla evaluada debe obtener una puntuación Lighthouse de accesibilidad ≥ 0,90 y no presentar barreras que impidan completar el inicio de sesión; cada criterio no conforme se registra como observación con su severidad (CP-014).
- **Seguridad:** ningún endpoint devuelve datos sensibles sin token válido; la subida de documentos solo acepta los formatos permitidos por RF-5.2 (PDF, DOC, PPT, JPG y PNG) y rechaza cualquier otro tipo o contenido; el login resiste inyección SQL; no existen vulnerabilidades críticas detectadas (OWASP A01, A02, A07, A08).
- **Cumplimiento:** sin credenciales en texto claro ni en código fuente; mensajes de error sin datos internos del motor; datos personales protegidos por control de acceso.
- **Reglas de negocio:** RB-2 (solo usuarios vinculados ven datos de la empresa), RB-3 (un contrato por cliente), RB-4 (editor solo lectura) y RB-5 (administrador con control completo).

**Criterio de certificación (transversal):** 100 % de los casos de seguridad críticos exitosos y ningún defecto de severidad crítica abierto. Un software con defectos críticos abiertos nunca debe ser certificado.

### 3.4. Herramientas utilizadas

| Herramienta | Uso en la ejecución | Justificación |
|---|---|---|
| Docker Compose | Despliegue del entorno completo (frontend, backend, PostgreSQL) | Reproduce el ambiente de forma aislada y verificable (Anexo D) |
| curl | Ejecución manual de pruebas sobre la API REST | Permite controlar token, cabeceras y payloads, y registrar código HTTP como evidencia |
| ESLint 9 | Análisis estático de calidad de código | Detecta errores y malas prácticas en frontend y backend de forma automática |
| SonarQube 10.6 + SonarScanner | Análisis estático de seguridad y calidad | Métricas objetivas de bugs, vulnerabilidades, code smells, hotspots y duplicación (Anexo E) |
| Revisión manual de código | Auditoría de seguridad del código fuente | Identifica hallazgos que las herramientas no cubren (control de acceso, secretos, manejo de archivos) |
| Swagger UI (`/docs/`) | Validación de la interfaz de la API | Verifica contratos, parámetros y respuestas de los endpoints |
| Navegador (Edge/Chromium) | Captura de evidencias SonarQube y revisión de interfaz | Evidencia visual legible de los resultados del análisis |

**Recursos humanos:** un líder de QA, un tester funcional y un tester de seguridad; colaboración con el equipo de desarrollo para la corrección de defectos.

**Recursos técnicos:** equipos con Node.js, npm, Docker, Git y navegadores modernos; entorno de pruebas local aislado de producción.

**Entorno de prueba:** ambiente QA local (Docker) con datos ficticios de clientes, contratos y usuarios; no se utilizaron datos reales de personas (Anexo D).

### 3.5. Cronograma de ejecución

El plan se ejecutó entre el 19 y el 29 de octubre de 2026. Cada actividad tiene responsable y entregable verificable; las fechas de ejecución de cada caso se detallan en la sección 5.2.

| N.º | Actividad | Inicio | Fin | Responsable | Entregable |
|---|---|---|---|---|---|
| 1 | Lectura del ERS, definición de alcance y criterios de aceptación | 19-10-2026 | 20-10-2026 | Luis Tasso | Secciones 1 y 2 |
| 2 | Diseño de casos de prueba y matriz de trazabilidad | 20-10-2026 | 22-10-2026 | Miguel Arredondo | CP-001 a CP-014 y sección 4.2 |
| 3 | Preparación del entorno Docker (frontend, API, PostgreSQL) | 22-10-2026 | 23-10-2026 | Nicolas Iturrieta | Anexo D |
| 4 | Ciclo 1: smoke test de funciones base | 23-10-2026 | 23-10-2026 | Miguel Arredondo | CP-001 a CP-004 |
| 5 | Ciclo 2: pruebas funcionales y de seguridad | 26-10-2026 | 28-10-2026 | Luis Tasso | CP-005 a CP-012 y SEG-01 a SEG-13 |
| 6 | Pruebas no funcionales: rendimiento y usabilidad | 27-10-2026 | 28-10-2026 | Nicolas Iturrieta | CP-013 y CP-014 |
| 7 | Análisis estático (ESLint y SonarQube) y revisión manual | 27-10-2026 | 28-10-2026 | Miguel Arredondo | Anexos C y E |
| 8 | Consolidación de evidencias, análisis y dictamen | 28-10-2026 | 29-10-2026 | Luis Tasso | Secciones 5 a 7 |

**Hitos de control:** al cierre del hito 4 se verificó que el sistema levantara y autenticara correctamente, condición para continuar; al cierre del hito 6 se congelaron las mediciones; al cierre del hito 8 se emitió el dictamen. Los desvíos se registraron como incidentes en la sección 5.3.

---

## 4. Diseño de casos de prueba

### 4.1. Fichas de casos representativos

Se diseñaron y ejecutaron **14 casos de prueba** (CP-001 a CP-014): 12 funcionales y de seguridad, y 2 no funcionales (rendimiento y usabilidad). La cobertura se declara por requisito en la sección 4.2 y **no se afirma cobertura total del ERS**. A continuación se detallan las fichas de los casos representativos en el formato exigido: ID, nombre, requerimiento asociado, descripción, precondiciones, pasos, resultado esperado, criterio de aceptación, datos de prueba, fecha, ejecutor y tipo de prueba.

> **Trazabilidad de la versión anterior:** el caso antes identificado como FN-02 (una sola medición de rendimiento) se renumera como **CP-013**, se amplía a cinco mediciones y se contabiliza como caso **FALLÓ** en el resumen de ejecución.

**CP-001 · Login con credenciales válidas**

| Campo | Detalle |
|---|---|
| **ID** | CP-001 |
| **Nombre** | Inicio de sesión y obtención de token |
| **Requerimiento** | RF-1 / RF-1.1 (El sistema debe permitir autenticarse con nombre_usuario y contraseña) |
| **Tipo de prueba** | Funcional / Seguridad |
| **Fecha de ejecución** | 28-10-2026 |
| **Ejecutor** | Miguel Arredondo |
| **Descripción** | Verificar que un usuario registrado obtiene un token de sesión y que credenciales inválidas son rechazadas |
| **Precondiciones** | Usuario `admin/admin` existente en la base de datos; backend desplegado |
| **Pasos** | 1. Enviar `POST /autenticacion/login` con credenciales válidas. 2. Verificar código 200 y presencia de `token`. 3. Repetir con contraseña incorrecta y verificar 401. |
| **Datos de prueba** | `{"nombre_usuario": "admin", "password": "admin"}` y variante con password incorrecta |
| **Resultado esperado** | Válidas: HTTP 200 + token JWT. Inválidas: HTTP 401 "Credenciales inválidas" sin enumerar usuarios |
| **Criterio de aceptación** | Login exitoso genera token; credenciales incorrectas son rechazadas sin información adicional (RF-1) |

**CP-005 · Listar clientes con token válido**

| Campo | Detalle |
|---|---|
| **ID** | CP-005 |
| **Nombre** | Listado de clientes de la empresa autenticada |
| **Requerimiento** | RF-4 / RB-2 (El usuario autenticado debe listar los clientes de su empresa) |
| **Tipo de prueba** | Funcional / Integración |
| **Fecha de ejecución** | 28-10-2026 |
| **Ejecutor** | Miguel Arredondo |
| **Descripción** | Verificar que el endpoint retorna los clientes de la empresa asociada al token |
| **Precondiciones** | Token JWT válido de usuario con empresa asociada; datos semilla cargados |
| **Pasos** | 1. Obtener token en `POST /autenticacion/login`. 2. Enviar `GET /clientes` con cabecera `Authorization: Bearer <token>`. 3. Verificar código 200 y contenido. |
| **Datos de prueba** | Token de `admin`; dataset semilla (2 clientes) + 1 cliente creado en CP-006 |
| **Resultado esperado** | HTTP 200 con la lista de clientes de la empresa |
| **Criterio de aceptación** | Solo se retornan los clientes de la empresa del usuario autenticado (RB-2); respuesta en formato JSON |

**CP-010 · Subida de archivo no permitido a contrato**

| Campo | Detalle |
|---|---|
| **ID** | CP-010 |
| **Nombre** | Adjuntar documento a contrato con archivo `.exe` y `.html` |
| **Requerimiento** | RF-5.2 (El sistema admite documentos PDF, DOC, PPT, JPG y PNG) / NFR-SEG-4 |
| **Tipo de prueba** | Seguridad |
| **Fecha de ejecución** | 28-10-2026 |
| **Ejecutor** | Luis Tasso |
| **Descripción** | Verificar que la subida de documentos acepta únicamente los formatos definidos en RF-5.2 (PDF, DOC, PPT, JPG, PNG) y rechaza ejecutables y contenido activo |
| **Precondiciones** | Token válido; cliente y contrato existentes; archivos de prueba disponibles |
| **Pasos** | 1. Con token, enviar `POST /contratos` con `file=evidencia.exe`. 2. Repetir con `evidencia.html`. 3. Descargar el archivo adjunto con `GET /contratos/:id/file`. 4. Comparar el tipo declarado con el contenido real. |
| **Datos de prueba** | `evidencia.exe` (cabecera `MZ`, MIME `application/octet-stream`) y `evidencia.html` (MIME `text/html`) |
| **Resultado esperado** | Rechazo (400/415) de `.exe` y `.html`; aceptación de PDF, DOC, PPT, JPG y PNG |
| **Criterio de aceptación** | Solo se almacenan los cinco formatos de RF-5.2, validando extensión y tipo MIME real; cualquier otro tipo se rechaza y queda registro de auditoría |
| **Resultado obtenido** | **Fallo (FAIL):** HTTP 201, el `.exe` y el `.html` fueron aceptados y almacenados; el `.exe` se sirve como `application/pdf` — defecto CRITICO (BUG-003) |

> **Observación de consistencia:** la interfaz también contradice el ERS. `ContratosTabCreate.jsx:147` indica "PDF, DOC, DOCX, XLS o XLSX" (incluye formatos no previstos y omite PPT, JPG y PNG), mientras `ContratoForm.jsx:221` indica "solo PDF". El backend, en cambio, no aplica ningún filtro (`multer` sin `fileFilter`).

**CP-011 · Acceso a contrato sin token (IDOR)**

| Campo | Detalle |
|---|---|
| **ID** | CP-011 |
| **Nombre** | Acceso a datos de contrato sin autenticación |
| **Requerimiento** | NFR-SEG-4 / NFR-SEG-9 / RB-2 (Los datos de contratos no deben ser accesibles sin autenticación) |
| **Tipo de prueba** | Seguridad |
| **Fecha de ejecución** | 28-10-2026 |
| **Ejecutor** | Luis Tasso |
| **Descripción** | Verificar que los endpoints de lectura exigen token válido |
| **Precondiciones** | Contrato existente (ID 1); sin token de sesión |
| **Pasos** | 1. Enviar `GET /contratos/1` sin cabecera `Authorization`. 2. Repetir para `GET /usuarios/1`, `GET /auditoria`, `GET /roles`. 3. Comparar con el resultado esperado 401. |
| **Datos de prueba** | Peticiones HTTP GET sin cabecera de autenticación |
| **Resultado esperado** | HTTP 401 en todos los endpoints consultados |
| **Criterio de aceptación** | Ningún endpoint que expone datos responde sin token válido (OWASP A01) |
| **Resultado obtenido** | **Fallo (FAIL):** HTTP 200 con datos completos del contrato, usuarios y auditoría sin autenticación — defecto CRITICO (BUG-001) |

**CP-012 · Intento de inyección SQL en login**

| Campo | Detalle |
|---|---|
| **ID** | CP-012 |
| **Nombre** | Login resistente a inyección SQL |
| **Requerimiento** | NFR-SEG-2 / NFR-SEG-4 (Validación de entradas e integridad de la información) |
| **Tipo de prueba** | Seguridad |
| **Fecha de ejecución** | 28-10-2026 |
| **Ejecutor** | Luis Tasso |
| **Descripción** | Verificar que el backend no es vulnerable a inyección SQL en el endpoint de login |
| **Precondiciones** | Backend desplegado; endpoint `POST /autenticacion/login` disponible |
| **Pasos** | 1. Enviar login con payload `admin' OR '1'='1` en el campo usuario. 2. Verificar código de respuesta. 3. Verificar que no se emite token. |
| **Datos de prueba** | `{"nombre_usuario": "admin' OR '1'='1", "password": "x"}` |
| **Resultado esperado** | HTTP 401, sin token emitido |
| **Criterio de aceptación** | La consulta parametrizada rechaza el payload y no entrega sesión (OWASP A03) |
| **Resultado obtenido** | **Aprobado (PASS):** HTTP 401; todas las consultas del backend usan parámetros `$1..$n` (node-postgres) |

**CP-013 · Rendimiento del listado de clientes (5 mediciones)**

| Campo | Detalle |
|---|---|
| **ID** | CP-013 |
| **Nombre** | Tiempo de respuesta de `GET /clientes` con token válido |
| **Requerimiento** | NFR-PERF-1 (respuesta CRUD < 300 ms bajo carga normal); NFR-PERF-2 como referencia |
| **Tipo de prueba** | No funcional (Rendimiento) |
| **Fecha de ejecución** | 28-10-2026 |
| **Ejecutor** | Nicolas Iturrieta |
| **Descripción** | Medir cinco veces consecutivas el tiempo total de respuesta del endpoint `GET /clientes` y comparar el promedio con el umbral de 300 ms |
| **Precondiciones** | Sistema desplegado en Docker; token válido; red local sin carga concurrente; dataset semilla cargado |
| **Pasos** | 1. Obtener token con `POST /autenticacion/login`. 2. Ejecutar cinco veces `curl -w "%{time_total}" GET /clientes` con el token. 3. Calcular promedio, mínimo y máximo. 4. Comparar con el umbral de NFR-PERF-1. |
| **Datos de prueba** | 5 mediciones sobre el mismo dataset (clientes semilla + creados en CP-006) |
| **Resultado esperado** | Promedio inferior a 0,300 s y dispersión menor al 10 % entre mediciones |
| **Criterio de aceptación** | Se cumple NFR-PERF-1 si el promedio de las cinco mediciones es < 300 ms |
| **Resultado obtenido** | **Fallo (FAIL):** promedio 4,011 s (mín. 4,010 s; máx. 4,013 s), 13,4 veces el umbral — BUG-010 |

**Mediciones registradas:**

| Medición | Tiempo (s) | Código HTTP |
|---|---|---|
| 1 | 4,010 | 200 |
| 2 | 4,013 | 200 |
| 3 | 4,010 | 200 |
| 4 | 4,011 | 200 |
| 5 | 4,011 | 200 |
| **Promedio** | **4,011** | 200 |

> La causa es una latencia artificial de 4 s (`delay(4000)`) insertada en `auth.js:17`, `clients.js:131`, `contracts.js:75` y `metricas.js:39`. Es un defecto del código entregado, no una limitación del hardware: por eso se clasifica como **FALLÓ** y se cuenta en el resumen.

**CP-014 · Usabilidad y accesibilidad de la pantalla de inicio de sesión**

| Campo | Detalle |
|---|---|
| **ID** | CP-014 |
| **Nombre** | Revisión de usabilidad y accesibilidad del login |
| **Requerimiento** | NFR-USAB (usabilidad y accesibilidad, incluida la atención a adultos mayores); NFR-COMPAT (parcial) |
| **Tipo de prueba** | No funcional (Usabilidad / Accesibilidad) |
| **Fecha de ejecución** | 28-10-2026 |
| **Ejecutor** | Nicolas Iturrieta |
| **Descripción** | Evaluar la pantalla de inicio de sesión con una lista de verificación de seis criterios y una auditoría automática Lighthouse |
| **Precondiciones** | Frontend desplegado en `http://localhost:3350`; navegador Chromium en ventana de 1000 × 700 px |
| **Pasos** | 1. Abrir `/login`. 2. Revisar tipografía, contraste, etiquetas, idioma y desbordamiento horizontal. 3. Inspeccionar los mensajes de error del formulario. 4. Ejecutar Lighthouse (categoría Accessibility). |
| **Datos de prueba** | Pantalla `/login`; Lighthouse 12 sobre Chromium; resolución 1000 × 700 |
| **Resultado esperado** | Lighthouse ≥ 0,90 y ningún bloqueo crítico de uso; cada criterio no conforme queda como observación |
| **Criterio de aceptación** | Se aprueba si la puntuación de accesibilidad es ≥ 0,90 y no hay barreras que impidan completar el inicio de sesión |
| **Resultado obtenido** | **Aprobado con observaciones:** Lighthouse 0,96; 3 de 6 criterios conformes, 1 parcial y 2 no conformes — BUG-012 (MODERADO) |

| N.º | Criterio | Resultado | Evidencia |
|---|---|---|---|
| 1 | Tipografía ≥ 12 px | Cumple | Cuerpo 14 px; título 31,5 px |
| 2 | Contraste AA (4,5:1; 3:1 en texto grande) | **No cumple** | Botón "Entrar": blanco sobre `#4BBC7F` = 2,39:1 (Lighthouse `color-contrast`) |
| 3 | Etiquetas asociadas a los campos | Cumple | `<label for="nombre_usuario">` y `<label for="password">` |
| 4 | Idioma de la página declarado | **No cumple** | `<html lang="en">` con contenido en español (WCAG 3.1.1) |
| 5 | Mensajes de error claros | Parcial | Credenciales inválidas muestra toast genérico; campos vacíos no muestran mensaje (no se usa `formState.errors`) |
| 6 | Sin desbordamiento horizontal | Cumple | `scrollWidth = innerWidth` en 1000 × 700 |

> **Foco visible:** los campos y el botón definen `outline: none`; el recorrido con `Tab` no pudo automatizarse en el entorno de revisión, por lo que se marca para verificación manual y no se computa en el resultado. Lighthouse: Accesibilidad 0,96 · Buenas prácticas 1,00 · SEO 0,67.

### 4.2. Matriz de trazabilidad de requisitos

La matriz usa los identificadores del ERS citados en el EP1 y en la retroalimentación (`RF-1.1`, `RF-4`, `RF-5.2`, `RF-6.1`, `NFR-PERF-1`, `NFR-SEG-4`, `RB-2`, etc.). Se eliminaron los identificadores internos `RQ-01…RQ-12` de la versión anterior.

**Alcance de la trazabilidad.** El ERS completo no forma parte del repositorio entregado; por lo tanto, la matriz se limita a los 21 requisitos identificables a partir del EP1, del código y de las guías del curso. No se declara cobertura total: se informa qué requisitos están cubiertos, cuáles parcialmente y cuáles no fueron verificados en este ciclo.

| ID ERS | Requerimiento | Caso(s) de prueba | Resultado | Cobertura | Defecto |
|---|---|---|---|---|---|
| RF-1.1 | Autenticación con nombre de usuario y contraseña | CP-001, CP-002 | Pass | Cubierto | — |
| RF-1 | Emisión y vigencia del token de sesión | CP-001 | Pass | Cubierto | — |
| RF-3.2 / RB-4 | El rol editor solo permite lectura | — | — | No cubierto | — |
| RF-4 | Gestión de clientes: listar, crear y buscar | CP-005, CP-006, CP-007 | Pass | Cubierto | — |
| RF-5 | Gestión de contratos: listar, crear y adjuntar documentos | CP-008, CP-010 | Fail | Parcial | BUG-003 |
| RF-5.2 | Documentos permitidos: PDF, DOC, PPT, JPG y PNG | CP-010, SEG-07b | Fail | Parcial | BUG-003 |
| RF-6 / RF-6.1 | Registro en auditoría de acciones críticas | CP-006, CP-010, SEG-03 | Parcial | Parcial | BUG-001 |
| NFR-PERF-1 | Respuesta de operaciones CRUD < 300 ms | CP-013 | **Fail** | Cubierto | BUG-010 |
| NFR-PERF-2 | Carga de la página principal < 2 s | — | — | No cubierto | — |
| NFR-PERF-3 | Soporte de 200 usuarios concurrentes | — | — | No cubierto | — |
| NFR-SEG-2 | Hash de contraseñas y validación de entradas | CP-012 + revisión manual | Parcial | Parcial | BUG-002 |
| NFR-SEG-4 | Autenticación y control de acceso en todos los endpoints | CP-011, SEG-01 a SEG-04 | **Fail** | Cubierto | BUG-001 |
| NFR-SEG-6 | Registro de actividad y protección de logs | SEG-03 | Fail | Parcial | BUG-001 |
| NFR-SEG-7 | Respaldos y recuperación | — | — | No cubierto | — |
| NFR-SEG-9 | Sesión JWT de corta vigencia y cierre seguro | CP-001, SEG-13 | Parcial | Parcial | BUG-006 |
| NFR-USAB | Usabilidad y accesibilidad (incluye adultos mayores) | CP-014 | Pass con observaciones | Cubierto | BUG-012 |
| NFR-DIS-1 | Disponibilidad mensual de 99,5 % | — | — | No cubierto | — |
| NFR-COMPAT | Compatibilidad desktop, tablet y móvil | CP-014 (solo desktop) | Parcial | Parcial | — |
| RB-2 | Aislamiento de datos por empresa | CP-005, CP-011 | Parcial | Parcial | BUG-001 |
| RB-3 | Un contrato por cliente | — | — | No cubierto | — |
| RB-5 | El administrador tiene control completo | CP-005 a CP-009 | Pass | Parcial | — |

**Cobertura real:** 6 de 21 requisitos cubiertos (28,6 %), 9 parcialmente cubiertos (42,9 %) y 6 no cubiertos (28,6 %). Los casos CP-010, CP-011 y CP-013 fallaron; por lo tanto, la cobertura plena no implica conformidad: un requisito puede estar cubierto y aun así incumplirse.

**Requisitos no verificados y su justificación:** RF-3.2/RB-4 y RB-3 requieren datos y roles adicionales (usuario editor y un segundo contrato por cliente); NFR-PERF-2 y NFR-PERF-3 requieren instrumentación de carga y un generador de usuarios concurrentes; NFR-SEG-7 y NFR-DIS-1 requieren observación prolongada del entorno. Se registran como trabajo pendiente para el próximo ciclo, no como conformidades presuntas.

---

## 5. Ejecución de pruebas

### 5.1. Resumen de ejecución

| Métrica | Valor |
|---|---|
| Total de casos de prueba diseñados | 14 |
| Casos ejecutados | 14 (100 %) |
| Casos aprobados (Pass) | 11 (78,6 %) |
| Casos fallidos (Fail) | 3 (21,4 %): CP-010, CP-011 y CP-013 |
| Casos bloqueados | 0 |
| Pruebas de seguridad complementarias (SEG) | 10 (7 inseguras / 3 conformes) |
| Incidentes registrados | 12 (4 CRITICO · 6 GRAVE · 1 MODERADO · 1 LEVE) |
| Problemas análisis estático (ESLint) | 14 (frontend 11 + backend 3) |
| Resultados análisis estático (SonarQube) | 1 vulnerabilidad BLOCKER · 4 security hotspots · 198 code smells · 1 bug |
| Tiempo promedio de respuesta con token válido | 4,011 s (promedio de 5 mediciones) |

Los tres casos fallidos son CP-010 y CP-011 (defectos de seguridad CRITICO) y CP-013 (rendimiento: 4,011 s frente a un umbral de 300 ms). Los dos casos no funcionales —CP-013 y CP-014— se contabilizan en el resumen: CP-013 como **FALLÓ** y CP-014 como **aprobado con observaciones**. No se aplica ningún "riesgo aceptado": un incumplimiento medido se informa como incumplimiento.

### 5.2. Detalle de ejecución de casos

Cada fila registra la fecha y el ejecutor responsables. La columna "Evidencia" remite al Anexo F, donde se transcribe la petición `curl` y la respuesta HTTP real del servidor.

| CASO | DESCRIPCIÓN | FECHA | EJECUTOR | RESULTADO | EVIDENCIA | TIPO DE PRUEBA |
|---|---|---|---|---|---|---|
| CP-001 | Login con credenciales válidas | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 200 + JWT de 233 caracteres — Anexo F | Funcional |
| CP-002 | Login con contraseña incorrecta | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 401 "Credenciales inválidas", sin enumeración — Anexo F | Funcional / Seguridad |
| CP-003 | Estado/salud de la API | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 200 `{"name":"Atlas","status":"ok"}` — Anexo F | Funcional / Integración |
| CP-004 | Documentación Swagger `/docs/` | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 200, interfaz interactiva — Anexo F | Funcional / Integración |
| CP-005 | Listar clientes (token) | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 200; 4 clientes en la captura — Anexo F | Funcional |
| CP-006 | Crear cliente | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 201; cliente ID 5 "Cliente Evidencia …" — Anexo F | Funcional |
| CP-007 | Buscar cliente por nombre | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 200; el cliente creado aparece en la búsqueda — Anexo F | Funcional |
| CP-008 | Listar contratos (token) | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 200; 8 contratos en la captura — Anexo F | Funcional |
| CP-009 | Dashboard / métricas (token) | 28-10-2026 | Miguel Arredondo | Aprobado | HTTP 200; 2 usuarios, 5 clientes — Anexo F | Funcional |
| CP-010 | Subir documento a contrato (`.exe` y `.html`) | 28-10-2026 | Luis Tasso | **Falló** | HTTP 201: ejecutable y HTML aceptados; el `.exe` se sirve como `application/pdf` (BUG-003) — Anexo F | Seguridad |
| CP-011 | Acceso a contrato sin token (`GET /contratos/1`) | 28-10-2026 | Luis Tasso | **Falló** | HTTP 200 con datos del contrato sin autenticación (BUG-001) — Anexo F | Seguridad |
| CP-012 | Login con intento SQLi (`admin' OR '1'='1`) | 28-10-2026 | Luis Tasso | Aprobado | HTTP 401; consulta parametrizada lo bloquea — Anexo F | Seguridad |
| CP-013 | Rendimiento de `GET /clientes` (5 mediciones) | 28-10-2026 | Nicolas Iturrieta | **Falló** | Promedio 4,011 s vs. umbral 0,300 s (BUG-010) — Anexo F | No funcional (Rendimiento) |
| CP-014 | Usabilidad y accesibilidad del login | 28-10-2026 | Nicolas Iturrieta | Aprobado con observaciones | Lighthouse 0,96; contraste 2,39:1 y `lang="en"` (BUG-012) — Anexo F | No funcional (Usabilidad) |
| SEG-01 a SEG-13 (10 pruebas) | Pruebas complementarias de seguridad (acceso sin token, upload, SQLi, CORS, fuerza bruta) | 28-10-2026 | Luis Tasso | 7 inseguras / 3 conformes | Petición y respuesta de cada prueba en el Anexo F; síntesis en el Anexo B | Seguridad |

### 5.3. Criticidad de incidentes

**Escala de medición de impacto:**

| NIVEL | DESCRIPCIÓN | IMPACTO | EVIDENCIA REQUERIDA | REMEDIACIÓN |
|---|---|---|---|---|
| CRITICO | El defecto impide completamente el funcionamiento o expone datos sensibles; vulnera seguridad o una funcionalidad esencial del negocio | Muy alto: el sistema no puede usarse en producción ni certificarse | Reproducción con evidencia (código HTTP, captura, log o hallazgo estático) | Requiere remedación inmediata |
| GRAVE | El defecto afecta funcionalidades importantes, pero el sistema aún funciona parcialmente; existe workaround | Alto: afecta áreas principales del usuario o la superficie de ataque | Registro de prueba y referencia al código afectado | Debe corregirse con urgencia |
| MODERADO | Afecta funcionalidades secundarias o casos específicos sin detener el flujo principal | Medio: el usuario puede trabajar con molestias o limitaciones | Registro de prueba con métrica o comparación | Se corrige en próxima iteración |
| LEVE | Defecto de apariencia, estética o código sin impacto funcional directo | Bajo: no impacta la operación | Hallazgo de análisis estático o revisión | Se corrige según disponibilidad |

**Incidentes identificados:**

| CASO / ID | DESCRIPCIÓN | RESULTADO | IMPACTO |
|---|---|---|---|
| BUG-001 | Endpoints accesibles sin token (IDOR): `GET /contratos/:id`, `/usuarios/:id`, `/auditoria`, `/roles`, `/empresa-usuarios/:id` | Datos y logs expuestos sin autenticación (CP-011, SEG-01/02/03/04) | CRITICO |
| BUG-002 | Credenciales en texto claro y débiles por defecto (`admin/admin`, `editor/editor`); comparación directa sin hash (`auth.js:26`) | Autenticación comprometible; incumple NFR-SEG-2 y Ley 19.628 | CRITICO |
| BUG-003 | Subida de archivos sin validación de tipo/MIME (multer sin filtro); `.exe` aceptado y servido como PDF | Superficie de ataque para malware (CP-010, SEG-07b, SEG-01) | CRITICO |
| BUG-011 | Credenciales de PostgreSQL en código (`db.js:6`), detectada como vulnerabilidad BLOCKER `secrets:S6698` por SonarQube | Secretos comprometidos en el repositorio; confirma BUG-002/BUG-004 | CRITICO |
| BUG-004 | `JWT_SECRET` con valor de respaldo `"inseguro"` (`auth.js:7`, replicado en 7 routers) | Tokens falsificables (revisión manual, `auth.js:7`) | GRAVE |
| BUG-005 | CORS con `Access-Control-Allow-Origin: *` global (`app.js:22`) | Amplía superficie de ataque CSRF (SEG-12, hotspot SonarQube) | GRAVE |
| BUG-006 | Ausencia de rate-limit / bloqueo por fuerza bruta en login | Ataque de fuerza bruta viable (SEG-13) | GRAVE |
| BUG-007 | Errores 500 exponen detalle interno del motor (`glosa`); creaciones no transaccionales | Fuga de información y datos huérfanos (SEG-07b) | GRAVE |
| BUG-008 | Token JWT y datos de usuario en `localStorage` (`AuthContext.jsx:8-16`) | Robo de sesión ante XSS | GRAVE |
| BUG-010 | Latencia artificial de 4 s (`delay(4000)`) en login, clientes, contratos y métricas | Incumple NFR-PERF-1: promedio 4,011 s vs. umbral 300 ms (CP-013) | GRAVE |
| BUG-012 | Contraste insuficiente del botón "Entrar" (2,39:1) y `lang="en"` en página en español; campos sin mensaje de validación visible | Barreras de accesibilidad para usuarios con baja visión y lectores de pantalla (CP-014) | MODERADO |
| BUG-009 | Code smells ESLint: 11 frontend (no-unused-vars, exhaustive-deps) y 3 backend | Deuda técnica sin impacto funcional | LEVE |

> Un software con defectos CRITICO abiertos nunca debe ser certificado. Al cierre del ciclo permanecen 4 incidentes CRITICO y 6 GRAVE abiertos.

---

## 6. Análisis ético y normativo de los resultados

### 6.1. Consideraciones éticas

- **Transparencia del reporte:** todos los hallazgos se documentan con evidencia reproducible (códigos HTTP, comandos, capturas de pantalla y referencias de código), sin ocultar ni minimizar los defectos detectados, sustentando un veredicto honesto ante el docente y la comunidad académica.
- **Uso responsable del entorno:** las pruebas de penetración se ejecutaron exclusivamente sobre el entorno de laboratorio Docker con datos ficticios; no se realizó exploración contra sistemas de terceros ni se usaron datos reales de personas.
- **Confidencialidad:** las credenciales y vulnerabilidades identificadas se reportan en este informe de uso académico y no se difunden fuera del ámbito de la asignatura, conforme a principios de divulgación responsable.
- **Integridad profesional:** no se modificó el código fuente del caso para ocultar hallazgos; la corrección queda como recomendación, preservando la objetividad de la auditoría.

### 6.2. Consideraciones normativas

- **Protección de datos personales (Ley 19.628 y Ley 21.719):** el almacenamiento de credenciales en texto claro (BUG-002) y la exposición de datos de clientes, usuarios y auditoría sin autenticación (BUG-001) implican una afectación directa a los principios de seguridad y confidencialidad en el tratamiento de datos personales, incluidos datos bancarios de clientes.
- **ISO/IEC 27001:** los controles A.9.4 (control de acceso), A.10 (criptografía) y A.12.4 (registro de actividad) se encuentran parcial o totalmente incumplidos: el control de acceso está delegado al frontend, no existe hash de contraseñas y los logs de auditoría son legibles sin token.
- **OWASP Top 10:** los hallazgos se mapean a A01 (Broken Access Control: BUG-001, BUG-003, BUG-005), A02 (Cryptographic Failures: BUG-002, BUG-004, BUG-011), A07 (Identification and Authentication Failures: BUG-006) y A08 (Software and Data Integrity Failures: BUG-003).
- **Responsabilidad del desarrollo:** conforme a criterios éticos de la profesión, los defectos detectados deben ser corregidos y re-verificados antes de cualquier despliegue real que afecte a usuarios.

### 6.3. Dictamen y acciones correctivas

**Criterio de aceptación para certificar:** 100 % de los casos de seguridad críticos exitosos y ningún defecto de severidad crítica abierto.

**Resultado:** NO se cumplió el criterio. De 14 casos ejecutados, 11 aprobaron y 3 fallaron: CP-010 y CP-011 (seguridad, CRITICO) y CP-013 (rendimiento sobre el umbral). Permanecen abiertos 4 incidentes CRITICO (BUG-001, BUG-002, BUG-003, BUG-011) y 6 GRAVE. SonarQube confirma 1 vulnerabilidad BLOCKER y Security Rating E en el backend. La cobertura plena de requisitos es 28,6 % (6 de 21), por lo que tampoco puede sostenerse un dictamen favorable por cobertura.

**Dictamen final: NO CERTIFICADO** — el software no es apto para producción y requiere un ciclo de corrección antes de una nueva certificación.

**Acciones correctivas recomendadas:**

1. Middleware de autenticación global (JWT) en todos los endpoints que leen o modifican datos (BUG-001).
2. Hash seguro de contraseñas (bcrypt/argon2) y eliminación de credenciales por defecto con cambio obligatorio en primer acceso (BUG-002).
3. Validación de extensión, tipo MIME y contenido real en la subida de archivos, limitando a los cinco formatos de RF-5.2 (PDF, DOC, PPT, JPG y PNG) (BUG-003).
4. `JWT_SECRET` y credenciales de base de datos fuera del código, en variables de entorno obligatorias (BUG-004, BUG-011).
5. Restricción de CORS a los orígenes autorizados (BUG-005).
6. Rate-limit en `/autenticacion/login` (BUG-006).
7. Envolver creaciones en transacciones y ocultar detalles internos del motor en errores 500 (BUG-007).
8. Corregir code smells ESLint y añadir hook de lint en CI (BUG-009).
9. Reemplazar `localStorage` por cookies `httpOnly` para la sesión (BUG-008).
10. Quality Gate de SonarQube en CI con condiciones de seguridad: 0 vulnerabilidades BLOCKER/CRITICAL, Security Rating A y deuda < 5 %.
11. Eliminar la latencia artificial `delay(4000)` y volver a medir CP-013 con cinco repeticiones antes de certificar (BUG-010).
12. Corregir contraste del botón a ≥ 4,5:1, declarar `lang="es"` y mostrar mensajes de validación en los campos (BUG-012).

---

## 7. Anexos y evidencias

### Anexo A · Bitácora de ejecución (actividad 2.3.2)

Las tablas de este anexo son una **síntesis** de la ejecución. La petición `curl` y la respuesta HTTP completa de cada caso están transcritas en el Anexo F; no se registra ningún resultado sin evidencia.

**Ciclo 1 · Smoke Test** (objetivo: verificar funciones base; si falla, se detiene la ejecución)

| ID | Nombre | Fecha | Ejecutor | Estado | Defecto | Observaciones |
|---|---|---|---|---|---|---|
| CP-001 | Login con credenciales válidas (admin/admin) | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 200, JWT de 233 caracteres |
| CP-002 | Login con contraseña incorrecta | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 401 "Credenciales inválidas". No enumera usuarios |
| CP-003 | Estado/salud de la API | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 200 `{"name":"Atlas","status":"ok"}` |
| CP-004 | Documentación Swagger `/docs/` | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 200 (interfaz interactiva) |

**Ciclo 2 · Ejecución de casos de prueba**

| ID | Nombre | Fecha | Ejecutor | Estado | Defecto | Observaciones |
|---|---|---|---|---|---|---|
| CP-005 | Listar clientes (token) | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 200; 4 clientes en la captura |
| CP-006 | Crear cliente | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 201; cliente ID 5 "Cliente Evidencia …" |
| CP-007 | Buscar cliente por nombre | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 200; el cliente creado aparece en la búsqueda |
| CP-008 | Listar contratos (token) | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 200; 8 contratos en la captura |
| CP-009 | Dashboard / métricas (token) | 28-10-2026 | Miguel Arredondo | Aprueba | N/A | HTTP 200; 2 usuarios, 5 clientes |
| CP-010 | Subir documento a contrato (`.exe` y `.html`) | 28-10-2026 | Luis Tasso | Falló | BUG-003 | HTTP 201: se aceptaron ejecutable y HTML sin validación |
| CP-011 | Acceso a contrato SIN token (`GET /contratos/1`) | 28-10-2026 | Luis Tasso | Falló | BUG-001 | HTTP 200 devuelve datos del contrato sin autenticación |
| CP-012 | Login con intento SQLi (`admin' OR '1'='1`) | 28-10-2026 | Luis Tasso | Aprueba | N/A | HTTP 401; consulta parametrizada lo bloquea |
| CP-013 | Rendimiento de `GET /clientes` (5 mediciones) | 28-10-2026 | Nicolas Iturrieta | Falló | BUG-010 | Promedio 4,011 s vs. umbral 0,300 s |
| CP-014 | Usabilidad y accesibilidad del login | 28-10-2026 | Nicolas Iturrieta | Aprueba con observaciones | BUG-012 | Lighthouse 0,96; contraste 2,39:1 y `lang="en"` |

### Anexo B · Evidencias de seguridad (pruebas complementarias)

Igual que el Anexo A, esta tabla es una síntesis: la columna "Evidencia" indica el bloque del Anexo F donde se transcribe la petición y la respuesta real de cada prueba.

| ID Prueba | Prueba | Resultado esperado | Resultado obtenido | Severidad | Evidencia (Anexo F) |
|---|---|---|---|---|---|
| SEG-01 | `GET /contratos/1` y descarga de archivo sin token | 401 | **200 (contrato y archivo con contenido `.exe`)** | Crítica | SEG-01 |
| SEG-02 | `GET /usuarios/1` sin token | 401 | **200 (correo de usuario)** | Crítica | SEG-02 |
| SEG-03 | `GET /auditoria` sin token | 401 | **200 (logs internos)** | Crítica | SEG-03 |
| SEG-04 | `GET /roles` sin token | 401 | **200** | Mayor | SEG-04 |
| SEG-05 | Login con payload SQLi (`admin' OR '1'='1`) | 401 | 401 (consulta parametrizada) | Conforme | SEG-05 |
| SEG-06 | Login con contraseña incorrecta (sin enumeración) | 401 | 401 | Conforme | SEG-06 |
| SEG-07b | Subir archivo `.exe` y `.html` con token | Rechazo 400/415 | **201 (aceptado)** | Crítica | SEG-07b |
| SEG-10 | Acceso con token válido a recurso propio | 200 | 200 | Conforme | SEG-10 |
| SEG-12 | `Origin: http://evil.example.com` | Origen restringido | **`Access-Control-Allow-Origin: *`** | Mayor | SEG-12 |
| SEG-13 | 3 intentos de login fallidos seguidos | Bloqueo/rate-limit | Ningún bloqueo (solo 4 s de espera) | Mayor | SEG-13 |

**Total: 10 pruebas SEG — 7 inseguras (SEG-01, SEG-02, SEG-03, SEG-04, SEG-07b, SEG-12, SEG-13) y 3 conformes (SEG-05, SEG-06, SEG-10).**

> Las pruebas SEG-08b y SEG-11a se integran como evidencia dentro de SEG-07b y SEG-01, respectivamente. SEG-09 corresponde al hallazgo de `JWT_SECRET` detectado por revisión manual (BUG-004) y no se contabiliza como prueba dinámica independiente. CP-013 (rendimiento) y CP-014 (usabilidad) son casos no funcionales y se registran en el Anexo A, no como SEG.

### Anexo C · Análisis estático de código (ESLint 9)

**Frontend (11 issues en 7 archivos):**

| Archivo | Línea | Tipo | Regla |
|---|---|---|---|
| `pages/clientes/ClientesTabList.jsx` | 27 | Error | no-unused-vars (`onLoad`) |
| `pages/contratos/ContratosTabCreate.jsx` | 31 | Error | no-unused-vars (`error`) |
| `pages/contratos/ContratosTabList.jsx` | 32 / 244 | Error / Warning | no-unused-vars / react-hooks/exhaustive-deps |
| `pages/empresas/EmpresaForm.jsx` | 42 / 63 | Error | no-unused-vars (`error`) |
| `pages/empresas/EmpresasList.jsx` | 43 | Warning | Unused eslint-disable directive |
| `pages/usuarios/UsuarioForm.jsx` | 43 / 61 / 86 | Error | no-unused-vars (`error`) |
| `pages/usuarios/UsuariosTabList.jsx` | 28 | Warning | react-hooks/exhaustive-deps |

**Backend (3 issues):**

| Archivo | Línea | Tipo | Regla |
|---|---|---|---|
| `src/app.js` | 8 | Warning | no-unused-vars (`pool` importado sin uso) |
| `src/routes/contracts.js` | 1–2 | Warning | no-unused-vars (`path`, `fs`) |

**Hallazgos manuales de seguridad (código fuente):**

| Ubicación | Hallazgo | Severidad |
|---|---|---|
| `auth.js:7` y 7 routers | `JWT_SECRET` default `"inseguro"` | Mayor |
| `auth.js:26` | Comparación de contraseña en texto claro (`user.contrasena_hash !== password`) | Crítica |
| `app.js:22` | `app.use(cors())` sin configurar → `*` | Mayor |
| `contracts.js:29` | `multer({ storage })` sin filtro de archivos; archivo guardado como bytea sin validar | Crítica |
| `contracts.js:275,413` | `GET /:id` y `GET /:id/file` sin validación de token | Crítica |
| `users.js:74-90,123` | `GET /:id` y `DELETE /:id` sin validación de token/empresa | Crítica |
| `audit.js:37-45`, `roles.js:39-59`, `empresa_usuarios.js:132-149` | Lecturas sin autenticación | Mayor |
| `AuthContext.jsx:8-16` | Token y user en `localStorage` | Mayor |
| `dump-atlas.sql:344-345` | Credenciales por defecto `admin/admin`, `editor/editor` | Crítica |
| `db.js:6` | Credenciales de BD en cadena de conexión por defecto del código | Mayor |
| Errores 500 | Campo `glosa` expone mensaje interno de PostgreSQL | Menor |

### Anexo D · Ambiente de prueba

| Componente | Tecnología | Endpoint |
|---|---|---|
| Frontend Atlas | React 19 + Vite + MUI (nginx) | http://localhost:3350 |
| API Atlas | Node 18 + Express 4.19 | http://localhost:4450 |
| Base de datos | PostgreSQL 17 | localhost:15432 (nombre: `atlas`) |
| Documentación API | Swagger UI (`/docs/`) | http://localhost:4450/docs/ |
| Método de ejecución | Docker Compose (`docker compose up -d --build`) | — |
| Fecha de ejecución | 28-10-2026 | — |
| Ejecutores | Luis Tasso (seguridad), Miguel Arredondo (funcional), Nicolas Iturrieta (no funcional) | — |

### Anexo E · Análisis estático con SonarQube (servidor local :9000)

Se desplegó un servidor **SonarQube 10.6 Community** en Docker (`sonarqube:10.6-community`, puerto 9000) y se ejecutó el análisis con **Sonar Scanner 3.1** (Node, sin JVM adicional) sobre el backend y el frontend de Atlas.

**Métricas de calidad:**

| Métrica | Backend (`atlas`) | Frontend (`atlas-frontend`) |
|---|---|---|
| Líneas de código (ncloc) | 1.523 | 5.432 |
| Bugs | 0 | 1 |
| Vulnerabilidades | **1** | 0 |
| Code Smells | 17 | 181 |
| Security Hotspots | 4 | 0 |
| Duplicación (%) | 37,0 | 11,1 |
| Cobertura | 0 % (sin tests) | 0 % |
| Reliability Rating | A (1.0) | C (3.0) |
| Security Rating | **E (5.0)** | A (1.0) |
| Maintainability Rating | A (1.0) | A (1.0) |
| Quality Gate | OK | OK |

> El Security Rating E del backend confirma los problemas de seguridad críticos detectados en las pruebas dinámicas y en la revisión manual. El Quality Gate figura "OK" porque el Quality Gate por defecto solo evalúa bugs y deuda técnica; en las recomendaciones se incluye agregar condiciones de seguridad.

**Hallazgos relevantes de SonarQube:**

**Backend (`atlas`)**
- **Vulnerabilidad BLOCKER — `src/db.js:6` (secrets:S6698):** "Make sure this PostgreSQL database password gets changed and removed from the code." Confirma el hallazgo manual de credenciales de BD en la cadena de conexión por defecto.
- 16 Code Smells **MINOR** (`javascript:S6582`): preferir *optional chaining* en `clients.js`, `contracts.js`, `empresa_usuarios.js`, `metricas.js`.
- 1 Code Smell **MAJOR** (`users.js:44`, `javascript:S125`): código comentado.
- 4 Security Hotspots:
  - `contracts.js:14-15` (`dos`): "Make sure the content length limit is safe here" — límite de tamaño de upload no definido (relacionado con BUG-003).
  - `app.js:22` (`insecure-conf`): "Make sure that enabling CORS is safe here" (relacionado con BUG-005).
  - `app.js:20` (`others`): la plataforma expone la versión de Express por defecto.

**Frontend (`atlas-frontend`)**
- 1 **BUG MAJOR** (`src/index.css:6`, `css:S4649`): falta *generic font family* de respaldo.
- 1 **Code Smell CRITICAL** (`ClienteForm.jsx:63`, `javascript:S3776`): Complejidad cognitiva 26 vs 15 permitido.
- 181 Code Smells: 110 × validación de props (`S6774`), 45 × API deprecada (`S1874`, `*.findDOMNode`), 16 × definir componente dentro del padre (`S6478`), etc.
- 1 BUG de compatibilidad de React 19 (`findDOMNode` deprecado, relacionado con `S1874`).

**Comando usado (evidencia reproducible):**

```bash
# 1) Servidor SonarQube
docker run -d --name sonarqube -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  -v sonarqube_data:/opt/sonarqube/data \
  -v sonarqube_logs:/opt/sonarqube/logs \
  -v sonarqube_extensions:/opt/sonarqube/extensions \
  sonarqube:10.6-community

# 2) Scan (en BACKEND/ y luego en FRONTEND/, con su sonar-project.properties)
sonar-scanner -Dsonar.host.url=http://localhost:9000 -Dsonar.token=TOKEN
```

**Conclusiones del análisis estático:** SonarQube encontró 1 vulnerabilidad de severidad Blocker (credenciales de PostgreSQL en código), 4 security hotspots que corresponden exactamente a los defectos BUG-003 y BUG-005 detectados en las pruebas dinámicas, y una deuda técnica de mantenibilidad importante en el frontend (181 code smells). Esto refuerza el dictamen **NO CERTIFICADO**.

**Evidencias (capturas de pantalla):**

**Dashboard Backend (atlas):**
![Dashboard backend - atlas](Evidencias%20SonarQube/01-dashboard-backend.png)

**Dashboard Frontend (atlas-frontend):**
![Dashboard frontend - atlas-frontend](Evidencias%20SonarQube/02-dashboard-frontend.png)

**Vulnerabilidad BLOCKER (db.js:6):**
![Vulnerabilidad BLOCKER secrets:S6698 - db.js:6](Evidencias%20SonarQube/03-issues-vulnerabilidad-db.png)

**Code Smells Backend:**
![Code Smells Backend](Evidencias%20SonarQube/04-issues-code-smells-backend.png)

**Security Hotspots:**
![Security Hotspots](Evidencias%20SonarQube/05-security-hotspots.png)

**Issues Frontend:**
![Issues Frontend](Evidencias%20SonarQube/06-issues-frontend.png)

**Quality Gate (Sonar way):**
![Quality Gate Sonar way](Evidencias%20SonarQube/07-quality-gate.png)

**Resumen de Proyectos:**
![Proyectos en SonarQube](Evidencias%20SonarQube/08-projects-overview.png)

### Anexo F · Evidencias crudas de ejecución (petición y respuesta)

**Entorno y método.** Las capturas se realizaron el **28-10-2026** contra el despliegue Docker Compose local (API `http://localhost:4450`, frontend `http://localhost:3350`). Cada bloque muestra el comando `curl` ejecutado y la respuesta real del servidor: código y frase HTTP, cabeceras seleccionadas y cuerpo. Los cuerpos de más de 700 caracteres se truncan con la marca `… (salida truncada)`; el código HTTP, las cabeceras y el resultado se conservan completos. El token JWT se muestra truncado por seguridad y su longitud real se indica en el resultado.

**Trazabilidad:** el orden de los bloques coincide con las fichas de la sección 4.1 y con el detalle de ejecución de la sección 5.2. Las tablas de los Anexos A y B remiten a estos bloques.

---

```bash
API=http://localhost:4450
TOKEN=$(curl -s -X POST "$API/autenticacion/login" \
  -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"admin"}' | jq -r .token)
```

**CP-001 · Login con credenciales válidas**

```bash
curl -s -i -X POST "$API/autenticacion/login" \
  -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"admin"}'
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 245
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5…"
}
```

**Resultado:** Aprobado. HTTP 200 y JWT emitido (233 caracteres).

**CP-002 · Login con contraseña incorrecta**

```bash
curl -s -i -X POST "$API/autenticacion/login" \
  -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"incorrecta"}'
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Content-Length: 35
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "error": "Credenciales inválidas"
}
```

**Resultado:** Aprobado. HTTP 401 con mensaje genérico; no enumera usuarios.

**CP-003 · Estado de salud de la API**

```bash
curl -s -i "$API/"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 30
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "name": "Atlas",
  "status": "ok"
}
```

**Resultado:** Aprobado. HTTP 200 con `{"name":"Atlas","status":"ok"}`.

**CP-004 · Documentación Swagger**

```bash
curl -s -i -L "$API/docs/"
```

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 3106
Access-Control-Allow-Origin: *
X-Powered-By: Express


<!-- HTML for static distribution bundle build -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  
  <title>Swagger UI</title>
  <link rel="stylesheet" type="text/css" href="./swagger-ui.css" >
  <link rel="icon" type="image/png" href="./favicon-32x32.png" sizes="32x32" /><link rel="icon" type="image/png" href="./favicon-16x16.png" sizes="16x16" />
  <style>
    html
    {
      box-sizing: border-box;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
    }
    *,
    *:before,
    *:after
    {
      box-sizing: inherit;
    }

    body {
      margin:0;
      background: #fafafa;
    }
  </style>
</head>

<body>

<svg xmlns="http://www.w3.org/2000/svg
… (salida truncada)
```

**Resultado:** Aprobado. HTTP 200; interfaz Swagger disponible.

**CP-005 · Listar clientes con token**

```bash
curl -s -i "$API/clientes" \
  -H "Authorization: Bearer $TOKEN"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 3163
Access-Control-Allow-Origin: *
X-Powered-By: Express

[
  {
    "id": "4",
    "nombre": "Cliente Prueba Script",
    "correo": "script@test.cl",
    "telefono": "111",
    "direccion": "Calle 1",
    "es_empresa": false,
    "rut": null,
    "nombre_fantasia": null,
    "giro_actividad_economica": null,
    "nombre_representante": null,
    "cargo_representante": null,
    "correo_representante": null,
    "telefono_representante": null,
    "relacion_representante": null,
    "direccion_calle": null,
    "direccion_numero": null,
    "direccion_ciudad": null,
    "direccion_region": null,
    "sitio_web": null,
    "telefono_corporativo": null,
    "nombre_banco": null,
    "numero_cuenta": null,
    "titular_cuenta": null,
    "metodo_pago":
… (salida truncada)
```

**Resultado:** Aprobado. HTTP 200; lista de clientes de la empresa.

**CP-006 · Crear cliente**

```bash
curl -s -i -X POST "$API/clientes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Cliente Evidencia 1793227468","correo":"evidencia@test.cl","telefono":"999999999","direccion":"Av. Evidencia 1","es_empresa":false}'
```

```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: 669
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "id": "5",
  "nombre": "Cliente Evidencia 1793227468",
  "correo": "evidencia@test.cl",
  "telefono": "999999999",
  "direccion": "Av. Evidencia 1",
  "es_empresa": false,
  "rut": null,
  "nombre_fantasia": null,
  "giro_actividad_economica": null,
  "nombre_representante": null,
  "cargo_representante": null,
  "correo_representante": null,
  "telefono_representante": null,
  "relacion_representante": null,
  "direccion_calle": null,
  "direccion_numero": null,
  "direccion_ciudad": null,
  "direccion_region": null,
  "sitio_web": null,
  "telefono_corporativo": null,
  "nombre_banco": null,
  "numero_cuenta": null,
  "titular_cuenta": null,
  "metodo_pago": null,
  "dia_pago": null,
 
… (salida truncada)
```

**Resultado:** Aprobado. HTTP 201; cliente creado: Cliente Evidencia 1793227468.

**CP-007 · Buscar cliente por nombre**

```bash
curl -s -i "$API/clientes/search?name=Evidencia" \
  -H "Authorization: Bearer $TOKEN"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 671
Access-Control-Allow-Origin: *
X-Powered-By: Express

[
  {
    "id": "5",
    "nombre": "Cliente Evidencia 1793227468",
    "correo": "evidencia@test.cl",
    "telefono": "999999999",
    "direccion": "Av. Evidencia 1",
    "es_empresa": false,
    "rut": null,
    "nombre_fantasia": null,
    "giro_actividad_economica": null,
    "nombre_representante": null,
    "cargo_representante": null,
    "correo_representante": null,
    "telefono_representante": null,
    "relacion_representante": null,
    "direccion_calle": null,
    "direccion_numero": null,
    "direccion_ciudad": null,
    "direccion_region": null,
    "sitio_web": null,
    "telefono_corporativo": null,
    "nombre_banco": null,
    "numero_cuenta": null,
    "titular_cuenta": 
… (salida truncada)
```

**Resultado:** Aprobado. HTTP 200; el cliente creado aparece en la búsqueda.

**CP-008 · Listar contratos con token**

```bash
curl -s -i "$API/contratos" \
  -H "Authorization: Bearer $TOKEN"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 1830
Access-Control-Allow-Origin: *
X-Powered-By: Express

[
  {
    "id": "8",
    "titulo": "Contrato evidencia",
    "descripcion": null,
    "fecha_inicio": "2026-01-01T00:00:00.000Z",
    "fecha_fin": "2026-12-31T00:00:00.000Z",
    "created_at": "2026-10-28T22:43:41.040Z",
    "cliente_nombre": "María González"
  },
  {
    "id": "7",
    "titulo": "Contrato prueba exe",
    "descripcion": null,
    "fecha_inicio": "2026-01-01T00:00:00.000Z",
    "fecha_fin": "2026-12-31T00:00:00.000Z",
    "created_at": "2026-10-03T00:51:14.015Z",
    "cliente_nombre": "María González"
  },
  {
    "id": "6",
    "titulo": "Contrato HTML v2",
    "descripcion": null,
    "fecha_inicio": "2026-01-01T00:00:00.000Z",
    "fecha_fin": "2026-12-31T00:00:00.000Z",

… (salida truncada)
```

**Resultado:** Aprobado. HTTP 200; contratos de la empresa.

**CP-009 · Dashboard / métricas**

```bash
curl -s -i "$API/contratos/dashboard" \
  -H "Authorization: Bearer $TOKEN"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 114
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "totalUsuarios": 2,
  "totalClientes": 5,
  "contratosVencen7Dias": 0,
  "contratosVencen15Dias": 0,
  "contratosVencen30Dias": 0
}
```

**Resultado:** Aprobado. HTTP 200; métricas del dashboard.

**CP-010 · Subida de archivo no permitido (.exe)**

```bash
printf 'MZ fake exe content' > evidencia.exe
curl -s -i -X POST "$API/contratos" \
  -H "Authorization: Bearer $TOKEN" \
  -F "cliente_id=1" -F "titulo=Contrato evidencia EP3" \
  -F "fecha_inicio=2026-01-01" -F "fecha_fin=2026-12-31" \
  -F "file=@evidencia.exe"
```

```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: 201
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "id": "9",
  "cliente_id": "1",
  "titulo": "Contrato evidencia EP3",
  "descripcion": null,
  "fecha_inicio": "2026-01-01T00:00:00.000Z",
  "fecha_fin": "2026-12-31T00:00:00.000Z",
  "created_at": "2026-10-28T22:44:33.064Z"
}
```

**Resultado:** **FALLÓ.** HTTP 201: el `.exe` fue aceptado y almacenado (contrato ID 9) — BUG-003.

**CP-011 · Acceso a contrato sin token (IDOR)**

```bash
curl -s -i "$API/contratos/1"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 239
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "id": "1",
  "cliente_id": "1",
  "titulo": "Contrato de Servicios",
  "descripcion": "Contrato de servicios de Biotec Solutions",
  "fecha_inicio": "2026-01-01T00:00:00.000Z",
  "fecha_fin": "2026-12-31T00:00:00.000Z",
  "created_at": "2026-09-24T22:43:44.731Z"
}
```

**Resultado:** **FALLÓ.** HTTP 200 con datos del contrato sin autenticación — BUG-001.

**CP-012 · Intento de inyección SQL en login**

```bash
curl -s -i -X POST "$API/autenticacion/login" \
  -H "Content-Type: application/json" \
  -d "{\"nombre_usuario\":\"admin' OR '1'='1\",\"password\":\"x\"}"
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Content-Length: 35
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "error": "Credenciales inválidas"
}
```

**Resultado:** Aprobado. HTTP 401; la consulta parametrizada bloquea la inyección.

**CP-013 · Rendimiento de `GET /clientes` (5 mediciones)**

```bash
for i in 1 2 3 4 5; do
  curl -s -o /dev/null -w "%{time_total}\n" "$API/clientes" \
    -H "Authorization: Bearer $TOKEN"
done
```

| Medición | Tiempo | HTTP |
|---|---|---|
| 1 | 4.010 s | 200 |
| 2 | 4.013 s | 200 |
| 3 | 4.010 s | 200 |
| 4 | 4.011 s | 200 |
| 5 | 4.011 s | 200 |
| **Promedio** | **4.011 s** | 200 |
| **Mínimo** | 4.010 s | 200 |
| **Máximo** | 4.013 s | 200 |

**Resultado:** **FALLÓ.** Promedio 4.011 s frente al umbral NFR-PERF-1 de 0,300 s — BUG-010.


**CP-014 · Usabilidad y accesibilidad del login (revisión con Chromium y Lighthouse)**

No es una prueba de API, por lo que no se ejecuta con `curl`. La evidencia se obtuvo con el navegador Chromium sobre `http://localhost:3350/login` y una auditoría Lighthouse 12:

```text
document.documentElement.lang  = "en"          (contenido en español)
getComputedStyle(body).fontSize = "14px"       (≥ 12 px exigidos)
Botón "Entrar": fondo #4BBC7F, texto #FFFFFF  -> contraste 2,39:1 (AA exige 4,5:1)
document.documentElement.scrollWidth = 1000 px = innerWidth  (sin desbordamiento)
Etiquetas: <label for="nombre_usuario">, <label for="password">  (asociadas)
Lighthouse 12: accessibility 0.96 · best-practices 1.00 · SEO 0.67
Fallo automático: color-contrast (button[type=submit])
```

| N.º | Criterio | Resultado |
|---|---|---|
| 1 | Tipografía ≥ 12 px | Cumple (14 px) |
| 2 | Contraste AA | No cumple (2,39:1) |
| 3 | Etiquetas asociadas | Cumple |
| 4 | Idioma declarado | No cumple (`lang="en"`) |
| 5 | Mensajes de error claros | Parcial (toast genérico; sin mensaje en campos vacíos) |
| 6 | Sin desbordamiento horizontal | Cumple |

**Resultado:** **Aprobado con observaciones.** Lighthouse 0,96 ≥ 0,90; se registran BUG-012 (contraste, idioma, validación) y la verificación manual pendiente del foco visible.

**SEG-01 · IDOR: contrato y archivo sin token**

```bash
curl -s -i "$API/contratos/1"
curl -s -i "$API/contratos/9/file"
```

```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Length: 19
Access-Control-Allow-Origin: *
Content-Disposition: inline; filename="contrato.pdf"
X-Powered-By: Express

MZ fake exe content
```

**Resultado:** **INSEGURO.** HTTP 200 y descarga del archivo sin token; `Content-Type: application/pdf` con contenido `.exe` (contrato 9).

**SEG-02 · IDOR: usuario sin token**

```bash
curl -s -i "$API/usuarios/1"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 106
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "id": "1",
  "nombre_usuario": "admin",
  "correo": "admin@atlasfake.com",
  "created_at": "2026-09-24T22:43:44.712Z"
}
```

**Resultado:** **INSEGURO.** HTTP 200 con datos del usuario sin token.

**SEG-03 · IDOR: auditoría sin token**

```bash
curl -s -i "$API/auditoria"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 2328
Access-Control-Allow-Origin: *
X-Powered-By: Express

[
  {
    "id": "21",
    "usuario_id": "admin",
    "accion": "CONTRATOS_CREAR: creó contrato Contrato evidencia EP3 para cliente 1",
    "fecha_hora": "2026-10-28T22:44:33.075Z"
  },
  {
    "id": "20",
    "usuario_id": "admin",
    "accion": "CLIENTES_CREAR: creó cliente Cliente Evidencia 1793227468",
    "fecha_hora": "2026-10-28T22:44:28.952Z"
  },
  {
    "id": "19",
    "usuario_id": "admin",
    "accion": "LOGIN: usuario inició sesión",
    "fecha_hora": "2026-10-28T22:44:20.878Z"
  },
  {
    "id": "18",
    "usuario_id": "admin",
    "accion": "CONTRATOS_CREAR: creó contrato Contrato evidencia para cliente 1",
    "fecha_hora": "2026-10-28T22:43:41.057Z"
  },
  {
    "id": "17",
 
… (salida truncada)
```

**Resultado:** **INSEGURO.** HTTP 200 con registros de auditoría sin token.

**SEG-04 · IDOR: roles sin token**

```bash
curl -s -i "$API/roles"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 66
Access-Control-Allow-Origin: *
X-Powered-By: Express

[
  {
    "id": "2",
    "nombre": "editor"
  },
  {
    "id": "1",
    "nombre": "administrador"
  }
]
```

**Resultado:** **INSEGURO.** HTTP 200 con el listado de roles sin token.

**SEG-05 · Inyección SQL en login**

```bash
curl -s -i -X POST "$API/autenticacion/login" \
  -H "Content-Type: application/json" \
  -d "{\"nombre_usuario\":\"admin' OR '1'='1\",\"password\":\"x\"}"
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Content-Length: 35
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "error": "Credenciales inválidas"
}
```

**Resultado:** **CONFORME.** HTTP 401; consulta parametrizada.

**SEG-06 · Login inválido sin enumeración**

```bash
curl -s -i -X POST "$API/autenticacion/login" \
  -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"incorrecta"}'
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Content-Length: 35
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "error": "Credenciales inválidas"
}
```

**Resultado:** **CONFORME.** HTTP 401 con mensaje genérico.

**SEG-07b · Subida de .exe y .html**

```bash
curl -s -i -X POST "$API/contratos" \
  -H "Authorization: Bearer $TOKEN" \
  -F "cliente_id=1" -F "titulo=Contrato evidencia" \
  -F "fecha_inicio=2026-01-01" -F "fecha_fin=2026-12-31" \
  -F "file=@evidencia.exe"
# y el mismo comando con evidencia.html
```

```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: 203
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "id": "10",
  "cliente_id": "1",
  "titulo": "Contrato evidencia HTML",
  "descripcion": null,
  "fecha_inicio": "2026-01-01T00:00:00.000Z",
  "fecha_fin": "2026-12-31T00:00:00.000Z",
  "created_at": "2026-10-28T22:45:05.327Z"
}
```

**Resultado:** **INSEGURO.** HTTP 201: el `.html` también fue aceptado (el `.exe` se aceptó en CP-010) — BUG-003.

**SEG-10 · Acceso con token válido a recurso propio**

```bash
curl -s -i "$API/clientes" \
  -H "Authorization: Bearer $TOKEN"
```

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 3833
Access-Control-Allow-Origin: *
X-Powered-By: Express

[
  {
    "id": "5",
    "nombre": "Cliente Evidencia 1793227468",
    "correo": "evidencia@test.cl",
    "telefono": "999999999",
    "direccion": "Av. Evidencia 1",
    "es_empresa": false,
    "rut": null,
    "nombre_fantasia": null,
    "giro_actividad_economica": null,
    "nombre_representante": null,
    "cargo_representante": null,
    "correo_representante": null,
    "telefono_representante": null,
    "relacion_representante": null,
    "direccion_calle": null,
    "direccion_numero": null,
    "direccion_ciudad": null,
    "direccion_region": null,
    "sitio_web": null,
    "telefono_corporativo": null,
    "nombre_banco": null,
    "numero_cuenta": null,
    "titular_cuenta": 
… (salida truncada)
```

**Resultado:** **CONFORME.** HTTP 200 con token válido.

**SEG-12 · CORS con origen malicioso**

```bash
curl -s -i -X POST "$API/autenticacion/login" \
  -H "Content-Type: application/json" \
  -H "Origin: http://evil.example.com" \
  -d '{"nombre_usuario":"x","password":"y"}'
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Content-Length: 35
Access-Control-Allow-Origin: *
X-Powered-By: Express

{
  "error": "Credenciales inválidas"
}
```

**Resultado:** **INSEGURO.** `Access-Control-Allow-Origin: *` para un origen no autorizado — BUG-005.

**SEG-13 · Fuerza bruta: 3 logins fallidos**

```bash
for i in 1 2 3; do
  curl -s -o /dev/null -w "%{http_code} %{time_total}\n" \
    -X POST "$API/autenticacion/login" \
    -H "Content-Type: application/json" \
    -d '{"nombre_usuario":"admin","password":"wrong"}'
done
```

| Intento | HTTP | Tiempo |
|---|---|---|
| 1 | 401 | 4.009 s |
| 2 | 401 | 4.010 s |
| 3 | 401 | 4.010 s |

**Resultado:** **INSEGURO.** No hay bloqueo ni rate-limit; solo la latencia artificial de 4 s — BUG-006.

---

**Cierre de evidencias.** Se capturaron 14 casos (CP-001 a CP-014) y 10 pruebas de seguridad (SEG-01 a SEG-13, con las integraciones indicadas en el Anexo B). Toda afirmación de la sección 5 tiene su petición y respuesta en este anexo; no se incluyen resultados sin respaldo.

---

*Documento elaborado como entregable de la Evaluación Parcial N.º 3 (EP3) — Verificando la calidad, seguridad y cumplimiento normativo. Su contenido resume la ejecución de pruebas y las evidencias levantadas en el laboratorio de proyectos.*
