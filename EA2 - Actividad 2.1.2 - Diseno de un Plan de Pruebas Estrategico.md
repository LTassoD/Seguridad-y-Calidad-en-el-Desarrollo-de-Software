# EA2 · Actividad 2.1.2 — Diseño de un Plan de Pruebas Estratégico (Calidad, Riesgo y Seguridad)

**Asignatura:** ISY1102 · Seguridad y calidad en el desarrollo de software
**Actividad:** 2.1.2 | **IL2.1** | **Tiempo:** 45 min | **Modalidad:** Individual

**Rol:** QA Lead — lanzamiento de una aplicación de **banca móvil**.

---

## Paso 1 · Definición de la Estrategia de Pruebas

Se adopta un **enfoque de tres capas complementarias** (caja negra + caja blanca + híbrido de integración) para lograr una cobertura robusta que verifique el *qué*, el *cómo interno* y el *entre-sistemas* del producto bancario.

### 1.1 Caja Negra para Validación de Interfaces

Se evaluarán los módulos funcionales de mayor exposición al usuario final:

- **Transferencias** (nacionales e inmediatas).
- **Pagos** de servicios y cuentas.
- **Recargas** de telefonía y tarjetas.
- **Gestión de tarjetas** (bloqueo/desbloqueo, límites, PIN).

Justificación por tipo de defecto detectado:

| Tipo de defecto | Cómo lo detecta la prueba de caja negra |
|---|---|
| **Validación de datos** | Entradas inválidas, vacías, límites (montos mínimos/máximos), formatos de RUT/cuenta y caracteres especiales rechazados o controlados. |
| **Flujo de usuario** | Navegación completa del flujo (transferir → confirmar → comprobante), estados intermedios y cancelaciones; sin depender del código interno. |
| **Reglas de negocio** | Restricciones como "monto máximo diario", "saldo insuficiente", "destinatario no propio", verificando que la interfaz refleja la regla correctamente. |
| **Usabilidad y consistencia** | Mensajes de error claros, terminología consistente, tiempos de carga aceptables y coherencia visual entre pantallas (estándares NFR‑USAB de la banca). |

**Fundamento:** la caja negra simula la perspectiva real del cliente y de la normativa de banca (exigencias del regulador sobre UX y transparencia), sin asumir cómo está construido el sistema.

### 1.2 Caja Blanca para Lógica Crítica

Procesos internos donde la **precisión es esencial**:

- **Cálculo de intereses** (diario, compuesto, días hábiles).
- **Validación de OTP** (match, expiración, reuso, anti fuerza bruta).
- **Cifrado** y derivación de claves (PBKDF2/Argon2, TLS 1.3).
- **Límites de transacción** (montos y frecuencias por perfil).

Técnicas estructurales aplicadas:

- **Pruebas de caminos independientes:** se diseña el grafo de flujo de cada función y se ejecuta cada camino linealmente independiente (base de ciclos), cubriendo ramas, bucles y condiciones.
- **Análisis de bucles:** se prueban bucles con 0, 1, *n*‑1, *n* y *n*+1 iteraciones para detectar desbordamientos, iteraciones fantasmas y termines no controladas.
- **Cobertura de decisiones y condiciones:** se evalúa cada decisión (if/switch) en sus ramas verdadero/falso y cada condición compuesta con variación de componente (MC/DC recomendado para lógica de seguridad).

**Filosofía de prevención:** estas técnicas permiten detectar **fallos lógicos** (fórmulas mal implementadas), **desbordamientos** (montos/expiración de OTP que exceden rangos) y **vulnerabilidades** (comparaciones inseguras, errores en la lógica de cifrado) antes de que lleguen a producción.

### 1.3 Enfoque Híbrido para Integración

Se combinan técnicas estructurales (verificar *cómo* se intercambia la información en el código) con funcionales (verificar *qué* recibe el usuario final) para validar:

- **Comunicación app móvil ↔ backend:** contratos de API (schema, versionado, serialización) probados con pruebas funcionales de endpoints más pruebas estructurales del middleware.
- **Manejo de errores en API:** códigos HTTP correctos, mensajes sin fuga de información, reintentos/backoff, y handling estructural de excepciones controladas.
- **Sincronización de estados:** transacciones concurrentes (doble envío, saldo en disputa) verificadas tanto end‑to‑end (negro) como a nivel de atomicidad de la lógica (blanco).
- **Integridad de datos en tránsito:** verificaciones de cifrado TLS y de checksum/integridad de payloads, combinando pruebas de penetración ligeras (negro) con inspección del flujo de datos (blanco).

