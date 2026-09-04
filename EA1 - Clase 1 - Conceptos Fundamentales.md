# Clase 1 · Conceptos Fundamentales: Calidad, Seguridad y Cumplimiento

**Asignatura:** Seguridad y Calidad en el Desarrollo de Software (ISY1102) · **EA1** · Clase 1
**Fuente:** "1.1.1 Qué entendemos por calidad, Seguridad y Cumplimiento en el software.pdf" (resumen)

---

## 1. Conceptos fundamentales

### Calidad del software
Grado en que un producto cumple los requisitos especificados y satisface las necesidades y expectativas de los usuarios. No es solo "que no falle": debe aportar valor real. Dimensiones según **ISO/IEC 25010**:

| Dimensión | Descripción |
|---|---|
| Funcionalidad | Realiza las funciones especificadas correctamente y con resultados precisos |
| Confiabilidad | Mantiene su nivel de rendimiento bajo condiciones establecidas |
| Usabilidad | Facilidad para aprender, operar y obtener satisfacción del sistema |
| Eficiencia | Rendimiento adecuado en relación con los recursos utilizados |

### Seguridad del software
Protección de aplicaciones y sistemas contra amenazas, vulnerabilidades y ataques. Se integra **desde el diseño**, no al final. Incluye: controles de acceso, cifrado, autenticación robusta, protección contra inyecciones y vulnerabilidades comunes (OWASP Top 10).

**Tríada CIA:**
1. **Confidencialidad** — solo personas autorizadas acceden a la información
2. **Integridad** — los datos no se modifican sin autorización
3. **Disponibilidad** — sistemas y datos accesibles cuando se necesitan

### Cumplimiento normativo (compliance)
Adherencia a leyes, regulaciones, estándares y políticas aplicables. No es opcional: el incumplimiento genera sanciones legales, multas y daño reputacional. Cumplir genera confianza en clientes y socios.

### Ecosistema integrado
Calidad, seguridad y cumplimiento **no son independientes**; trabajan en conjunto. Puede haber software funcional pero inseguro, o seguro pero fuera de norma. El objetivo es el equilibrio de los tres.

---

## 2. Marco normativo chileno

### Ley N° 21.663 — Ley Marco de Ciberseguridad (2024)
- Crea la **Agencia Nacional de Ciberseguridad (ANCI)** como organismo rector.
- Define **infraestructuras críticas de información**.
- Establece **requisitos mínimos de seguridad** y protocolos de respuesta a incidentes.
- **Impacto en desarrollo (Security by Design):**
  - Prácticas de código seguro (prevenir vulnerabilidades OWASP Top 10)
  - Arquitectura segura (componentes, APIs e infraestructura resistentes)
  - Modelado de amenazas (threat modeling) antes de escribir código
- **Impacto en operación:**
  - Monitoreo y logging auditable (requisitos ANCI)
  - Notificación obligatoria de incidentes ("Operadores de Servicios Esenciales")
- **Impacto en QA y mantenimiento:**
  - Pruebas de seguridad rigurosas (pen-testing, escaneo de vulnerabilidades periódico y documentado)
  - Gestión formal y rápida de vulnerabilidades con trazabilidad

### Ley N° 21.719 — Protección de Datos Personales (2024)
Alineada con el **GDPR** europeo. Exige *privacy by design*, consentimientos válidos, derechos de los usuarios y seguridad de los datos.

**7 principios:**
1. Licitud, lealtad y transparencia
2. Limitación de la finalidad
3. Minimización de datos
4. Exactitud
5. Limitación del plazo de conservación
6. Integridad y confidencialidad (seguridad)
7. Responsabilidad proactiva (accountability) — poder demostrar el cumplimiento

---

## 3. Estándares internacionales

### ISO/IEC 27001:2022 — SGSI
Marco para el sistema de gestión de seguridad de la información. Enfoque basado en procesos y gestión de riesgos. Ciclo **PDCA** (Planificar–Hacer–Verificar–Actuar). La versión 2022 actualiza controles para ransomware, nube y privacidad. La certificación es requerida en licitaciones y contratos.

### ISO/IEC 25010:2011 — SQuaRE (modelos de calidad)
**8 características de calidad del producto:**
1. **Adecuación funcional** — completitud, corrección y pertinencia
2. **Eficiencia de desempeño** — comportamiento temporal, uso de recursos, capacidad
3. **Compatibilidad** — coexistencia e interoperabilidad
4. **Usabilidad** — reconocibilidad, aprendizaje, operabilidad, protección contra errores
5. **Confiabilidad** — madurez, disponibilidad, tolerancia a fallos, recuperabilidad
6. **Seguridad** — confidencialidad, integridad, no repudio, responsabilidad, autenticidad
7. **Mantenibilidad** — modularidad, reusabilidad, analizabilidad, modificabilidad
8. **Portabilidad** — adaptabilidad, instalabilidad, reemplazabilidad

---

## 4. Pausa reflexiva (dilema del desarrollador)
Entrega con plazo ajustado: un bug funcional menor (calidad) y una pequeña vulnerabilidad de inyección (seguridad). Corregir ambos = 48 h de retraso con penalización. ¿Entregas a tiempo o asumes el retraso? La respuesta correcta desde el punto de vista profesional: asumir el retraso y garantizar seguridad y calidad.

---

## 5. Tarea para la casa
A la luz de la Ley 21.719, analizar un formulario de registro en línea:
- ¿Piden más datos de los necesarios? (**minimización**)
- ¿Es clara la finalidad del uso de datos? (**finalidad**)

---

## 6. Referencias
1. Ley N° 21.663: Ley Marco de Ciberseguridad e Infraestructura Crítica de la Información (2024).
2. Ley N° 21.719: Ley de Protección de Datos Personales (2024).
3. ANCI — https://anci.gob.cl/normativa/leyes/
4. ISO/IEC 25010:2011 — https://www.iso.org/standard/35733.html
5. ISO/IEC 27001:2022 — https://www.iso.org/standard/27001
