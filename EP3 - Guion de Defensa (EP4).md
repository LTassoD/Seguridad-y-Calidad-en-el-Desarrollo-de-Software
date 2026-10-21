# Guion de Defensa — EP4

## Evaluación Parcial N.º 4 · ISY1102

### Sección 002V

Carrera: Ingeniería en Desarrollo de Software

Docente: Christian Rodrigo Alvarez Lobos

Fecha: 17 de octubre de 2026

**Integrantes:**

Luis Tasso

Miguel Arredondo

Nicolas Iturrieta

<!-- pagebreak -->

## 1. Estructura y distribución del tiempo

La defensa tiene 10 minutos de exposición y 5 minutos de preguntas. La exposición es individual, aunque el trabajo sea grupal: cada integrante debe dominar el contenido completo.

| N.º | Diapositiva | Inicio | Fin | Duración |
|---|---|---|---|---|
| 1 | Portada y saludo | 0:00 | 0:30 | 30 s |
| 2 | Contenido | 0:30 | 0:50 | 20 s |
| 3 | Contexto y alcance | 0:50 | 1:40 | 50 s |
| 4 | Enfoque estratégico | 1:40 | 2:40 | 60 s |
| 5 | Tipos de prueba | 2:40 | 3:20 | 40 s |
| 6 | Herramientas | 3:20 | 4:10 | 50 s |
| 7 | Resumen de ejecución | 4:10 | 5:00 | 50 s |
| 8 | Casos representativos | 5:00 | 5:50 | 50 s |
| 9 | Análisis estático | 5:50 | 6:40 | 50 s |
| 10 | Clasificación de defectos | 6:40 | 7:30 | 50 s |
| 11 | Evidencias | 7:30 | 8:00 | 30 s |
| 12 | Reflexiones | 8:00 | 9:00 | 60 s |
| 13 | Dictamen y acciones | 9:00 | 9:40 | 40 s |
| 14 | Cierre | 9:40 | 10:00 | 20 s |

## 2. Guion diapositiva por diapositiva

### Diapositiva 1 · Portada (0:00–0:30)

**Mensaje clave:** presentar al equipo, el caso y adelantar el dictamen.

> Buenos días. Somos Luis Tasso, Miguel Arredondo y Nicolas Iturrieta. Presentamos la verificación de seguridad y calidad del sistema Atlas, desarrollada para la Evaluación Parcial N.º 3. Anticipo la conclusión: el dictamen es NO CERTIFICADO, porque encontramos cuatro defectos críticos de seguridad que impiden su puesta en producción. A continuación explico el enfoque, la ejecución y la evidencia.

### Diapositiva 2 · Contenido (0:30–0:50)

**Mensaje clave:** ordenar la exposición.

> La presentación sigue el orden exigido: contexto y alcance, enfoque estratégico de las pruebas, tipos y herramientas, resultados de ejecución, análisis estático, clasificación de los defectos, reflexiones de calidad, seguridad y normativa, y finalmente el dictamen con las acciones correctivas.

### Diapositiva 3 · Contexto y alcance (0:50–1:40)

**Mensaje clave:** qué es Atlas, qué módulos se evaluaron y con qué marco.

> Atlas es una plataforma web para pymes chilenas que gestiona clientes, contratos y documentos. Tiene arquitectura de tres capas: frontend React con Material UI, API REST en Express/Node y PostgreSQL. Evaluamos seis módulos: autenticación, clientes, contratos y documentos, usuarios y roles, métricas y auditoría.
>
> Nos guiamos por ISO/IEC 25010 para calidad, ISO/IEC 27001 y OWASP Top 10 para seguridad, y la Ley 19.628 y 21.719 de protección de datos. El objetivo era determinar con evidencia si el software es apto para producción. Todo se ejecutó sobre un despliegue Docker en laboratorio: frontend en el puerto 3350, API en 4450 y PostgreSQL en 15432.

### Diapositiva 4 · Enfoque estratégico (1:40–2:40)

**Mensaje clave:** cómo se planificó y priorizó el ciclo de pruebas.

