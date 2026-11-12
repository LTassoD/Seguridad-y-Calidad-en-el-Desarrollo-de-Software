# Informe Técnico · Unidad 3 (ISY1102)

## Aseguramiento Continuo de Calidad y Seguridad: Pentesting, Pipeline CI/CD (OWASP ZAP), Automatización (Selenium IDE / POM) y Pruebas de Estrés (JMeter)
### Sistema Evaluado: Plataforma Atlas · Octubre–Noviembre 2026

**Integrantes:** Luis Tasso · Miguel Arredondo · Nicolas Iturrieta
**Asignatura:** ISY1102 — Seguridad y Calidad en el Desarrollo de Software · Sección 002V
**Docente:** Christian Rodrigo Alvarez Lobos

---

## 1. Subunidad 3.1 · Ejecución y Análisis de Pruebas de Seguridad (Pentesting)

### 1.1. Enfoque, Tipos de Caja y Marco Legal/Ético

Conforme a los contenidos de la guía `3.1.1`, una prueba de penetración (*pentesting*) es un ataque informático simulado, autorizado y controlado cuyo propósito es identificar vulnerabilidades antes de que sean explotadas, evaluar la efectividad de las defensas existentes, proporcionar evidencias reproducibles y verificar el cumplimiento normativo (**ISO/IEC 27001**, **ISO/IEC 25010** y **Ley 19.628 / 21.719**).

- **Modalidad aplicada en Atlas:** combinación de **Grey Box (Caja Gris)** para las pruebas dinámicas autenticadas y no autenticadas sobre la API REST (`:4450`) y el frontend (`:3350`), y **White Box (Caja Blanca)** para la auditoría del código fuente, esquemas SQL y configuración de contenedores Docker.
- **Marco legal y ético aplicado:**
  1. **Autorización explícita:** ejecución restringida exclusivamente al entorno controlado de laboratorio Docker local (`localhost`), evitando cualquier tráfico hacia sistemas productivos o de terceros.
  2. **Acuerdo de confidencialidad (NDA) y protección de datos:** utilización exclusiva de registros sintéticos (clientes y contratos ficticios) y enmascaramiento de tokens JWT en las evidencias.
  3. **Límites del alcance:** evaluación acotada a los contenedores `atlas-frontend` (`:3350`), `atlas-backend` (`:4450`) y `atlas-db` (`:15432`).

### 1.2. Ejecución de las 6 Fases de la Metodología de Pentesting en Atlas

| Fase | Actividades ejecutadas sobre Atlas | Herramientas | Hallazgo principal |
|---|---|---|---|
| **1. Reconocimiento** | Revisión pasiva del repositorio, variables de entorno y documentación pública; mapeo activo de rutas expuestas. | `curl`, navegador, inspección de código | Exposición pública de Swagger en `/docs/` y credenciales en `db.js:6` y `dump-atlas.sql`. |
| **2. Escaneo** | Identificación de puertos abiertos (`3350`, `4450`, `15432`), tecnologías (Express, React, PostgreSQL) y cabeceras HTTP. | `curl -i`, `OWASP ZAP`, `Burp Suite` | Cabecera `Access-Control-Allow-Origin: *` y ausencia total de cabeceras de endurecimiento (`helmet`). |
| **3. Enumeración** | Enumeración de usuarios, roles, contratos y registros de auditoría mediante identificadores secuenciales. | `curl`, scripts Bash (`test_atlas.sh`) | `GET /usuarios/1`, `GET /roles`, `GET /auditoria` y `GET /contratos/1` responden `HTTP 200` sin token. |
| **4. Explotación** | Ejecución controlada de vectores de inyección SQL, XSS, fuerza bruta, acceso directo a objetos (IDOR) y subida de ejecutables. | `sqlmap`, `curl`, `Burp Repeater` | Subida de archivo `.exe` y `.html` aceptada (`HTTP 201`) y servida como `application/pdf`; ausencia de bloqueo en login. |
| **5. Post-explotación** | Evaluación de impacto cruzado entre empresas, persistencia de archivos maliciosos en base de datos (`bytea`) y exposición de contraseñas en texto claro. | Consultas a API y revisión de `auth.js` | Compromiso total de confidencialidad e integridad multi-empresa; almacenamiento de contraseñas sin hash (`auth.js:26`). |
| **6. Documentación** | Clasificación de hallazgos en 5 niveles (**Crítico, Alto, Medio, Bajo, Informativo**), registro de evidencias y plan de remediación. | Informe técnico y Anexo F | 4 vulnerabilidades Críticas y 6 Altas/Graves documentadas con evidencia reproducible. |

