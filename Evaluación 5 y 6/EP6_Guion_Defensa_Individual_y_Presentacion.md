# Guía de Presentación y Defensa Individual — EP5 y EP6 (ISY1102)

## Optimizando el Aseguramiento de la Calidad y Seguridad del Software · Sistema Atlas
**Evaluación:** EP6 (Presentación y defensa — **24 %**, evaluación **100 % individual**) · Coherente con EP5 (**11 %**, Encargo grupal) y Evaluación Final Transversal (**40 %**)
**Formato:** **10 minutos de exposición** + **5 minutos de ronda de preguntas** (orden de exposición aleatorio; cada integrante debe dominar el 100 % del proyecto).
**Integrantes (Grupo 2):** Luis Tasso · Miguel Arredondo · Nicolas Iturrieta · Sección 002V · Docente: Christian Rodrigo Alvarez Lobos.

---

## 1. Mapa de Coherencia EP5 ↔ EP6 ↔ Evaluación Final Transversal

| Indicador de Logro | En Informe EP5 (Encargo — 11 %) | En Defensa EP6 (Presentación — 24 %) | Peso | Diapositivas |
|---|---|---|---|---|
| **IL 3.1** | `IE1`: Enfoques y herramientas de pruebas de seguridad según su función con ejemplos reales. | `IE2`: Exponer enfoques y herramientas de seguridad, finalidad y relevancia en detección de vulnerabilidades. | **30 %** | Slides 3–4 |
| **IL 3.2** | `IE3`: Diagramas de controles de seguridad automatizados + criterios normativos/legales. | `IE4`: Explicar el diagrama del pipeline CI/CD destacando controles y relación normativa/legal. | **14 %** | Slide 5 |
| **IL 3.3** | `IE5`: Automatización de casos de prueba (eficiencia y aseguramiento de calidad). | `IE6`: Mostrar evidencias ejecutadas (logs, reportes, flujos) demostrando impacto en tiempo y recursos. | **24 %** | Slides 6–7 |
| **IL 3.4** | `IE7`: Análisis de planes de mantenimiento (continuidad de calidad, seguridad y normativa). | `IE8`: Comunicar elementos del plan de mantenimiento relacionados con estándares y normativas. | **20 %** | Slide 8 |
| **IL 3.5** | `IE9`: Documentación técnica clara, regulatoria y calidad sostenible. | `IE10`: Recursos visuales (gráficos, reportes, comparativas) que facilitan la comprensión. | **12 %** | Todas (Diagramas 1–3) |

---

## 2. Estructura Sugerida de Presentación (10 Diapositivas · 10 Minutos)

