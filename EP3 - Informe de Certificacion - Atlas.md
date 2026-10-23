# Informe de seguridad y calidad en el desarrollo de software

## ISY1102 — Seguridad y Calidad en el Desarrollo de Software

### Sección 002V

Carrera: Ingeniería en Desarrollo de Software

Docente: Christian Rodrigo Alvarez Lobos

Fecha: 17 de octubre de 2026

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

- **Cobertura ampliada al 100 % de los requerimientos del ERS:** la matriz de trazabilidad (sección 4.2) vincula los 12 requisitos evaluados con sus casos de prueba y resultados, superando los 5 casos representativos del EP1.
- **Ejecución real y evidencia verificable:** donde el EP1 presentaba diseño y análisis preliminar, este informe registra la ejecución efectiva de los 12 casos con resultado, evidencia y defecto asociado (sección 5), más las pruebas complementarias de seguridad (Anexo B).
- **Análisis estático ampliado:** se incorpora SonarQube 10.6 sobre backend y frontend, además de ESLint 9 y la revisión manual, dejando métricas y capturas de pantalla como evidencia (Anexo E).
- **Escala de criticidad estandarizada:** los incidentes se clasifican con escala CRITICO/GRAVE/MODERADO/LEVE con impacto y remediación definidos (sección 5.3), conforme a la estructura de informes de certificación.
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
- **Pruebas no funcionales de rendimiento:** medición de tiempos de respuesta de los endpoints CRUD frente a los umbrales NFR-PERF-1/2, detectando la latencia artificial de 4 s del código.
- **Pruebas de usabilidad:** revisión exploratoria de la interfaz y sus estados (menores: validación de campos, mensajes de error), acotada al alcance de este ciclo.

### 3.3. Criterios de aceptación

Un caso se considera aprobado cuando:

- **Funcional:** la acción produce el resultado esperado sin errores; la respuesta es correcta en formato y contenido; las acciones críticas generan registro de auditoría.
- **No funcional:** los endpoints CRUD responden en menos de 300 ms bajo carga normal y la página principal carga en menos de 2 s (NFR-PERF-1/2).
- **Seguridad:** ningún endpoint devuelve datos sensibles sin token válido; solo se aceptan archivos PDF en la subida; el login resiste inyección SQL; no existen vulnerabilidades críticas detectadas (OWASP A01, A02, A07, A08).
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

---

## 4. Diseño de casos de prueba

### 4.1. Fichas de casos representativos

Se diseñaron y ejecutaron 12 casos de prueba (CP-001 a CP-012) con cobertura del 100 % de los requerimientos evaluados del ERS. A continuación se detallan sus fichas en el formato exigido: ID, nombre, requerimiento asociado, descripción, precondiciones, pasos, resultado esperado, criterio de aceptación, datos de prueba y tipo de prueba.

**CP-001 · Login con credenciales válidas**

| Campo | Detalle |
|---|---|
| **ID** | CP-001 |
| **Nombre** | Inicio de sesión y obtención de token |
| **Requerimiento** | RF-1 / RF-1.1 (El sistema debe permitir autenticarse con nombre_usuario y contraseña) |
| **Tipo de prueba** | Funcional / Seguridad |
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
| **Nombre** | Adjuntar documento a contrato con archivo `.exe` |
| **Requerimiento** | RF-5 / NFR-SEG (El sistema debe permitir adjuntar solo documentos seguros a un contrato) |
| **Tipo de prueba** | Seguridad |
| **Descripción** | Verificar que el sistema rechaza archivos que no sean PDF en la subida de documentos |
| **Precondiciones** | Token válido; contrato existente; archivo ejecutable de prueba disponible |
| **Pasos** | 1. Con token, enviar `POST /contratos/:id/file` con archivo `prueba.exe`. 2. Observar código de respuesta. 3. Repetir con archivo `.html`. 4. Intentar descargarlo. |
| **Datos de prueba** | Archivos `prueba.exe` y `prueba.html` (tipo MIME binario y text/html) |
| **Resultado esperado** | Rechazo (400/415) por tipo de archivo no permitido |
| **Criterio de aceptación** | Solo se aceptan archivos PDF; cualquier otro tipo es rechazado y queda registro |
| **Resultado obtenido** | **Fallo (FAIL):** HTTP 201, el archivo `.exe` fue aceptado y almacenado, y se sirve como `application/pdf` — defecto CRITICO (BUG-003) |

**CP-011 · Acceso a contrato sin token (IDOR)**