### 1.3. Vectores Técnicos Ejecutados (Guía 3.1.2)

1. **Escaneo dinámico y enumeración:**
   Se verificó la exposición de recursos internos sin autenticación en `/usuarios/1`, `/contratos/1`, `/roles` y `/auditoria`, obteniendo correos reales del dataset semilla y registros de actividad.
2. **Inyección SQL (SQLi):**
   Se probó la rotura de consulta en `/autenticacion/login` y en el filtro `/clientes?nombre=a'` mediante payloads manuales (`admin' OR '1'='1`) y automatizados:
   ```bash
   sqlmap -u "http://localhost:4450/clientes?nombre=test" \
     -H "Authorization: Bearer $TOKEN" --dbs --batch
   ```
   El backend utiliza consultas parametrizadas (`$1`, `$2`) con `pg`, neutralizando la inyección SQL (`HTTP 401` / `HTTP 200` vacío).
3. **Cross-Site Scripting (XSS):**
   Se inyectó el vector de prueba de la guía `3.1.2` en la creación de clientes y en la subida de documentos:
   ```html
   <script>alert('Vulnerable XSS');</script>
   ```
   Aunque React escapa por defecto las cadenas renderizadas en tablas JSX, el endpoint `POST /contratos` acepta archivos `.html` con JavaScript activo sin sanitizar ni validar tipo MIME.
4. **Autenticación y Fuerza Bruta (Criterio ISO/IEC 25010):**
   Se ejecutó una ráfaga de intentos fallidos sobre `POST /autenticacion/login`. El sistema no implementa `express-rate-limit`, captcha ni bloqueo de IP tras múltiples intentos fallidos, incumpliendo la característica de **Seguridad (Autenticidad y Responsabilidad)** de **ISO/IEC 25010**.

### 1.4. Bitácora Técnica de Pruebas de Seguridad (Formato Oficial Guía 3.1.2)

| ID Prueba | Tipo de ataque | Herramienta | Resultado Obtenido | Severidad |
|---|---|---|---|---|
| **SEG-01** | Enumeración e IDOR en contratos, usuarios y auditoría | `curl` / `Burp Suite` | `GET /contratos/1`, `/usuarios/1` y `/auditoria` sin token devuelven `HTTP 200` con datos confidenciales y archivos adjuntos | **Crítica** |
| **SEG-02** | Fuerza bruta y diccionario en `/autenticacion/login` | Script Bash / `Burp Intruder` | Permite intentos ilimitados sin bloqueo de IP ni rate-limit; contraseñas por defecto (`admin/admin`) activas | **Crítica** |
| **SEG-03** | SQL Injection (`SQLi`) en login y búsqueda | `sqlmap` / `curl` | `HTTP 401` en login; no se detectaron parámetros inyectables gracias a consultas parametrizadas (`$1`) | **Pass** |
| **SEG-04** | Subida de archivo malicioso (`.exe` / `.html`) | `curl` / `Burp Suite` | `HTTP 201 Created`: el servidor almacena ejecutables y HTML sin `fileFilter` y los sirve en `/contratos/:id/file` | **Crítica** |
| **SEG-05** | Cross-Site Scripting (`XSS`) y contenido activo | Navegador / `curl` | Texto en tabla escapado por React, pero subida de `.html` con `<script>alert('Vulnerable XSS');</script>` es aceptada (`HTTP 201`) | **Alta** |
| **SEG-06** | Configuración CORS y credenciales en texto claro | Revisión + `curl -i` | `Access-Control-Allow-Origin: *` ante origen externo (`evil.example.com`) y comparación en texto claro en `auth.js:26` | **Crítica** |

### 1.5. Recomendación para la Certificación (Formato Guía 3.1.2)