| Slide | Título | Tiempo | Contenido Clave y Recurso Visual | Indicador EP6 |
|---|---|---|---|---|
| **1** | Portada — Aseguramiento Continuo de Atlas | 0:30 | Título, Grupo 2, Sección 002V, Docente, objetivo de la fase final y evolución EP1 → EP3 → EP5/EP6. | Contexto |
| **2** | Evolución del Proyecto y Correcciones Aplicadas | 0:45 | Cierre de las fortalezas EP1 + las 6 correcciones de EP3 (evidencia cruda, 21 códigos reales ERS, `RF-5.2` = 5 formatos, mediciones repetidas, fallos contabilizados, cronograma + fecha/ejecutor). | Coherencia semestral |
| **3** | Enfoques y Herramientas de Seguridad (Caja Blanca y Gris) | 1:15 | Tabla comparativa: Gitleaks (Secretos), `npm audit` (SCA), SonarQube/ESLint (SAST), Pytest/curl/sqlmap (Pentesting 6 fases), OWASP ZAP (DAST). Marco ético/legal (Docker local, datos sintéticos). | **IE2 (30 %)** |
| **4** | Resultados Reales de Seguridad: Pentesting y DAST | 1:30 | Evidencias del `12-11-2026` (`reporte_dast_zap_atlas.html`): `PENT-01` IDOR (`HTTP 200` sin token), `PENT-02` sin rate-limit, `PENT-03` SQLi bloqueado (`$1`), `PENT-04/05` `.exe`/`.html` XSS (`HTTP 201`) + 5 alertas OWASP ZAP (CORS `*`, sin Helmet/CSP). | **IE2 (30 %) + IE6** |
| **5** | Pipeline CI/CD DevSecOps y Trazabilidad Normativa | 1:15 | **Insertar `Diagrama_01_Pipeline_DevSecOps_Normativo.png`**. Explicar las 5 etapas, *Shift-Left*, *Fail Fast* y enlace con ISO 27001 (`A.9.4/A.10/A.12.4/A.14.2`), ISO 25010, OWASP Top 10 y Ley 19.628/21.719. | **IE4 (14 %) + IE10** |
| **6** | Automatización Funcional E2E (Selenium IDE + POM) | 1:00 | Criterios de selección (frecuencia, riesgo, estabilidad), flujos `AUT-01..03` (13,1 s totales), refactorización a **Page Object Model** (> 40 % menos duplicación, `WebDriverWait` frente a `delay(4000)`). | **IE6 (24 %)** |
| **7** | Evidencias de Estrés (JMeter) e Impacto en Tiempo/Recursos | 1:15 | **Insertar `Diagrama_02_Impacto_Automatizacion_y_Estres.png`**. Comparativa Manual vs. Automatizado (**-93 % tiempo por ciclo**), 575 muestras reales: `/contratos/1` soporta 200 usuarios (342,4 ms, RTO **8,4 ms**), `/clientes` colapsa a **4.019 ms** / 6,17 req/s por `delay(4000)` (vector App-Layer DoS). | **IE6 (24 %) + IE10 (12 %)** |
| **8** | Plan de Mantenimiento para Futuras Iteraciones | 1:15 | **Insertar `Diagrama_03_Plan_Mantenimiento_Calidad_Sostenible.png`**. Explicar los 4 frentes **ISO/IEC 14764** (Correctivo Sprint 0, Preventivo en cada PR, Adaptativo Ley 21.719/Examen Transversal, Perfectivo WCAG/Pool/JMeter) y los 4 Gates por release. | **IE8 (20 %) + IE10** |
| **9** | Reflexiones de Calidad, Seguridad, Normativa y Ética | 0:45 | Impacto real en Ley 19.628/21.719 e ISO 27001; cobertura honesta actualizada (7/21 = 33,3 % con `NFR-PERF-3` cubierto); dictamen **NO CERTIFICADO** (4 Críticos + 7 Graves abiertos) y divulgación responsable. | **IE8 + IE10** |
| **10** | Cierre y Preparación para Evaluación Final Transversal | 0:30 | Demostrar que la suite (`auditor_transversal_atlas.py`, `test_atlas_pom.py`, `test_atlas_pentest_dast.py`, `test_atlas_stress.py`) permite reauditar cambios de código en minutos. | Cierre + Transversal |

---

## 3. Guion de Defensa Individual (10 Minutos Exactos)

> **Consejo clave de la pauta EP6:** *«Aunque el proyecto se trabaja de forma grupal, la defensa es individual. Si durante la defensa un/a estudiante no puede explicar con claridad el proyecto, se asumirá que no participó activamente».* Practica este guion completo para poder defender **cualquier bloque** si el docente te pregunta o sortea el orden.

### Bloque 1 · Apertura y Evolución Semestral (0:00 – 1:15)
> *"Buenos días/tardes profesor. Presentamos la fase final de aseguramiento de calidad y seguridad sobre la plataforma **Atlas** (React, Express y PostgreSQL en Docker). En esta etapa integramos el plan estratégico de EP1 y la verificación estática/funcional de EP3 —manteniendo las 6 correcciones aplicadas tras su feedback: evidencia cruda reproducible, trazabilidad exclusiva a los 21 códigos reales del ERS, `RF-5.2` con sus 5 formatos permitidos, múltiples casos no funcionales con mediciones repetidas, contabilización honesta de fallos y cronograma con fecha y ejecutor— junto con las pruebas de seguridad dinámicas, el pipeline CI/CD DevSecOps, la automatización E2E, las pruebas de estrés y el Plan de Mantenimiento para futuras iteraciones."*

### Bloque 2 · Enfoques, Herramientas y Resultados de Seguridad — `IE2` (1:15 – 4:00)
> *"Para detectar vulnerabilidades de forma integral combinamos **Caja Blanca** y **Caja Gris**, respetando el marco ético y legal: todo se ejecutó exclusivamente en nuestro laboratorio Docker local con datos sintéticos.*
> *En **Caja Blanca**, aplicamos **Gitleaks** para secretos, **npm audit** para dependencias (SCA), **ESLint 9** y **SonarQube 10.6** (SAST), confirmando 1 vulnerabilidad **BLOCKER** (`db.js:6` con credenciales PostgreSQL en código) y un **Security Rating E** en el backend.*
> *En **Caja Gris**, ejecutamos las 6 fases de **Pentesting** mediante `test_atlas_pentest_dast.py` y **OWASP ZAP** (DAST) el 12 de noviembre de 2026. Los resultados fueron concluyentes:*
> - *`PENT-01` (IDOR): `GET /contratos/1`, `/usuarios/1` y `/auditoria` devuelven `HTTP 200` sin token (`BUG-001`, Crítico — OWASP A01).*
> - *`PENT-02`: ráfaga sobre `/autenticacion/login` devuelve `401` sin `HTTP 429` ni bloqueo de IP (`BUG-006`).*
> - *`PENT-03` (SQLi): `admin' OR '1'='1` fue bloqueado (`HTTP 401`) porque el backend usa consultas parametrizadas `$1`.*
> - *`PENT-04` y `PENT-05`: `POST /contratos` aceptó un `.exe` y un `.html` con `<script>` XSS con `HTTP 201` (`BUG-003`), violando `RF-5.2`.*
> - *Y **OWASP ZAP** levantó 5 alertas activas: `Access-Control-Allow-Origin: *` (Alta), falta de `X-Frame-Options`, `nosniff` y `CSP` (Medias), y Swagger `/docs/` expuesto (Baja)."*

