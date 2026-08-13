# Actividad 1.1.2 · Identificando Calidad, Seguridad y Cumplimiento

**Sigla:** ISY1102 · **Asignatura:** Seguridad y calidad en el desarrollo de Software · **EA1**
**Tiempo:** 1 hora · **Modalidad:** Individual · **Indicador de Logro:** IL1.1

**Objetivo:** Reconoce el rol de la calidad del software en el desarrollo de productos, valorando su contribución al éxito del proyecto y comprendiendo el cumplimiento legal y normativo como un componente esencial del proceso de desarrollo.

---

## I. Comprensión lectora: marco normativo y legal en calidad del software

Suponga que se le proporciona un documento con las siguientes áreas regulatorias y estándares:

- **Regulaciones de Protección de Datos** (ej. GDPR, Ley de Protección de Datos Personales Chilena/Latinoamericana)
- **Leyes de Propiedad Intelectual** (Derechos de Autor)
- **Estándares ISO/IEC** (ej. ISO/IEC 25010 para Calidad del Producto; ISO/IEC 27001 para Seguridad de la Información)
- **Leyes de Consumo** (relacionadas con defectos y garantías del software)

### Preguntas de selección múltiple

**1. ¿Cuál es el principal objetivo de incluir estándares como el ISO/IEC 25010 (SQuaRE) dentro del marco normativo de un proyecto de software?**

- [ ] Asegurar la portabilidad del software entre diferentes arquitecturas de hardware
- [x] **Proveer una estructura formal y métricas para evaluar y especificar los atributos de calidad del producto, como la fiabilidad y usabilidad**
- [ ] Determinar el costo final del desarrollo para fines de licitación
- [ ] Cumplir únicamente con requisitos de seguridad

**2. La inclusión de código de terceros (librerías open source con licencia permisiva) en un proyecto comercial es un aspecto regulado principalmente por:**

- [ ] La Ley de Delitos Informáticos (relacionada con hacking)
- [ ] El ISO/IEC 27001 (relacionada con la gestión de riesgos)
- [x] **Las Leyes de Propiedad Intelectual y los términos de licencia aplicables (ej. MIT, GPL)**
- [ ] Las regulaciones de accesibilidad web (WCAG)

**3. Si una ley regulatoria exige al software cumplir con altos estándares de seguridad de la información, el estándar internacional más adecuado para guiar la implementación y gestión de estos controles es:**

- [ ] ISO 9001 (Gestión de la Calidad general)
- [ ] ISO/IEC 25010 (Calidad del Producto)
- [x] **ISO/IEC 27001 (Sistemas de Gestión de Seguridad de la Información - SGSI)**
- [ ] ISO/IEC 12207 (Procesos del Ciclo de Vida del Software)

---

## II. Verdadero o Falso (justifique las falsas)

**1. La Ley de Protección de Datos Personales (GDPR o similar) solo aplica al software que gestiona tarjetas de crédito o información financiera.**

- [ ] Verdadero
- [x] **Falso** — Aplica a todo tratamiento de datos personales de ciudadanos, independiente del sector. Cubre historial médico, geolocalización, correos, etc. Un sistema de salud con historiales clínicos también está regulado.

**2. En el contexto de las Leyes de Consumo, la aparición de un bug crítico en producción que cause pérdidas económicas al usuario final podría ser considerado un "vicio o defecto" que obligue a la empresa desarrolladora a ofrecer una garantía o compensación.**

- [x] **Verdadero** — Un bug crítico que cause pérdidas económicas califica como vicio o defecto del producto, activando garantías o compensaciones.

---

## III. Preguntas de desarrollo y análisis

**Caso:** Un desarrollador creó un sistema de gestión de salud que almacena historiales médicos confidenciales. Por desconocimiento, omitió implementar cifrado fuerte en la base de datos y no definió políticas de acceso detalladas.

**a) Identifique el área del marco normativo que está violando**

> Respuesta: Está violando la normativa de **Protección de Datos Personales** (Ley 21.719 / GDPR) en los principios de **Integridad y Confidencialidad (seguridad)**, **Minimización de datos** y **Responsabilidad proactiva (accountability)**: no cifró datos sensibles ni definió políticas de acceso. Al tratarse de historiales de salud (datos sensibles), además se exige un nivel de protección reforzado.

**b) Describa la consecuencia más grave (no técnica) para la empresa desarrolladora**

> Respuesta: La consecuencia más grave es **legal/reputacional**: multas significativas y sanciones económicas por la autoridad reguladora, **pérdida de confianza de los pacientes y clientes**, posibles demandas por daños y perjuicios, y daño reputacional que puede cerrar oportunidades comerciales o afectar futuras licitaciones.

**c) Si el objetivo de calidad es asegurar que el software sea compatible con la ISO/IEC 25010, ¿cuál es la principal tarea que un Ingeniero de Calidad debe realizar durante el ciclo de vida de desarrollo (SDLC)?**

> Respuesta: Definir e implementar **métricas y criterios de evaluación por cada característica de calidad** (adecuación funcional, eficiencia de desempeño, compatibilidad, usabilidad, confiabilidad, seguridad, mantenibilidad y portabilidad), ejecutar **pruebas y verificaciones en cada fase del SDLC** para medir esos atributos, y documentar resultados para asegurar que el producto cumpla con el modelo de calidad ISO 25010.

---

## IV. Reflexión final

**¿Por qué se considera que la trazabilidad (la capacidad de rastrear un requisito legal hasta la línea de código o la feature que lo cumple) es esencial en proyectos de software altamente regulados (ej. Banca, Fintech o Medicina)?**

> Respuesta: Porque permite **demostrar el cumplimiento normativo (accountability)**: ante una auditoría o fiscalización, se puede evidenciar qué requisito legal cubre cada funcionalidad y qué código lo implementa. Facilita el análisis de impacto ante cambios normativos (saber qué módulos modificar si cambia la ley), reduce el riesgo de incumplimiento, y agiliza la revisión y corrección de defectos o vulnerabilidades con evidencia clara del alcance.

---

## Recursos de apoyo

- Marco normativo chileno: Ley 21.663 (ciberseguridad) y Ley 21.719 (datos personales)
- Estándares: ISO/IEC 25010 (calidad), ISO/IEC 27001 (seguridad)
- OWASP Top Ten: https://owasp.org/www-project-top-ten/