**Fundamento:** en banca móvil ningún defecto es solo "funcional" o solo "estructural"; el enfoque híbrido garantiza que lo que el código garantiza internamente sea lo que el usuario percibe externamente.

---

## Paso 2 · Evaluación de Riesgos y Seguridad

### 2.1 Identificación de Módulos Críticos (Complejidad Ciclomática V(G) > 20)

Se realiza un análisis estático (herramienta de métricas de complejidad) para identificar componentes con **V(G) > 20**, típicamente:

- Motor de **cálculo de intereses** y comisiones.
- Orquestador de **transferencias** (validación + límites + antifraude + notificación).
- Lógica de **autenticación y OTP** (multi condición).
- Gestión de **tarjetas** con reglas cruzadas de estado.

Justificación de tratamiento especial para estos módulos:

| Acción requerida | Razón |
|---|---|
| **Mayor profundidad de pruebas** | Alta V(G) implica muchos caminos posibles; cada ruta mal probada es un defecto probable en producción. |
| **Revisión de código** | La complejidad exige revisión por pares y refactorización para reducir V(G). |
| **Pruebas negativas y de estrés** | Las muchas ramas deben cubrirse también con entradas inválidas y carga máxima concurrente. |
| **Priorización en el cronograma** | Se ejecutan primero y con mayor tiempo asignado (ver cronograma basado en riesgos). |

### 2.2 Seguridad de Datos y Análisis de Flujo de Datos

Estrategia de **Análisis de Flujo de Datos (DFA)** sobre las variables y recursos que transportan información sensible, garantizando:

- **Credenciales no en texto plano:** uso obligatorio de hash (bcrypt/Argon2) con salt; prohibición de variables de entorno con secretos en el repositorio.
- **Sin filtraciones en logs, variables temporales o excepciones:** políticas de logging que enmascaran datos sensibles; control de que ninguna excepción exponga credenciales, tokens o saldos en stack traces.
- **Sesiones correctamente cifradas:** transporte por TLS 1.3, cifrado de cookies de sesión y de almacenamiento local de tokens.
- **Invalidación adecuada de tokens:** revocación al cierre de sesión, expiración de JWT corta, rotación de refresh tokens y revocación forzada ante cambio de contraseña.

**Escenarios de ataque considerados (sin convertir la actividad en pentesting):**
- Replay de una solicitud de transferencia capturada (se valida que el idempotency‑key y el nonce lo bloqueen).
- Manipulación del token en el dispositivo (se valida la firma y la expiración en el backend).
- Lectura de logs/errores del dispositivo por un tercero (se valida el enmascaramiento).
- Extracción de variables temporales en memoria (se valida que los secretos no se mantienen más tiempo del necesario).

---

## Paso 3 · Selección de Herramientas y Métricas

### 3.1 Herramienta de Gestión de Pruebas seleccionada: **Jira + Zephyr**

| Criterio | Cómo lo mejora |
|---|---|
| **Trazabilidad** | Los casos se vinculan a historias/requisitos y a defectos; cada ejecución queda ligada a su requerimiento y módulo (matriz de trazabilidad automática). |
| **Reutilización** | Agrupación de casos en librerías por módulo (transferencias, pagos); los casos se clonan y versionan para regresiones. |
| **Auditoría y cumplimiento normativo** | Historial completo, trabajores de evidencia, permisos y reportes exportables que sustentan exigencias del regulador (SBIF/CMF) de control y trazabilidad. |

*Alternativas válidas equivalentes:* TestRail (API + reportes de cobertura) y Azure Test Plans (integración con CI/CD).

### 3.2 Métricas de Éxito del Plan

Indicadores cuantitativos definidos:

| Métrica | Objetivo | Relevancia bancaria |
|---|---|---|
| **Confiabilidad** | ≥ 95% de casos críticos aprobados | Un fallo en banca genera riesgo reputacional, regulatorio y financiero; la confiabilidad mide estabilidad operativa. |
| **Reducción de tiempo de ejecución por automatización** | ≥ 40% del tiempo manual ahorrado | Equipos con recursos acotados; la automatización libera foco para pruebas exploratorias y de riesgo. |
| **Cobertura de requisitos** | ≥ 90% de los requisitos con caso de prueba vinculado | El regulador exige justificar qué se probó; cobertura < 90% deja módulos sin evidencia. |
| **Defectos críticos detectados antes de producción** | ≥ 98% | En banca el costo de un defecto en producción se multiplica hasta 10x (corrección, multas regulatorias, compensación de clientes). |