### Bloque 3 · Diagrama del Pipeline CI/CD y Cumplimiento Normativo — `IE4` (4:00 – 5:15)
> *"En el **Diagrama 1** mostramos cómo materializamos estos controles en `ci-devsecops-atlas.yml` bajo la filosofía **Shift-Left** y **Fail Fast** en 5 etapas:*
> *1) **Source & Secrets** con Gitleaks (cumple **ISO 27001 A.10** y **OWASP A02**);*
> *2) **Build & SCA** con `npm ci` y `npm audit --audit-level=high` (**OWASP A06**);*
> *3) **SAST** con ESLint y SonarQube exigiendo Security Rating A y deuda < 5 % (**ISO 25010**);*
> *4) **Testing Automatizado** con Docker, `test_atlas.sh` y nuestra suite Selenium POM (**ISO/IEC/IEEE 29119**);*
> *5) **DAST y Deploy condicionado** con OWASP ZAP Full Scan antes de pasar a Staging (**ISO 27001 A.9.4/A.14.2** y **Ley 19.628 / 21.719**).*
> *Si cualquier control detecta un fallo crítico, el pipeline detiene el despliegue automáticamente."*

### Bloque 4 · Automatización E2E, Estrés e Impacto en Tiempo/Recursos — `IE6` + `IE10` (5:15 – 7:30)
> *"Para optimizar tiempo y recursos automatizamos los 3 flujos E2E de mayor frecuencia, riesgo y estabilidad (`AUT-01` Login, `AUT-02` Crear Cliente y `AUT-03` Listado y Logout) en Selenium IDE y luego los refactorizamos a **Page Object Model** en `test_atlas_pom.py`. Esto redujo en más de **40 %** la duplicación de código y reemplazó pausas fijas por `WebDriverWait`, absorbiendo el `delay(4000)` del backend sin falsos negativos.*
> *Como muestra el **Diagrama 2**, pasar del enfoque manual de EP3 (~180 minutos entre 3 personas) a la ejecución automatizada (~12 minutos) logra un **93 % de ahorro de tiempo** por ciclo de regresión, con evidencia HTML y CSV trazable.*
> *En pruebas de carga, estrés y pico (`test_atlas_stress.py` / JMeter, **575 muestras reales**), cubrimos `NFR-PERF-3`: `GET /contratos/1` soportó **200 usuarios simultáneos** en 342,4 ms con 0 % de error y un **RTO real de 8,4 ms**. En contraste, `GET /clientes` con solo 25 hilos colapsó a **4.019 ms** y 6,17 req/s porque ejecuta `delay(4000)` incluso antes de devolver `HTTP 401`, exponiendo a Atlas a un ataque **DoS a nivel de aplicación**."*

### Bloque 5 · Plan de Mantenimiento, Reflexiones y Cierre — `IE8` (7:30 – 10:00)
> *"Para que la calidad no se degrade en futuras iteraciones, en el **Diagrama 3** estructuramos un **Plan de Mantenimiento según ISO/IEC 14764** en 4 frentes:*
> - ***Correctivo (Sprint 0):** cerrar los 4 incidentes Críticos (`BUG-001`, `BUG-002`, `BUG-003`, `BUG-011`) y 7 Graves (Helmet, CORS, rate-limit, cookies `httpOnly`, eliminar `delay(4000)` y usar transacciones SQL).*
> - ***Preventivo (en cada PR):** mantener activos los *gates* de `ci-devsecops-atlas.yml` (Gitleaks, SCA, SonarQube, Selenium POM y OWASP ZAP).*
> - ***Adaptativo (trimestral / cambios de alcance):** adecuar Atlas a la **Ley 21.719** (derechos ARCO, retención, brechas), actualizar contenedores base y usar nuestro script `auditor_transversal_atlas.py` para detectar cambios de código en futuras versiones.*
> - ***Perfectivo (por release):** bajar la complejidad cognitiva de `ClienteForm.jsx`, corregir contraste WCAG AA (`BUG-012`), dimensionar `pg.Pool` y re-ejecutar JMeter validando CRUD < 300 ms, RTO < 30 s y RPO = 0.*
> *Concluimos manteniendo el dictamen técnico honesto de **SISTEMA NO CERTIFICADO** mientras persistan vulnerabilidades críticas abiertas que incumplen ISO 27001 y la Ley 19.628/21.719, pero dejando toda la infraestructura DevSecOps lista para certificar el próximo release. Quedo atento a sus preguntas."*

