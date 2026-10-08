# Informe de Certificación — Sistema Atlas (Caso Semestral)

| Campo | Detalle |
|---|---|
| **Proyecto** | Atlas — Plataforma de gestión de clientes y contratos |
| **Asignatura** | ISY1102 · Seguridad y Calidad en el Desarrollo de Software |
| **Evaluación** | EP3 · Verificando la calidad (12% · Encargo + defensa) |
| **Alcance** | Módulos probados: Autenticación, Clientes, Contratos, Documentos, Usuarios, Métricas/Dashboard, Auditoría |
| **Herramientas** | Docker (Atlas en laboratorio), ESLint 9 (análisis estático), curl (pruebas de API), revisión manual de código |
| **Entorno** | Node 18 / Express 4.19, PostgreSQL 17, React 19 + Vite (contenedores Docker locales) |
| **Código de informe** | ALT-2026-0001-V1-INICIAL |

---

## 1. Resumen ejecutivo

Se ejecutó el proceso completo de verificación de calidad y seguridad sobre la plataforma **Atlas**, desplegada en un entorno de laboratorio controlado mediante Docker Compose (frontend `:3350`, API `:4450`, PostgreSQL `:15432`).

Se diseñaron **12 casos de prueba** (funcionales y de seguridad), todos ejecutados en dos ciclos: **Ciclo 1 · Smoke Test** (funcionalidad base) y **Ciclo 2 · Ejecución de casos** (funcional + seguridad + análisis estático).

**Resultado global:**
- **10 de 12** casos aprobados (83% de éxito).
- **2 casos fallidos** correspondientes a defectos de seguridad **Críticos** (acceso no autenticado a datos y subida de archivos sin validación).
- Análisis estático: **11 problemas** detectados por ESLint en el frontend (8 errores, 3 advertencias) y **3** en el backend, más **10 hallazgos manuales** de seguridad.

**Dictamen: NO CERTIFICADO.**

El sistema no es apto para su lanzamiento en producción: presenta vulnerabilidades de seguridad críticas explotables sin autenticación, practica inadecuada de almacenamiento de credenciales (texto claro) y defectos estructurales de control de acceso. Se recomienda un **ciclo de corrección** antes de una nueva certificación.

---

## 2. Métricas de ejecución

| Métrica | Valor |
|---|---|
| Total de casos de prueba diseñados | 12 |
| Casos ejecutados | 12 (100%) |
| Casos aprobados (Pass) | 10 (83%) |
| Casos fallidos (Fail) | 2 |
| Casos bloqueados | 0 |
| Defectos abiertos al cierre | 11 (3 Críticos · 4 Mayores · 2 Menores · 2 Observaciones) |
| Vulnerabilidades críticas explotables | 4 confirmadas con evidencia |
| Problemas análisis estático (ESLint) | 14 (frontend 11 + backend 3) |
| Resultados análisis estático (SonarQube) | 1 vulnerabilidad BLOCKER · 4 security hotspots · 198 code smells · 1 bug |
| Tiempo promedio de respuesta con token válido | ~4,0 s (latencia artificial) |

---

## 3. Gestión de defectos

### 3.1 Registro de defectos (bug report)