---

## Entregable: Plan de Pruebas Estratégico

### A. Matriz de Trazabilidad (requisito ↔ caso de prueba ↔ riesgo ↔ módulo)

| Requisito / Código | Caso de prueba | Riesgo asociado | Módulo afectado |
|---|---|---|---|
| Transferencia inmediata (RF‑TRA‑01) | CP‑TRA‑05: monto máximo diario | Riesgo alto (fraude, saldo) | Transferencias |
| Límites por perfil (RF‑TRA‑03) | CP‑TRA‑07: límites excedidos (negativo) | Riesgo alto | Transferencias |
| Validación OTP (RF‑AUT‑02) | CP‑AUT‑04: OTP vencido/reusado | Riesgo alto (suplantación) | Autenticación |
| Cálculo de intereses (RF‑CRE‑02) | CP‑CRE‑03: interés compuesto exacto | Riesgo crítico (pérdida monetaria) | Motor de intereses |
| Pago de servicios (RF‑PAG‑01) | CP‑PAG‑02: pago exitoso y fallido | Riesgo medio | Pagos |
| Recarga (RF‑REC‑01) | CP‑REC‑01: recarga y notificación | Riesgo medio | Recargas |
| Bloqueo de tarjeta (RF‑TAR‑04) | CP‑TAR‑06: bloqueo/desbloqueo | Riesgo alto (fraude) | Gestión de tarjetas |
| Cifrado en tránsito (NFR‑SEG‑03) | CP‑INT‑01: integridad TLS | Riesgo alto (interceptación) | Integración app↔backend |

### B. Cronograma de Ejecución Basado en Riesgos

Priorización según **impacto × probabilidad × complejidad (V(G))**. Los módulos con mayor puntaje de riesgo y complejidad se ejecutan primero y con más tiempo.

| Semana | Etapa | Módulos priorizados | Justificación |
|---|---|---|---|
| 1 | Diseño y revisión | Análisis de riesgos, V(G), selección de casos | Base para todo el plan |
| 2 | Caja blanca | Motor de intereses, autenticación/OTP | V(G) > 20, impacto monetario/seguridad |
| 3 | Caja negra crítica | Transferencias, tarjetas (límites, bloqueo) | Escenario"alto impacto × alta probabilidad" |
| 4 | Híbrido integración | API app↔backend, sincronización de estados | Fallas entre capas, datos en tránsito |
| 5 | No funcional y estrés | Pagos, recargas, carga concurrente | Validación de disponibilidad y rendimiento |
| 6 | Regresión asistida por automatización | Casos reutilizables de todos los módulos | Verificación de mantenibilidad en el tiempo |

### C. Protocolo de Mantenimiento del Plan

Procedimiento para mantener los casos actualizados ante cambios regulatorios, funcionales o de arquitectura:

1. **Detección del cambio (trigger):** cualquier cambio en requisitos (product owner), normativa (equipo de cumplimiento/legal) o arquitectura (arquitectos) dispara una revisión del plan.
2. **Evaluación de impacto:** se determina si el cambio afecta casos existentes, crea requisitos nuevos o invalida criterios (análisis de impacto sobre la matriz de trazabilidad).
3. **Actualización de la matriz y casos:** se agregan, modifican o retiran casos en Jira + Zephyr, vinculando siempre al requisito y al riesgo.
4. **Re‑priorización del cronograma:** si el cambio eleva el riesgo de algún módulo, se reordena la ejecución según impacto × probabilidad.
5. **Revisión de métricas:** se recalibran cobertura y confiabilidad tras el cambio.
6. **Aprobación y trazabilidad:** todo cambio del plan se documenta y aprueba para sostener las auditorías del regulador.

---

## Reflexión final

El plan no se limita a "correr casos": **fundamenta cada decisión en riesgo, seguridad y trazabilidad**, y optimiza recursos al concentrar el esfuerzo donde el impacto y la complejidad son mayores. El ciclo de mantenimiento garantiza su **sostenibilidad en el tiempo** (cambios normativos, funcionales y de arquitectura), cerrando la visión integral de aseguramiento de calidad de la IL2.1.

## Recursos de apoyo

- PDF de la clase: `2.1.1 'PPT Estrategias y enfoques de diseño del plan de pruebas con enfoque en calidad y seguridad.pdf` (referencia de la sesión).
- Modelos previos de EA1 (actividades 1.1.2, 1.2.2, 1.3.2 y Clase 1).