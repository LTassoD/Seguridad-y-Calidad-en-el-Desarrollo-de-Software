# Guía de estudio — Cuestionario EP1 (ISY1102)

**Evaluación Parcial 1 · EA1 · Cuestionario individual (1 hora pedagógica)**
**Formato:** 20 preguntas de selección única (corrección automática) + 5 de desarrollo.
**Importante:** no se admite el uso de IA ni recursos durante el cuestionario; solo se permite un intento.

Esta guía resume los conceptos clave de las Clases 1.1, 1.2 y 1.3 para repasar antes del cuestionario.

---

## 1. Calidad del software

**Definición** (la del material): el grado en que el software cumple con los requisitos funcionales, técnicos y las expectativas reales del usuario final, garantizando una experiencia satisfactoria y confiable.

**Pilares / dimensiones:**
- Funcionalidad: el sistema hace exactamente lo que debe.
- Seguridad: protección de datos, accesos controlados, prevención de vulnerabilidades.
- Mantenibilidad: facilidad para actualizar, corregir y evolucionar el software.
- Eficiencia: uso óptimo de recursos y rendimiento adecuado.

**ISO/IEC 25010 (SQuaRE)** — 8 características de calidad del producto:
1. Adecuación funcional (completitud, corrección, pertinencia).
2. Eficiencia de desempeño (comportamiento temporal, uso de recursos, capacidad).
3. Compatibilidad (coexistencia e interoperabilidad).
4. Usabilidad (reconocibilidad, aprendizaje, operabilidad, protección contra errores, **accesibilidad**).
5. Confiabilidad (madurez, disponibilidad, tolerancia a fallos, recuperabilidad).
6. Seguridad (confidencialidad, integridad, no repudio, responsabilidad, autenticidad).
7. Mantenibilidad (modularidad, reusabilidad, analizabilidad, modificabilidad, probabilidad).
8. Portabilidad (adaptabilidad, instalabilidad, reemplazabilidad).

> Modelo de **calidad en uso**: evalúa el producto desde la perspectiva del usuario final.

## 2. Tríada CIA (pilares de la seguridad)

| Pilar | Significado |
|---|---|
| **Confidencialidad** | Solo personas autorizadas acceden a la información |
| **Integridad** | Los datos no se modifican sin autorización |
| **Disponibilidad** | Los sistemas y datos están accesibles cuando se necesitan |

## 3. Cumplimiento normativo (compliance)

Adherencia del software a leyes, regulaciones, estándares y políticas. No es opcional: el incumplimiento conlleva **multas, sanciones y daño reputacional**.

**Calidad, seguridad y cumplimiento forman un ecosistema integrado**, no son independientes: un software puede tener calidad funcional pero carecer de seguridad, o ser seguro pero no cumplir regulaciones.

## 4. Pruebas de software: funcionales vs no funcionales

| | Funcionales | No funcionales |
|---|---|---|
| **Pregunta clave** | ¿Qué hace? | ¿Cómo lo hace? |
| **Enfocadas en** | Cumplir requisitos y especificaciones | Experiencia y características operacionales |
| **Ejemplos** | Login, CRUD, cálculos, reglas de negocio | Rendimiento, carga, seguridad, usabilidad, compatibilidad |

**Complementariedad esencial:** un software funcionalmente correcto puede ser inutilizable si es lento, inseguro o no escala.

**Niveles de pruebas funcionales (secuenciales):**
1. Unitarias (componente individual).
2. Integración (interacción entre módulos).
3. Sistema (sistema completo en entorno de producción simulado).
4. Aceptación (satisfacen necesidades del usuario/negocio).

**Tipos de pruebas no funcionales:**
- **Rendimiento:** tiempos de respuesta, velocidad, estabilidad, escalabilidad.
- **Carga:** respuesta bajo un número específico de usuarios simultáneos.
- **Seguridad:** protección contra vulnerabilidades, accesos no autorizados (inyección SQL, XSS).
- **Usabilidad:** interfaz intuitiva, amigable y accesible.

**Caso típico:** en una transferencia bancaria, verificar que el monto se debita/acredita correctamente es **funcional**; procesar miles de transacciones simultáneas en <2 s es **no funcional**.

## 5. Auditoría de calidad vs auditoría legal

| Auditoría de calidad | Auditoría legal |
|---|---|
| Funcionalidad y usabilidad | Cumplimiento de licencias (open source y propietario) |
| Seguridad y protección de datos | Conformidad con normativas |
| Rendimiento y eficiencia | Protección de propiedad intelectual |
| Mantenibilidad y escalabilidad | Privacidad y tratamiento de datos personales |
| Cumplimiento de ISO 25010 | Requisitos fiscales y contables |

Ambas son imprescindibles para garantizar software confiable, legal y sostenible.