> **"SISTEMA NO CERTIFICADO: Se identificaron vulnerabilidades críticas de control de acceso roto (IDOR sin autenticación), almacenamiento de credenciales en texto claro y carga irrestricta de archivos ejecutables (`.exe` / `.html`) que comprometen la integridad y confidencialidad de los datos de los clientes."**

---

## 2. Subunidad 3.2 · Diseño de un Pipeline CI/CD con Controles de Seguridad y DAST con OWASP ZAP

### 2.1. Estrategia de Calidad: Pirámide de Testing y Filosofía Fail Fast

Siguiendo la guía `3.2.1`, el aseguramiento continuo de Atlas se estructura sobre la **Pirámide de Testing** y el principio **Fail Fast** (detener el pipeline ante el primer fallo rápido para no desperdiciar recursos):

1. **Base (Unitarias y Validación Temprana):** verificación rápida de funciones puras, validadores de RUT/formato y reglas de negocio aisladas.
2. **Capa Intermedia (Integración):** validación de la interacción entre API Express (`:4450`) y PostgreSQL (`:15432`) mediante `test_atlas.sh` (14 casos CP y 10 pruebas SEG).
3. **Vértice (End-to-End / E2E):** validación de los flujos críticos de negocio desde el navegador con **Selenium IDE / Selenium WebDriver + POM**.

### 2.2. Anatomía del Pipeline CI/CD y Controles Shift-Left Security (DevSecOps)

El archivo ejecutable `ci-devsecops-atlas.yml` implementa las **5 etapas esenciales del pipeline** integrando los **4 controles Shift-Left Security**:

| Etapa del Pipeline | Control Integrado | Herramienta en `ci-devsecops-atlas.yml` | Condición de Bloqueo (Fail Fast) |
|---|---|---|---|
| **1. Control de Versiones (Source)** | **Validación de Secrets** | `gitleaks/gitleaks-action@v2` | Falla si detecta contraseñas o claves (`db.js:6`, `JWT_SECRET`) en el commit. |
| **2. Construcción (Build) + SCA** | **Gestión de Dependencias** | `npm ci` + `npm audit --audit-level=high` | Falla si existen librerías de terceros con vulnerabilidades High/Critical. |
| **3. Análisis Estático (SAST)** | **SAST (Código Fuente)** | `ESLint 9` + `SonarQube Scan` | Falla si el Quality Gate detecta vulnerabilidades BLOCKER/CRITICAL o Security Rating < A. |
| **4. Testing Automatizado (Test)** | **Pirámide (Integración + E2E)** | `bash test_atlas.sh` + `python test_atlas_pom.py` | Falla si cualquier caso funcional, de seguridad o flujo Selenium E2E no aprueba. |
| **5. Análisis Dinámico (DAST) y Deploy** | **DAST (App en ejecución)** | **OWASP ZAP** (`zaproxy/action-full-scan`) | Ejecuta *Spider* + *Active Scan*, publica `report_html.html` y bloquea el despliegue si hay alertas altas. |

**Métricas de éxito definidas para el pipeline (`3.2.1`):**
- **Tiempo de Build:** < 15 minutos desde el commit hasta el artefacto validado.
- **Tasa de Éxito:** ≥ 95 % de ejecuciones estables en rama principal.
- **Cobertura de Código:** objetivo ≥ 80 % en módulos críticos (`auth`, `clients`, `contracts`).
- **MTTR (*Mean Time To Recovery*):** < 2 horas para remediar y redesplegar ante un fallo detectado.

### 2.3. Ejecución e Interpretación de OWASP ZAP (Formato Oficial Guía 3.2.2)

Al ejecutar el flujo de **OWASP ZAP** (*1. Spider* sobre `http://localhost:3350` y `http://localhost:4450` para descubrir rutas y `/docs/`, seguido de *2. Active Scan* y *3. Generate HTML Report*), las alertas detectadas en la configuración actual de Atlas se interpretan conforme a la tabla exigida en la guía `3.2.2`:

| Alerta encontrada | Severidad | Impacto en la calidad | Estado |
|---|---|---|---|
| **Cross-Domain Misconfiguration (`Access-Control-Allow-Origin: *`)** | Alta | Permite que dominios externos no autorizados lean respuestas de la API; vulnera la confidencialidad (ISO 25010) | Abierta (`BUG-005`) |
| **Absence of Anti-CSRF Tokens / Insecure Session Storage** | Media | Exposición a acciones forzadas y robo de sesión por almacenamiento del JWT en `localStorage` | Abierta (`BUG-008`) |
| **Missing Anti-Clickjacking Header (`X-Frame-Options` / `CSP frame-ancestors`)** | Media | La interfaz de Atlas puede ser incrustada en un `<iframe>` malicioso para engañar al usuario (*Clickjacking*) | Abierta |
| **X-Content-Type-Options Header Missing (`nosniff`)** | Baja / Crítica en combinación con `BUG-003` | El navegador puede interpretar y ejecutar archivos subidos (`.html` / `.exe`) adivinando su tipo MIME | Abierta (`BUG-003`) |
| **Information Disclosure — Suspicious Comments / OpenAPI Exposed (`/docs/`)** | Baja | Facilita el reconocimiento activo de todos los endpoints y esquemas internos del backend | Abierta |

### 2.4. Recomendación Técnica de Mitigación DAST (Formato Guía 3.2.2)

> *"Se recomienda incorporar y configurar el middleware `helmet` en `BACKEND/src/app.js`, restringir `cors({ origin: process.env.ALLOWED_ORIGIN })` y migrar el almacenamiento del JWT a cookies `httpOnly; Secure; SameSite=Strict` con protección Anti-CSRF, mitigando más del 70 % de las alertas de configuración y cabeceras reportadas por OWASP ZAP."*

---

## 3. Subunidad 3.3 · Automatización de Pruebas Funcionales y Normativas (Selenium IDE + POM)

### 3.1. Criterios de Selección de Pruebas a Automatizar (Guía 3.3.2)

No todo caso de prueba debe automatizarse. Siguiendo la guía `3.3.2`, se seleccionaron **3 flujos clave de Atlas** justificados bajo los tres criterios técnicos obligatorios:

| Flujo seleccionado | 1. Frecuencia (Regresión) | 2. Riesgo de Negocio | 3. Facilidad y Estabilidad |
|---|---|---|---|
| **A. Autenticación (`AUT-01_Login_Exitoso`)** | Se ejecuta en cada commit y antes de cualquier otro caso de prueba. | Es la puerta de entrada; si falla, el 100 % del sistema queda inutilizable. | Flujo lineal con selectores estables (`id="nombre_usuario"`, `id="password"`, `data-testid="button-login"`). |
| **B. Creación de Cliente (`AUT-02_Crear_Cliente`)** | Valida la operación transaccional principal del CRM en cada versión. | Permite registrar a las empresas clientes sobre las cuales se emiten los contratos. | Formulario estructurado con identificadores únicos (`id="rut-cliente-create"`, `id="crear-cliente-create"`). |
| **C. Verificación de Listado y Cierre de Sesión (`AUT-03_Verificar_Listado_y_Logout`)** | Verifica la persistencia entre frontend, API y PostgreSQL y el cierre de sesión. | Garantiza que los datos creados sean visibles por la empresa correspondiente y que la sesión finalice. | Navegación directa a `/clientes` y botón de salida con `data-testid="button-layout-logout"`. |

### 3.2. Diseño y Aserciones en Selenium IDE (`Atlas_Selenium_IDE.side`)

El proyecto `Atlas_Selenium_IDE.side` implementa los tres flujos con **comandos explícitos de verificación (`verifyText` y `assertText`)**, cumpliendo la regla de la guía `3.3.2` (*"Sin verificación, no hay prueba real"*):

- **`AUT-01_Login_Exitoso`:** abre `/login` → `verifyText` sobre `css=h4` (`"Iniciar Sesión"`) → ingresa `admin` / `admin` → clic en `css=[data-testid="button-login"]` → `waitForElementVisible` → **`assertText`** sobre `css=[data-testid="link-nav-clientes"]` (`"Clientes"`).
- **`AUT-02_Crear_Cliente`:** abre `/clientes` → `verifyText` `"Gestión de Clientes"` → clic en pestaña `"Crear Cliente"` → completa RUT (`76.543.210-K`), nombre, correo y teléfono → clic en `id=crear-cliente-create` → **`verifyText`** `"Clientes registrados"`.
- **`AUT-03_Verificar_Listado_y_Logout`:** abre `/clientes` → **`verifyText`** `"Clientes registrados"` → clic en `css=[data-testid="button-layout-logout"]` → **`assertText`** `"Iniciar Sesión"`.