| ID | Severidad | Módulo | Título | Estado | Evidencia |
|---|---|---|---|---|---|
| BUG-001 | **Crítica** | Autenticación | Endpoints accesibles sin token (IDOR): `GET /contratos/1`, `GET /usuarios/1`, `GET /auditoria`, `GET /roles`, `GET /roles/:id`, `GET /empresa-usuarios/:id` | Abierto | SEG-01, SEG-03, SEG-04, SEG-05, SEG-11 |
| BUG-002 | **Crítica** | Autenticación | Credenciales en texto claro y débiles por defecto: usuarios `admin/admin` y `editor/editor`; comparación directa `contrasena_hash !== password` sin hash (auth.js:26) | Abierto | FN-01, dump-atlas.sql:344-345, auth.js:26 |
| BUG-003 | **Crítica** | Contratos | Subida de archivos sin validación de tipo/MIME: se acepta `.exe` y `.html` (multer sin filtro) y se sirven como `application/pdf` con contenido arbitrario | Abierto | SEG-07b, SEG-08b, SEG-11a |
| BUG-004 | **Mayor** | Seguridad | `JWT_SECRET` con valor de respaldo `"inseguro"` (auth.js:7, y replicado en 7 routers); firmas comprometibles | Abierto | SEG-09, revisión estática |
| BUG-005 | **Mayor** | API | CORS con `Access-Control-Allow-Origin: *` habilitado globalmente (app.js:22) | Abierto | SEG-12 |
| BUG-006 | **Mayor** | Autenticación | Ausencia de rate-limit / bloqueo por fuerza bruta en login (solo latencia fija de 4 s que amortigua parcialmente) | Abierto | SEG-13 |
| BUG-007 | **Mayor** | API | Errores 500 exponen detalle interno del motor (campo `glosa` con mensaje de PostgreSQL); operación de creación no transaccional deja datos huérfanos ante fallo de auditoría | Abierto | SEG-07, SEG-08 |
| BUG-008 | **Mayor** | Frontend | Token JWT y datos de usuario almacenados en `localStorage` (AuthContext.jsx:8-16) — robo de sesión ante XSS | Abierto | Revisión estática |
| BUG-009 | **Menor** | Frontend/Backend | Code smells ESLint: 11 issues frontend (8 × no-unused-vars, 2 × exhaustive-deps, 1 × unused disable) y 3 imports sin uso en backend | Abierto | Análisis estático |
| BUG-010 | **Observación** | Performance | Latencia artificial de 4 s (delay en auth, clientes, contratos y métricas) degrada la experiencia y facilita lentitud bajo carga | Abierto | FN-02 (4,06 s) |
| BUG-011 | **Observación** | Deuda técnica | Credenciales de PostgreSQL en código (`db.js:6`). Detectado por SonarQube como vulnerabilidad **BLOCKER** `secrets:S6698` y confirma BUG-004 | Abierto | Anexo E · SonarQube |

### 3.2 Distribución por severidad

| Severidad | Cantidad | Requiere corrección antes de certificar |
|---|---|---|
| Crítica | 3 | Sí — bloqueante |
| Mayor | 5 | Sí |
| Menor | 1 | Recomendable |
| Observación | 1 | No bloqueante |

> **Nota (base criterio):** un software con defectos **Críticos abiertos nunca debe ser certificado** (actividad 2.4.2).

---

## 4. Matriz de trazabilidad de requisitos

| ID Requisito | Requisito | Caso(s) de prueba | Resultado | Defecto asociado |
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
| RQ-10 | El sistema debe permitir adjuntar documentos a un contrato | CP-010 | **Fail** | BUG-003 |
| RQ-11 | Los datos de contratos no deben ser accesibles sin autenticación | CP-011 | **Fail** | BUG-001 |
| RQ-12 | El login debe ser resistente a inyección SQL | CP-012 | Pass | — |

---

## 5. Evaluación de riesgos

### 5.1 Riesgos mitigados

- **Inyección SQL en login:** el payload `admin' OR '1'='1` fue rechazado (`401`). Todas las consultas del backend usan consultas parametrizadas `$1..$n` (node-postgres), por lo que el riesgo de SQLi es bajo en las rutas revisadas.
- **Exposición accidental de información inncesaria en mensajes genéricos 401:** las respuestas de login son genéricas ("Credenciales inválidas") sin enumeración de usuarios.
- **Entorno de laboratorio:** implementación aislada en Docker (sin exposición pública de datos reales o clientes).

### 5.2 Riesgos aceptados

- **Latencia artificial de 4 s:** corresponde a diseño del caso académico; se acepta para la certificación, fuera del alcance de rendimiento de producción.
- **Uso de `localStorage` de sesión:** riesgo de robo de sesión ante XSS; se acepta en el alcance académico, documentado como mejora.
- **Missing de TLS** (comunicación HTTP local en laboratorio): se acepta para el entorno de pruebas; en producción debe implementarse HTTPS.

### 5.3 Riesgos residuales (requieren corrección)

- Acceso no autenticado a datos de contratos, usuarios y auditoría (BUG-001) — exposición de información sensible.
- Subida y descarga de archivos de tipo arbitrario (BUG-003) — superficie de ataque para malware/alojamiento de contenido malicioso.
- Credenciales débiles por defecto en texto claro (BUG-002) — compromiso total de la cuenta administrador.

---

## 6. Conclusión y recomendación final

**Criterio de aceptación definido:** se requiere el 100% de los casos de seguridad críticos exitosos y ningún defecto de severidad **Crítica** abierto.

**Resultado:** NO se cumplió el criterio. De los 3 casos de seguridad críticos (CP-010, CP-011 y la verificación estática de credenciales), **2 fallaron** y se confirmaron 3 defectos de severidad crítica (BUG-001, BUG-002, BUG-003).