| Campo | Detalle |
|---|---|
| **ID** | CP-011 |
| **Nombre** | Acceso a datos de contrato sin autenticación |
| **Requerimiento** | NFR-SEG-4 / NFR-SEG-9 / RB-2 (Los datos de contratos no deben ser accesibles sin autenticación) |
| **Tipo de prueba** | Seguridad |
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
| **Descripción** | Verificar que el backend no es vulnerable a inyección SQL en el endpoint de login |
| **Precondiciones** | Backend desplegado; endpoint `POST /autenticacion/login` disponible |
| **Pasos** | 1. Enviar login con payload `admin' OR '1'='1` en el campo usuario. 2. Verificar código de respuesta. 3. Verificar que no se emite token. |
| **Datos de prueba** | `{"nombre_usuario": "admin' OR '1'='1", "password": "x"}` |
| **Resultado esperado** | HTTP 401, sin token emitido |
| **Criterio de aceptación** | La consulta parametrizada rechaza el payload y no entrega sesión (OWASP A03) |
| **Resultado obtenido** | **Aprobado (PASS):** HTTP 401; todas las consultas del backend usan parámetros `$1..$n` (node-postgres) |

**FN-02 · Tiempo de respuesta de listado de clientes**

| Campo | Detalle |
|---|---|
| **ID** | FN-02 |
| **Nombre** | Verificación de tiempo de respuesta del CRUD |
| **Requerimiento** | NFR-PERF-1 (respuesta CRUD < 300 ms bajo carga normal) y NFR-PERF-2 (página < 2 s) |
| **Tipo de prueba** | No funcional (Rendimiento) |
| **Descripción** | Medir el tiempo de respuesta del endpoint `GET /clientes` con token válido |
| **Precondiciones** | Sistema desplegado; token válido; red local sin carga |
| **Pasos** | 1. Ejecutar `GET /clientes` con token. 2. Registrar el tiempo total de respuesta. 3. Comparar con el umbral de 300 ms. |
| **Datos de prueba** | Dataset de clientes semilla + creados en pruebas |
| **Resultado esperado** | Respuesta en menos de 300 ms |
| **Criterio de aceptación** | Se cumple NFR-PERF-1 |
| **Resultado obtenido** | **Fallo documentado:** ~4,06 s por `delay(4000)` artificial del código (BUG-010) — riesgo aceptado en el ámbito académico, bloqueante en producción |

### 4.2. Matriz de trazabilidad de requisitos

| ID Requisito | Requerimiento ERS | Caso(s) de prueba | Resultado | Defecto asociado |
|---|---|---|---|---|
| RQ-01 | El usuario debe poder autenticarse con credenciales válidas | CP-001 | Pass | — |
| RQ-02 | El sistema debe rechazar credenciales inválidas | CP-002 | Pass | — |
| RQ-03 | La API debe exponer un estado de salud ("ok") | CP-003 | Pass | — |
| RQ-04 | Debe existir documentación de la API (Swagger) | CP-004 | Pass | — |
| RQ-05 | El usuario autenticado debe listar los clientes de su empresa | CP-005 | Pass | — |
| RQ-06 | El sistema debe permitir crear un cliente | CP-006 | Pass | — |
| RQ-07 | El sistema debe permitir buscar clientes por nombre | CP-007 | Pass | — |
| RQ-08 | El usuario autenticado debe listar los contratos | CP-008 | Pass | — |
| RQ-09 | El sistema debe mostrar métricas del dashboard | CP-009 | Pass | — |
| RQ-10 | El sistema debe permitir adjuntar documentos seguros a un contrato | CP-010 | **Fail** | BUG-003 |
| RQ-11 | Los datos de contratos no deben ser accesibles sin autenticación | CP-011 | **Fail** | BUG-001 |
| RQ-12 | El login debe ser resistente a inyección SQL | CP-012 | Pass | — |

**Cobertura:** 12 de 12 requerimientos evaluados (100 %) cuentan con al menos un caso de prueba con resultado registrado.

---

## 5. Ejecución de pruebas

### 5.1. Resumen de ejecución

| Métrica | Valor |
|---|---|
| Total de casos de prueba diseñados | 12 |
| Casos ejecutados | 12 (100 %) |
| Casos aprobados (Pass) | 10 (83 %) |
| Casos fallidos (Fail) | 2 |
| Casos bloqueados | 0 |
| Pruebas de seguridad complementarias (SEG) | 10 (7 inseguras / 3 conformes) |
| Incidentes registrados | 11 (4 CRITICO · 5 GRAVE · 1 MODERADO · 1 LEVE) |
| Problemas análisis estático (ESLint) | 14 (frontend 11 + backend 3) |
| Resultados análisis estático (SonarQube) | 1 vulnerabilidad BLOCKER · 4 security hotspots · 198 code smells · 1 bug |
| Tiempo promedio de respuesta con token válido | ~4,0 s (latencia artificial) |

Los dos casos fallidos corresponden a defectos de seguridad CRITICO (CP-010 y CP-011). El caso FN-02 queda registrado como hallazgo de rendimiento (BUG-010, riesgo aceptado por ser latencia artificial del caso académico).