> Aplicamos un enfoque mixto: ejecución manual reproducible con curl, análisis estático automatizado y revisión manual del código. La priorización fue por riesgo: primero seguridad —control de acceso, subida de archivos e inyección—, luego la funcionalidad central y al final lo no funcional.
>
> Trabajamos en dos ciclos: el Ciclo 1 fue un smoke test de funciones base; si fallaba, deteníamos la ejecución. El Ciclo 2 ejecutó 12 casos funcionales y de seguridad más pruebas complementarias. Los criterios de entrada exigían entorno desplegado, datos semilla y casos revisados; los de salida, el 100 % de los casos críticos ejecutados, sin defectos críticos abiertos y con evidencia registrada.

### Diapositiva 5 · Tipos de prueba (2:40–3:20)

**Mensaje clave:** cada tipo responde a un requisito del ERS.

> Diseñamos cinco tipos de prueba, cada uno justificado por el ERS. Funcionales para validar los requisitos RF-1 a RF-6: login, CRUD de clientes, contratos, usuarios, dashboard y auditoría. De seguridad para control de acceso, uploads, SQLi, CORS y fuerza bruta. De integración para verificar el flujo completo entre frontend, API y base de datos. De rendimiento para comparar los tiempos de respuesta con los umbrales NFR-PERF. Y de usabilidad, en una revisión acotada de los estados de interfaz.

### Diapositiva 6 · Herramientas (3:20–4:10)

**Mensaje clave:** justificar la elección de cada herramienta.

> Elegimos cada herramienta por su aporte a la evidencia. Docker Compose reproduce el ambiente completo de forma aislada y verificable. curl nos permite controlar token, cabeceras y payloads, y registrar el código HTTP como prueba. ESLint detecta errores y malas prácticas de calidad de forma automática. SonarQube entrega métricas objetivas de bugs, vulnerabilidades, hotspots y duplicación. Y la revisión manual cubre lo que las herramientas no ven: control de acceso, secretos y manejo de archivos. El equipo de prueba fue un líder de QA, un tester funcional y un tester de seguridad, sobre un entorno QA local con datos ficticios.

### Diapositiva 7 · Resumen de ejecución (4:10–5:00)

**Mensaje clave:** resultados cuantitativos del ciclo.

> Diseñamos y ejecutamos 12 casos: 10 aprobados, un 83 % de éxito, y 2 fallidos. Los fallos son CP-010, que aceptó un archivo ejecutable en la subida de documentos, y CP-011, que permitió leer datos de contratos sin token. Sumamos 10 pruebas de seguridad complementarias, de las cuales 7 arrojaron resultado inseguro. En total registramos 11 incidentes: 4 críticos, 5 graves, 1 moderado y 1 leve. ESLint reportó 14 problemas y SonarQube, 1 vulnerabilidad BLOCKER, 4 hotspots y 198 code smells. El tiempo de respuesta fue de 4 segundos por una latencia artificial en el código.

### Diapositiva 8 · Casos representativos (5:00–5:50)

**Mensaje clave:** conectar cada caso con su evidencia.

> Estos son los casos que mejor resumen el resultado. CP-001 aprobó: el login válido emite el JWT. CP-010 falló: el sistema aceptó un archivo .exe y lo sirvió como PDF, lo que es un riesgo de malware. CP-011 falló: un GET a contratos sin token devolvió los datos completos, un IDOR clásico. CP-012 sí aprobó: el intento de inyección SQL fue rechazado con 401 porque las consultas están parametrizadas. SEG-12 mostró CORS abierto con Allow-Origin asterisco, y FN-02 midió 4,06 segundos frente a un umbral de 300 milisegundos.

### Diapositiva 9 · Análisis estático (5:50–6:40)

**Mensaje clave:** la herramienta confirma los hallazgos dinámicos.

> El análisis estático confirma lo que vimos dinámicamente. ESLint detectó 14 problemas, principalmente variables e imports sin uso y dependencias de hooks. SonarQube, en el backend, encontró una vulnerabilidad BLOCKER: la contraseña de PostgreSQL escrita directamente en db.js, línea 6. Además, 4 security hotspots y un Security Rating E. En el frontend encontró 1 bug, 181 code smells y un problema crítico de complejidad cognitiva. Lo relevante es que los hotspots coinciden exactamente con los defectos BUG-003, de subida de archivos, y BUG-005, de CORS.