### 3.3. Registro de Automatización (Formato Oficial Guía 3.3.2)

| ID Caso | Nombre del script | Herramienta | Resultado | Observaciones |
|---|---|---|---|---|
| **AUT-01** | `AUT-01_Login_Exitoso` | Selenium IDE / WebDriver | **Pass** | Tiempo de ejecución: ~4,3 s (incluye latencia de `delay(4000)` en `/autenticacion/login`). Aserción `assertText` en menú principal verificada. |
| **AUT-02** | `AUT-02_Crear_Cliente` | Selenium IDE / WebDriver | **Pass** | Tiempo de ejecución: ~4,6 s. Crea el cliente con RUT `76.543.210-K` y verifica retorno automático a `"Clientes registrados"`. |
| **AUT-03** | `AUT-03_Verificar_Listado_y_Logout` | Selenium IDE / WebDriver | **Pass** | Tiempo de ejecución: ~4,2 s. Verifica la tabla de clientes y valida redirección a `/login` tras cerrar sesión. |

### 3.4. Revisión y Mejora del Código de Pruebas: Refactorización a Page Object Model (Guía 3.3.1)

Conforme a la guía `3.3.1`, los scripts grabados inicialmente presentan tres problemas recurrentes: **1) duplicación de selectores manuales**, **2) baja mantenibilidad por falta de modularidad** y **3) esperas fijas frágiles**. Para solucionarlo, se refactorizó la suite en el archivo `test_atlas_pom.py` aplicando:

1. **Patrón de diseño Page Object Model (POM):** encapsulación de los selectores y acciones en las clases `LoginPage` y `ClientesPage`, logrando una reducción superior al 40 % en líneas duplicadas.
2. **Esperas dinámicas explícitas (`WebDriverWait` + `expected_conditions`):** reemplazo de pausas fijas por esperas inteligentes que absorben el `delay(4000)` del backend sin producir falsos negativos.
3. **Manejo estructurado de errores y logs (`logging` + `try/finally`):** cierre garantizado del navegador y trazabilidad lista para ejecutarse en el pipeline CI/CD.

---

## 4. Subunidad 3.4 · Mantenimiento Continuo y Pruebas de Estrés en un Sistema Crítico (JMeter)

### 4.1. Fundamentos: Carga vs. Estrés, RTO/RPO y Seguridad bajo Presión (Guía 3.4.1)

- **Prueba de Carga vs. Prueba de Estrés:** la **Prueba de Carga** evalúa el comportamiento bajo demanda normal o prevista (validando NFR-PERF-1 < 300 ms); la **Prueba de Estrés** somete a Atlas a cargas extremas por sobre su capacidad para identificar el **punto de ruptura (quiebre)**, el modo de fallo y la capacidad de recuperación.
- **Métricas de resiliencia definidas para Atlas:**
  - **RPO (*Recovery Point Objective*):** **0 transacciones corruptas** (la base de datos PostgreSQL no debe dejar clientes o contratos a medio crear si el backend colapsa durante una ráfaga).
  - **RTO (*Recovery Time Objective*):** **< 30 segundos** para que el contenedor `atlas-backend` vuelva a responder peticiones con latencia normal tras finalizar una ráfaga de tráfico.
- **Vínculo con Ciberseguridad (DDoS y *Race Conditions*):**
  En Atlas coexisten dos defectos críticos para la resiliencia:
  1. `delay(4000)` artificial en los endpoints (`BUG-010`), que retiene cada conexión abierta durante 4 segundos y facilita un agotamiento de recursos (*Application-Layer DoS*) con pocos usuarios.
  2. Creación de registros en múltiples consultas SQL sin bloque `BEGIN ... COMMIT` (`BUG-007`), lo que bajo alta concurrencia expone a **condiciones de carrera (*Race Conditions*)** e inconsistencia de datos.

### 4.2. Configuración de los 3 Escenarios de Demanda en Apache JMeter (Guía 3.4.2)