**Dictamen final: NO CERTIFICADO** — el software requiere un nuevo ciclo de corrección.

**Acciones correctivas recomendadas (plazo sugerido antes de re-certificación):**
1. Implementar **middleware de autenticación** global (JWT) y eliminar los endpoints que no validan token (contratos `:id`, `:id/file`, usuarios `:id`, auditoría, roles, empresa-usuarios `:id`).
2. Aplicar **hash seguro de contraseñas** (bcrypt/argon2) y eliminar credenciales por defecto, forzando cambio en primer acceso.
3. Validar en **multer** el tipo MIME y extensión permitida (solo PDF) y verificar el contenido real del archivo; limitar tamaño.
4. Generar `JWT_SECRET` aleatorio y fuera de imagen (variable de entorno obligatoria).
5. Restringir **CORS** a los orígenes autorizados.
6. Agregar **rate-limit** (express-rate-limit) en `/autenticacion/login`.
7. Oculta del campo `glosa` los detalles internos del motor en errores 500; envolver creaciones en **transacciones**.
8. Corregir code smells ESLint (variables e imports sin uso) y añadir hook de lint en CI.
9. Usar **httpOnly/cookie** para la sesión en lugar de `localStorage`.
10. Configurar un **Quality Gate de SonarQube** que incluya condiciones de seguridad (0 vulnerabilidades BLOCKER/CRITICAL, security rating A) y deuda < 5 %, para que la certificación dependa de la herramienta en CI.

### 6.1 Próximas auditorías (seguimiento)

| Auditoría | Alcance | Frecuencia sugerida |
|---|---|---|
| Revisión de corrección | Verificar cierre de BUG-001, BUG-002 y BUG-003 | A los 15 días |
| Auditoría de seguimiento 1 | Re-ejecutar matriz de trazabilidad RQ-01 a RQ-12 | Mensual |
| Auditoría de seguimiento 2 | Análisis estático + pentest de acceso no autenticado | Trimestral |

---

## 7. Anexos

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

### Anexo B · Evidencias de seguridad (pruebas realizadas)

| ID Prueba | Prueba | Resultado esperado | Resultado obtenido | Severidad |
|---|---|---|---|---|
| SEG-01 | `GET /contratos/1` sin token | 401 | **200 (datos expuestos)** | Crítica |
| SEG-03 | `GET /auditoria` sin token | 401 | **200 (logs internos)** | Crítica |
| SEG-04 | `GET /roles` sin token | 401 | **200** | Mayor |
| SEG-05 | `GET /usuarios/1` sin token | 401 | **200 (correo de usuario)** | Crítica |
| SEG-07b | Subir archivo `.exe` con token | Rechazo | **201 (aceptado)** | Crítica |
| SEG-08b | Subir archivo `.html` con token | Rechazo | **201 (aceptado)** | Crítica |
| SEG-11a | Descargar archivo del contrato ID 5 sin token | 401 | **200, `Content-Type: application/pdf` con contenido `.exe`** | Crítica |
| SEG-12 | `Origin: http://evil.example.com` | Origen restringido | **`Access-Control-Allow-Origin: *`** | Mayor |
| SEG-13 | 3 intentos de login fallidos seguidos | Bloqueo/rate-limit | Ningún bloqueo (solo 4 s de espera) | Mayor |
| SEG-14 | Tiempo de respuesta de listar clientes | < 2 s | ~4,01 s (latencia artificial) | Observación |

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

> El **Security Rating E** del backend confirma los problemas de seguridad críticos detectados en las pruebas dinámicas y en la revisión manual. El Quality Gate figura "OK" porque el *Quality Gate* por defecto solo evalúa bugs y debt; ajustamos esta observación en las recomendaciones (agregar condiciones de seguridad).

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

**Conclusiones del análisis estático:** SonarQube encontró **1 vulnerabilidad de severidad Blocker** (credenciales de PostgreSQL en código), **4 security hotspots** que corresponden exactamente a los defectos BUG-003 y BUG-005 detectados en las pruebas dinámicas, y una deuda técnica de mantenibilidad importante en el frontend (181 code smells). Esto refuerza el dictamen **NO CERTIFICADO**.

#### Evidencias (capturas de pantalla)

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

*Documento elaborado como entregable de la Evaluación Parcial 3 (EP3) — Verificando la calidad. Su contenido resume la ejecución de pruebas y evidencias levantadas en laboratorio el día de la evaluación.*