## 6. Licenciamiento de software

- **Open source permisivo (MIT, Apache):** se puede usar en software propietario/cerrado.
- **Copyleft (GPLv3):** si incorporas la librería, debes distribuir todo el software derivado bajo esa misma licencia y entregar el código fuente; no se puede vender como código cerrado.
- Usar GPLv3 en software cerrado = **infracción de derechos de autor**.

## 7. Marco normativo chileno

| Ley | Contenido |
|---|---|
| **Ley 21.663** (2024) | Ley Marco de Ciberseguridad. Crea la **ANCI** (Agencia Nacional de Ciberseguridad), define infraestructuras críticas, requisitos mínimos de seguridad y respuesta a incidentes. Exige **seguridad por diseño**. |
| **Ley 21.719** (2024) | Protección de Datos Personales (alineada al **GDPR**). 7 principios, derechos de los titulares, sanciones. Implica privacy by design y consentimiento. |
| **Ley 19.628** | Protección de Datos Personales (anterior). Cifrado, control de accesos, trazabilidad, consentimiento. |
| **Ley 21.180** | Transformación Digital del Estado: interoperabilidad, trazabilidad. |
| **CMF NCG 386/461** | Transparencia financiera y reportabilidad ESG. |

**7 principios de la Ley 21.719 (memoriza):**
1. Licitud, Lealtad y Transparencia
2. Limitación de la Finalidad
3. Minimización de Datos
4. Exactitud
5. Limitación del Plazo de Conservación
6. Integridad y Confidencialidad (Seguridad)
7. Responsabilidad Proactiva (Accountability)

> **Datos sensibles** (ej. salud) exigen protección reforzada y mayor cuidado.

## 8. Estándares internacionales

| Estándar | Tema |
|---|---|
| **ISO 9001** | Sistema de Gestión de Calidad (base de certificaciones). |
| **ISO/IEC 25010** | Modelo de calidad del producto (SQuaRE). |
| **ISO/IEC 27001:2022** | SGSI (Sistema de Gestión de Seguridad de la Información). Enfoque PDCA: Planificar → Hacer → Verificar → Actuar. |
| **ISO/IEC/IEEE 29119, IEEE 730** | Pruebas y aseguramiento de calidad de software. |

## 9. Seguridad en el desarrollo (OWASP / buenas prácticas)

- **OWASP Top Ten:** lista de vulnerabilidades web comunes.
- **Vulnerabilidades clave:** SQL Injection, XSS, CSRF, Broken Access Control (contro de acceso quebrado/IDOR), autenticación débil, exposición de secretos, mal gestión de sesiones.
- **Security by Design:** integrar seguridad desde el inicio del SDLC (código seguro, arquitectura segura, threat modeling).
- **Pruebas de seguridad:** penetración (pen-testing), escaneo de vulnerabilidades, verificación de cifrado, control de accesos, autenticación multifactor, trazabilidad.

## 10. Herramientas (para asociar correctamente)

| Herramienta | Uso |
|---|---|
| **Selenium** | Automatización de pruebas de interfaz web |
| **JUnit** | Pruebas unitarias en Java |
| **Cucumber** | Pruebas basadas en comportamiento (BDD) |
| **Postman** | Validación de APIs/web services |
| **JMeter / Locust** | Pruebas de carga y rendimiento |
| **OWASP ZAP** | Escáner de vulnerabilidades de seguridad web |
| **SonarQube** | Análisis estático de calidad y seguridad del código |
| **New Relic / Datadog / Grafana** | Monitoreo de rendimiento |
| **TestRail** | Gestión de casos de prueba |

## 11. Conceptos de un plan de pruebas (para las preguntas de desarrollo)

Un plan de pruebas incluye: **introducción, alcance, objetivos, estrategia, tipos de prueba, criterios de aceptación, recursos y cronograma**. Debe ser **coherente** con los requerimientos y las **normativas** vigentes, y mantener **trazabilidad** entre requisito legal → caso de prueba → resultado (accountability).

**Criterios de aceptación:** condiciones para considerar una prueba/proyecto aprobado.

**Trazabilidad** (pregunta recurrente de reflexión): esencial en banca/fintech/medicina porque permite demostrar cumplimiento ante auditorías, analizar el impacto ante cambios normativos y reducir el riesgo de incumplimiento.

---

## Guía rápida para el día del cuestionario

- Distinguir siempre **funcional (¿qué?) vs no funcional (¿cómo?)** al clasificar casos o requisitos.
- Asociar cada norma a su tema correcto (calidad=25010, seguridad info=27001, datos personales=21.719/19.628, ciberseguridad=21.663, calidad general=9001).
- Recordar los **7 principios** de la Ley 21.719 y la tríada **CIA**.
- Para V/F y desarrollo, justificar y dar ejemplos concretos.