### Diapositiva 10 · Clasificación de defectos (6:40–7:30)

**Mensaje clave:** escala aplicada y regla de certificación.

> Clasificamos los 11 incidentes con una escala de cuatro niveles. CRITICO: 4 casos, que impiden operar o exponen datos sensibles —el acceso sin token, las credenciales en texto claro, la subida sin validación y el secreto en el código—. GRAVE: 5 casos, entre ellos el JWT_SECRET inseguro, el CORS abierto, la ausencia de rate-limit, los errores 500 y el uso de localStorage. MODERADO: la latencia artificial. Y LEVE: los code smells de ESLint. La regla que aplicamos es que un software con defectos CRITICO abiertos nunca debe certificarse.

### Diapositiva 11 · Evidencias (7:30–8:00)

**Mensaje clave:** mostrar que todo es verificable.

> Aquí están las capturas del servidor SonarQube local. Se ven los dashboards de ambos proyectos, los issues de code smells y del frontend, el Quality Gate y el resumen de proyectos. Todas las capturas están incorporadas también en el Anexo E del informe, para que la evidencia sea verificable.

### Diapositiva 12 · Reflexiones (8:00–9:00)

**Mensaje clave:** calidad, seguridad, normativa, legal y ética.

> En calidad, el sistema tiene una base funcional correcta, pero una deuda técnica alta en el frontend y un bug de compatibilidad con React 19. En seguridad, los cuatro defectos críticos se mapean a OWASP: control de acceso roto, fallas criptográficas, fallas de autenticación y de integridad de datos y software.
>
> En lo normativo, la exposición de datos personales y el manejo de contraseñas incumplen la Ley 19.628 y la 21.719, y los controles de acceso y criptografía de ISO 27001. En lo legal, los datos de clientes no pueden quedar accesibles sin autorización. Y en lo ético, nuestro compromiso fue reportar todo con transparencia y evidencia, sin ocultar hallazgos y sin usar datos reales.

### Diapositiva 13 · Dictamen (9:00–9:40)

**Mensaje clave:** criterio, resultado y acciones.

> El criterio de certificación era tener el 100 % de los casos de seguridad críticos exitosos y ningún defecto crítico abierto. No se cumplió: fallaron CP-010 y CP-011 y quedan 4 incidentes CRITICO. Por eso el dictamen es NO CERTIFICADO. Las acciones correctivas prioritarias son: autenticación global en todos los endpoints, hash seguro de contraseñas, validación de archivos, secretos fuera del código, CORS restringido, rate-limit, transacciones y errores genéricos, cookies httpOnly y un Quality Gate de seguridad en CI.

### Diapositiva 14 · Cierre (9:40–10:00)

**Mensaje clave:** cerrar y ofrecer respaldo.

> Con esto cerramos la presentación. El informe completo, con el detalle de cada caso y las evidencias, está disponible como respaldo. Quedamos atentos a sus preguntas.

## 3. Recomendaciones para la defensa

- **Ritmo:** ensayar al menos dos veces con cronómetro; si se pasa de 10 minutos, recortar las diapositivas 5 y 11, que son de apoyo.
- **No leer:** las notas del orador están en el PPTX (vista Notas); úsalas como guía, no como texto literal.
- **Dominio individual:** la defensa es personal; cada integrante debe poder explicar cualquier sección, especialmente el dictamen y los defectos críticos.
- **Respaldo:** tener abiertos el informe EP3 y el Anexo E con las capturas para responder consultas técnicas.
- **Preguntas probables:** por qué NO CERTIFICADO, por qué SonarQube da Quality Gate OK si hay una vulnerabilidad BLOCKER, diferencia entre IDOR y autenticación faltante, y qué corregir primero.
- **Entrega AVA:** subir el informe (Word/PDF), la presentación y el material de apoyo antes del plazo de la evaluación.

---

*Documento de apoyo para la defensa individual de la Evaluación Parcial N.º 4 (EP4). Complementa el informe EP3 y la presentación `EP3_Presentacion_Atlas.pptx`.*