---

## 4. Banco de Preguntas Frecuentes del Docente (5 Minutos de Defensa)

1. **¿Por qué su dictamen sigue siendo «NO CERTIFICADO» si ya implementaron CI/CD y automatización?**
   - *Respuesta:* Porque la automatización y el pipeline **detectan y bloquean** defectos, pero no corrigen el código fuente del caso evaluado (por integridad de auditoría no alteramos el código entregado). Permanecen abiertos 4 incidentes Críticos (`BUG-001`, `BUG-002`, `BUG-003`, `BUG-011`), Security Rating E en SonarQube y 5 alertas OWASP ZAP. Un sistema con defectos críticos abiertos no debe certificarse.

2. **¿Cuál es la diferencia práctica entre SAST, SCA y DAST en su pipeline?**
   - *Respuesta:* **SAST** (SonarQube/ESLint) analiza nuestro código fuente sin ejecutarlo y encontró `db.js:6` (`secrets:S6698`). **SCA** (`npm audit`) revisa librerías de terceros en `package.json` contra CVEs públicos. **DAST** (OWASP ZAP) ataca la aplicación ya desplegada en Docker y detectó fallas de configuración en tiempo de ejecución como CORS `*`, falta de `X-Frame-Options`, `nosniff` y `CSP`. Son complementarios; ninguno reemplaza al otro.

3. **¿Por qué refactorizaron de Selenium IDE a Page Object Model (POM)? ¿Qué impacto concreto tuvo?**
   - *Respuesta:* Los scripts grabados duplican selectores y fallan con esperas fijas ante el `delay(4000)` de Atlas. Con POM (`LoginPage` y `ClientesPage`) encapsulamos los selectores en un solo lugar (reduciendo > 40 % de código duplicado) y usamos `WebDriverWait` explícito. Además, cada prueba incluye `assertText`/`verifyText`, bajando la regresión E2E de ~25 min manuales a ~13,1 s automatizados.

4. **En sus pruebas de estrés, ¿por qué `/contratos/1` respondió en 342 ms con 200 usuarios pero `/clientes` tardó 4.019 ms con 25 usuarios?**
   - *Respuesta:* Porque `/contratos/1` no tiene la instrucción `delay(4000)` (aunque tiene `BUG-001` al responder 200 sin token), demostrando que Express + PostgreSQL sí tienen capacidad de cómputo (254,76 req/s y RTO 8,4 ms). En cambio, `/clientes` tiene un `delay(4000)` artificial (`BUG-010`) que incluso se ejecuta antes de devolver `HTTP 401`, convirtiéndolo en un vector de **DoS a nivel de aplicación** que desploma el Throughput a 6,17 req/s.

5. **¿Cómo justifican que su Plan de Mantenimiento preserva el cumplimiento legal en Chile?**
   - *Respuesta:* A través de dos frentes: el **Preventivo**, que impide mediante Gitleaks, SonarQube y OWASP ZAP que se vuelva a filtrar una contraseña o un endpoint sin autenticación (protegiendo la confidencialidad exigida por Ley 19.628); y el **Adaptativo**, que planifica la adecuación a la **Ley 21.719** (derechos ARCO, trazabilidad inmutable de auditoría, minimización y gestión de brechas) junto con el reajuste del plan de pruebas ante cada cambio del software.

6. **¿Qué pasa si en la Evaluación Final Transversal les entregan una versión modificada de Atlas con nuevas fallas?**
   - *Respuesta:* Precisamente para eso construimos `auditor_transversal_atlas.py`, que compara archivo por archivo contra `CodigoFuenteA`, detecta automáticamente patrones SAST nuevos y genera un reporte HTML, complementado con nuestra suite `test_atlas_pentest_dast.py`, `test_atlas_pom.py` y `test_atlas_stress.py` para reajustar la matriz ERS y re-ejecutar en minutos.