### 5.2. Detalle de ejecución de casos

| CASO | DESCRIPCIÓN | RESULTADO | EVIDENCIA | TIPO DE PRUEBA |
|---|---|---|---|---|
| CP-001 | Login con credenciales válidas | Aprobado | HTTP 200 + JWT emitido (~4,13 s) — Anexo A | Funcional |
| CP-002 | Login con contraseña incorrecta | Aprobado | HTTP 401 "Credenciales inválidas", sin enumeración de usuarios — Anexo A | Funcional / Seguridad |
| CP-003 | Estado/salud de la API | Aprobado | HTTP 200 `{"name":"Atlas","status":"ok"}` — Anexo A | Funcional / Integración |
| CP-004 | Documentación Swagger `/docs/` | Aprobado | HTTP 200, interfaz interactiva — Anexo A | Funcional / Integración |
| CP-005 | Listar clientes (token) | Aprobado | HTTP 200; 3 clientes (2 semilla + 1 creado) — Anexo A | Funcional |
| CP-006 | Crear cliente | Aprobado | HTTP 201; cliente ID 3 "Cliente Prueba EP3" — Anexo A | Funcional |
| CP-007 | Buscar cliente por nombre | Aprobado | HTTP 200; búsqueda "Mar" → María González — Anexo A | Funcional |
| CP-008 | Listar contratos (token) | Aprobado | HTTP 200; 6 contratos (2 semilla + 4 de prueba) — Anexo A | Funcional |
| CP-009 | Dashboard / métricas (token) | Aprobado | HTTP 200; 2 usuarios, 3 clientes — Anexo A | Funcional |
| CP-010 | Subir documento a contrato (archivo `.exe`) | **Falló** | HTTP 201: archivo ejecutable aceptado sin validación (BUG-003) — Anexo B SEG-07b | Seguridad |
| CP-011 | Acceso a contrato sin token (`GET /contratos/1`) | **Falló** | HTTP 200 con datos del contrato sin autenticación (BUG-001) — Anexo B SEG-01 | Seguridad |
| CP-012 | Login con intento SQLi (`admin' OR '1'='1`) | Aprobado | HTTP 401; consulta parametrizada lo bloquea — Anexo A | Seguridad |
| SEG-01 a SEG-13 (10 pruebas) | Pruebas complementarias de seguridad (acceso sin token, upload, SQLi, CORS, fuerza bruta) | 7 inseguros / 3 conformes | Detalle en Anexo B | Seguridad |
| FN-02 | Tiempo de respuesta de `GET /clientes` | No conforme (latencia artificial) | ~4,06 s vs. umbral 300 ms (BUG-010) — Anexo A | No funcional (Rendimiento) |

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
| BUG-010 | Latencia artificial de 4 s (`delay(4000)`) en operaciones CRUD | Degradación de experiencia; falla NFR-PERF (FN-02: 4,06 s) | MODERADO |
| BUG-009 | Code smells ESLint: 11 frontend (no-unused-vars, exhaustive-deps) y 3 backend | Deuda técnica sin impacto funcional | LEVE |

> Un software con defectos CRITICO abiertos nunca debe ser certificado. Al cierre del ciclo permanecen 4 incidentes CRITICO y 5 GRAVE abiertos.

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

**Resultado:** NO se cumplió el criterio. De los casos de seguridad críticos, CP-010 y CP-011 fallaron, y permanecen abiertos 4 incidentes CRITICO (BUG-001, BUG-002, BUG-003, BUG-011). SonarQube confirma 1 vulnerabilidad BLOCKER y Security Rating E en el backend.

**Dictamen final: NO CERTIFICADO** — el software no es apto para producción y requiere un ciclo de corrección antes de una nueva certificación.

**Acciones correctivas recomendadas:**

1. Middleware de autenticación global (JWT) en todos los endpoints que leen o modifican datos (BUG-001).
2. Hash seguro de contraseñas (bcrypt/argon2) y eliminación de credenciales por defecto con cambio obligatorio en primer acceso (BUG-002).
3. Validación de tipo MIME y extensión en la subida de archivos, limitando a PDF y verificando el contenido real (BUG-003).
4. `JWT_SECRET` y credenciales de base de datos fuera del código, en variables de entorno obligatorias (BUG-004, BUG-011).
5. Restricción de CORS a los orígenes autorizados (BUG-005).
6. Rate-limit en `/autenticacion/login` (BUG-006).
7. Envolver creaciones en transacciones y ocultar detalles internos del motor en errores 500 (BUG-007).
8. Corregir code smells ESLint y añadir hook de lint en CI (BUG-009).
9. Reemplazar `localStorage` por cookies `httpOnly` para la sesión (BUG-008).
10. Quality Gate de SonarQube en CI con condiciones de seguridad: 0 vulnerabilidades BLOCKER/CRITICAL, Security Rating A y deuda < 5 %.