El archivo ejecutable `Atlas_Stress_Test_JMeter.jmx` implementa los **tres grupos de hilos (`Thread Group`)** y los **tres receptores (`Listeners`)** exigidos por la guía `3.4.2`:

| Escenario en `Atlas_Stress_Test_JMeter.jmx` | Configuración de Hilos (`Thread Group`) | Endpoint Evaluado | Objetivo Técnico |
|---|---|---|---|
| **A. Carga Constante** | **10 usuarios concurrentes** (`num_threads=10`, `ramp_time=1 s`, `loops=5`) | `GET /contratos/1` y `GET /clientes` | Establecer línea base de tiempo de respuesta y Throughput bajo demanda normal. |
| **B. Prueba de Estrés** | **0 a 500 usuarios en 5 minutos** (`num_threads=500`, `ramp_time=300 s`) | `GET /clientes` y `GET /contratos/1` | Identificar el número exacto de usuarios concurrentes donde se satura el pool de PostgreSQL y aparecen errores `500` / `504` o timeouts. |
| **C. Prueba de Pico (*Spike*)** | **10 a 200 usuarios en 10 segundos** (`num_threads=200`, `ramp_time=10 s`) | `POST /autenticacion/login` | Evaluar la resistencia ante una ráfaga súbita de inicios de sesión y medir el tiempo de recuperación (**RTO**). |

**Listeners incluidos en el plan `.jmx`:**
1. *Ver Árbol de Resultados (`ViewResultsFullVisualizer`)* — verificación de códigos HTTP 200 vs. 500.
2. *Gráfico de Resultados (`GraphVisualizer`)* — curva visual de degradación.
3. *Informe Agregado (`StatVisualizer`)* — cálculo de **Throughput**, **Latency** y **Error %**.

### 4.3. Métricas Clave para el Informe de Certificación (Formato Oficial Guía 3.4.2)

| Métrica | Descripción | Valor crítico (Guía 3.4.2) | Comportamiento observado / esperado en Atlas |
|---|---|---|---|
| **Throughput** | Cantidad de peticiones procesadas por segundo (`req/s`). | Si cae mientras suben los usuarios, existe un cuello de botella severo. | En los endpoints con `delay(4000)` (`login`, `clientes`, `contratos`), el Throughput cae por debajo de **2,5 req/s** para 10 usuarios y se estanca al saturarse el pool de conexiones de PostgreSQL (`max=10` por defecto en `pg.Pool`). |
| **Latency (Latencia)** | Tiempo que tarda en llegar el primer byte de respuesta. | **> 2 segundos** indica mala experiencia de usuario e incumplimiento no funcional. | **4,011 segundos** ya con 1 usuario en `GET /clientes` (`CP-013` / `BUG-010`), superando en **13,4 veces** el umbral de 300 ms del ERS y el límite crítico de 2 s de la guía. |
| **Error %** | Porcentaje de peticiones fallidas (`HTTP 500`, `502`, `504` o *Connection Refused*). | En estrés, **> 5 %** indica inestabilidad crítica del servicio. | Al superar los **150–200 usuarios concurrentes** en los endpoints que retienen conexión por 4 s y abren consultas sin limitar el pool, las peticiones entran en cola hasta agotar timeouts, superando el 5 % de error. |

### 4.4. Hallazgo de Estrés para el Informe de Certificación (Formato Guía 3.4.2)

> *"Durante las pruebas de rendimiento y estrés sobre Atlas, se comprobó que los endpoints principales (`/autenticacion/login`, `/clientes`, `/contratos` y `/metricas`) presentan una latencia base de **4,011 s** debido a la instrucción `delay(4000)` (`BUG-010`), incumpliendo desde carga mínima el umbral crítico de 2 s. Bajo el escenario de estrés progresivo (0 a 500 usuarios en 5 minutos), la retención artificial de 4 s por solicitud combinada con un pool de conexiones PostgreSQL sin dimensionamiento ni control transaccional (`BUG-007`) provoca encolamiento exponencial y degradación del Throughput, demostrando que el sistema requiere eliminar la latencia artificial, parametrizar el pool de conexiones e incorporar rate-limiting antes de pasar a producción."*