---

## 7. Anexos y evidencias

### Anexo A · Bitácora de ejecución (actividad 2.3.2)

**Ciclo 1 · Smoke Test** (objetivo: verificar funciones base; si falla, se detiene la ejecución)

| ID | Nombre | Estado | Defecto | Observaciones |
|---|---|---|---|---|
| CP-001 | Login con credenciales válidas (admin/admin) | Aprueba | N/A | HTTP 200, JWT emitido. Respuesta en ~4,13 s (latencia artificial) |
| CP-002 | Login con contraseña incorrecta | Aprueba | N/A | HTTP 401 "Credenciales inválidas" en ~4,01 s. No enumera usuarios |
| CP-003 | Estado/salud de la API | Aprueba | N/A | HTTP 200 `{"name":"Atlas","status":"ok"}` |
| CP-004 | Documentación Swagger `/docs/` | Aprueba | N/A | HTTP 200 (interfaz interactiva) |

**Ciclo 2 · Ejecución de casos de prueba**

| ID | Nombre | Estado | Defecto | Observaciones |
|---|---|---|---|---|
| CP-005 | Listar clientes (token) | Aprueba | N/A | HTTP 200 en ~4,06 s; retorna 3 clientes (2 semilla + 1 creado) |
| CP-006 | Crear cliente | Aprueba | N/A | HTTP 201; cliente ID 3 "Cliente Prueba EP3" |
| CP-007 | Buscar cliente por nombre | Aprueba | N/A | HTTP 200; búsqueda "Mar" → María González |
| CP-008 | Listar contratos (token) | Aprueba | N/A | HTTP 200; 6 contratos (2 semilla + 4 de prueba) |
| CP-009 | Dashboard / métricas (token) | Aprueba | N/A | HTTP 200; 2 usuarios, 3 clientes |
| CP-010 | Subir documento a contrato (archivo `.exe`) | Falló | BUG-003 | HTTP 201: se aceptó el archivo ejecutable sin validación |
| CP-011 | Acceso a contrato SIN token (`GET /contratos/1`) | Falló | BUG-001 | HTTP 200 devuelve datos del contrato sin autenticación |
| CP-012 | Login con intento SQLi (`admin' OR '1'='1`) | Aprueba | N/A | HTTP 401; consulta parametrizada lo bloquea |

### Anexo B · Evidencias de seguridad (pruebas complementarias)

| ID Prueba | Prueba | Resultado esperado | Resultado obtenido | Severidad |
|---|---|---|---|---|
| SEG-01 | `GET /contratos/1` y descarga de archivo sin token | 401 | **200 (contrato y PDF con contenido `.exe`)** | Crítica |
| SEG-02 | `GET /usuarios/1` sin token | 401 | **200 (correo de usuario)** | Crítica |
| SEG-03 | `GET /auditoria` sin token | 401 | **200 (logs internos)** | Crítica |
| SEG-04 | `GET /roles` sin token | 401 | **200** | Mayor |
| SEG-05 | Login con payload SQLi (`admin' OR '1'='1`) | 401 | 401 (consulta parametrizada) | Conforme |
| SEG-06 | Login con contraseña incorrecta (sin enumeración) | 401 | 401 | Conforme |
| SEG-07b | Subir archivo `.exe` y `.html` con token | Rechazo 400/415 | **201 (aceptado)** | Crítica |
| SEG-10 | Acceso con token válido a recurso propio | 200 | 200 | Conforme |
| SEG-12 | `Origin: http://evil.example.com` | Origen restringido | **`Access-Control-Allow-Origin: *`** | Mayor |
| SEG-13 | 3 intentos de login fallidos seguidos | Bloqueo/rate-limit | Ningún bloqueo (solo 4 s de espera) | Mayor |

**Total: 10 pruebas SEG — 7 inseguras (SEG-01, SEG-02, SEG-03, SEG-04, SEG-07b, SEG-12, SEG-13) y 3 conformes (SEG-05, SEG-06, SEG-10).**

> Las pruebas SEG-08b y SEG-11a se integran como evidencia dentro de SEG-07b y SEG-01, respectivamente. SEG-09 corresponde al hallazgo de `JWT_SECRET` detectado por revisión manual (BUG-004) y no se contabiliza como prueba dinámica independiente. FN-02 (rendimiento) se registra en el Anexo A como prueba no funcional, no como SEG.

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

---

*Documento elaborado como entregable de la Evaluación Parcial N.º 3 (EP3) — Verificando la calidad, seguridad y cumplimiento normativo. Su contenido resume la ejecución de pruebas y las evidencias levantadas en el laboratorio de proyectos.*
