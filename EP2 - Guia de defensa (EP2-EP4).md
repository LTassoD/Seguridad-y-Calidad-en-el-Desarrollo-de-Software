# Guía de Defensa — EP3 y EP4 · Verificando la calidad

**Objetivo:** preparar la defensa grupal (EP3 12% · Encargo+defensa) y la presentación/defensa (EP4 28%) sobre la **verificación de la calidad del caso semestral Atlas**.

---

## 1. Narrativa en 3 minutos (resumen para abrir la defensa)

> "Ejecutamos el ciclo de verificación del sistema **Atlas** en un laboratorio real levantado con Docker (frontend :3350, API :4450, PostgreSQL :15432). Aplicamos dos pasadas: un **smoke test** que validó la base (login, estado de API, Swagger) y un **ciclo de casos** funcionales y de seguridad. Complementamos con **análisis estático** (ESLint en frontend y backend + revisión manual del código fuente). El resultado: **12 casos ejecutados, 10 aprobados, 2 fallidos, 10 defectos registrados** con 3 de severidad **crítica** (acceso sin autenticación a datos, credenciales en texto claro, subida de archivos sin validar). El dictamen es **NO CERTIFICADO** y proponemos un ciclo de corrección con acciones concretas."

---

## 2. Preguntas probables y respuestas con evidencia

### Calidad y pruebas
**Q: ¿Qué casos de prueba diseñaron y por qué esa técnica?**
R: 12 casos (CP-001..012), 4 de smoke y 8 de detalle. Seguimos las técnicas del módulo 2.2: casos funcionales (login, CRUD clientes, contratos, métricas) y casos de **seguridad** orientados a requisitos (control de acceso RQ-11, subida de documentos RQ-10, resistencia SQLi RQ-12).

**Q: ¿Cómo prepararon el entorno?**
R: Con Docker Compose (`docker compose up -d --build`), 3 contenedores. Verificamos que postgres quedara *healthy* antes de probar, que el frontend respondiera 200 y que la API devolviera `{"name":"Atlas","status":"ok"}`. Ejecutamos vía **curl** contra la API y usamos el navegador para el frontend.

**Q: ¿Cómo ejecutaron la bitácora en ciclos?**
R: Siguiendo la actividad 2.3.2: **Ciclo 1 · Smoke** (login, salud API, Swagger) y **Ciclo 2 · Casos** (funcionales + seguridad). Por cada caso registramos: estado (Aprueba/Falla/Bloqueado), defecto asociado y observación.

**Q: ¿Qué es un smoke test y por qué se separa?**
R: Verifica que las funciones base (login, carga) operen antes de probar el resto; si falla, la ejecución se **bloquea** porque no se puede probar el sistema completo.

### Seguridad
**Q: ¿Qué vulnerabilidad encontraron? Descríbanla y demuestrenla.**
R: La principal es **falta de control de acceso** (BUG-001). Ejemplo: `GET /contratos/1` **sin token** devuelve HTTP 200 con los datos del contrato. Esperábamos 401. Es un **IDOR / broken access control** (OWASP A01). También `GET /auditoria`, `GET /usuarios/1` y `GET /roles` sin token responden 200.

**Q: ¿Cómo explican la subida de archivos sin validar?**
R: El backend usa `multer({ storage })` **sin filtro** de archivos (contracts.js:29). Enviamos un `.exe` y un `.html` con un script y ambos fueron aceptados (201) y guardados como bytea. Además, al descargarlos (`GET /contratos/5/file`) los sirve con `Content-Type: application/pdf` aunque el contenido es un ejecutable. Es un **upload de archivos no restringido** (OWASP A08).

**Q: ¿Por qué las credenciales en texto claro son críticas?**
R: En `auth.js:26` se compara `user.contrasena_hash !== password` directo, y el seed de BD trae `admin/admin` y `editor/editor`. Si alguien accede a la BD o al código, obtiene credenciales válidas sin ningún esfuerzo. Debe usarse **hash (bcrypt/argon2)** y borrar las cuentas por defecto.

**Q: ¿Intentaron SQL injection?**
R: Sí. Enviamos `admin' OR '1'='1` en el usuario del login y el sistema lo **rechazó (401)** porque todas las consultas usan parámetros (`$1..$n`) de node-postgres. Ese riesgo está **mitigado** en las rutas revisadas. Lo registramos como riesgo mitigado en el informe.

**Q: ¿Qué otros controles de seguridad revisaron?**
R: CORS (está abierto `Access-Control-Allow-Origin: *`), rate-limit en login (no existe; solo una espera fija de 4 s que amortigua), exposición de detalles internos en errores 500 (campo `glosa` filtra mensajes de PostgreSQL), y almacenamiento del token en `localStorage`.

### Análisis estático
**Q: ¿Qué herramienta usaron y qué encontraron?**
R: **ESLint 9** (el frontend ya lo traía configurado; lo agregamos para el backend). Frontend: **11 issues** en 7 archivos — 8 errores `no-unused-vars` y 2 warnings `react-hooks/exhaustive-deps`. Backend: 3 imports sin usar (`path`, `fs`, `pool`). No son vulnerabilidades, son **code smells** de mantenibilidad (calidad).

**Q: ¿Por qué el análisis estático es "estático"?**
R: Porque inspecciona el **código fuente sin ejecutarlo**, detectando bugs, code smells y vulnerabilidades en etapas tempranas — corregirlos ahí es hasta **100× más barato** que en producción (PPT 2.3.1).

### Informe de certificación
**Q: ¿Cuál es su dictamen y por qué?**
R: **NO CERTIFICADO.** El criterio de aceptación era 100% de casos de seguridad críticos exitosos y cero defectos críticos abiertos. Tenemos BUG-001, BUG-002 y BUG-003 críticos y 2 casos fallidos (CP-010, CP-011). Un software con críticos abiertos **nunca se certifica**.

**Q: ¿Cómo construyeron la matriz de trazabilidad?**
R: 12 requisitos (RQ-01..12), cada uno con su caso de prueba y su resultado, mapeados a defectos cuando falló. Es el anexo que demuestra que **cada requisito del cliente tiene un caso asociado y un resultado**.

**Q: ¿Qué riesgos quedaron aceptados vs mitigados?**
R: Mitigados: SQLi (parametrización) y enumeración de usuarios (login 401 genérico). Aceptados: latencia artificial de 4 s (diseño del caso), `localStorage` y ausencia de TLS en laboratorio.

**Q: ¿Cuáles son sus recomendaciones priorizadas?**
R: (1) middleware de autenticación global, (2) hash de contraseñas + quitar credenciales default, (3) validar archivos en multer (solo PDF, límite de tamaño), (4) `JWT_SECRET` seguro obligatorio, (5) CORS restringido, (6) rate-limit en login, (7) no exponer `glosa`, (8) corregir code smells.

---

## 3. Estructura propuesta para la presentación (EP4 · ~10-15 min)

| # | Sección | Min | Contenido clave |
|---|---|---|---|
| 1 | Portada + contexto | 1 | Proyecto, alcance, equipo, objetivo de la certificación |
| 2 | Entorno y metodología | 2 | Docker, ciclos 1 y 2, herramientas (curl, ESLint) |
| 3 | Ejecución y bitácora | 3 | Tabla CP-001..012, resultados (10/12 pass) |
| 4 | Hallazgos de seguridad | 4 | Demo/live o capturas: IDOR sin token, upload .exe, texto claro (BUG-001..003) |
| 5 | Análisis estático | 2 | Issues ESLint frontend/backend + hallazgos manuales |
| 6 | Dictamen + riesgos | 2 | NO CERTIFICADO, criterio de aceptación, riesgos mitigados/aceptados |
| 7 | Recomendaciones + cierre | 2 | 8 acciones correctivas + seguimiento |

> Consejo: durante la defensa **muestra una prueba real** (un `curl` sin token → 200) en vez de solo leer la tabla. Imagen de respaldo en pantalla si el live falla.

---

## 4. Respuestas rápidas para "exámenes cortos" del docente

| Concepto | Respuesta |
|---|---|
| Prueba estática vs dinámica | Estática: analiza el código sin ejecutarlo (revisión, ESLint, SonarQube). Dinámica: ejecuta el software (pruebas de API, funcionales). |
| Severidad de defectos | Crítica (bloquea negocio), Mayor, Menor, Cosmética. |
| Cuándo no certificar | Con defectos críticos abiertos. |
| IDOR | Object reference directo a recurso sin verificar autorización → acceso a datos ajenos. |
| Mitigación de SQLi | Consultas parametrizadas (prepared statements). |
| CORS `*` | Cualquier sitio web puede llamar a la API desde el navegador. |
| Por qué token en localStorage es malo | Accesible por XSS; mejor cookie `httpOnly`. |

---

*Documento de apoyo para la defensa. Complementa el informe `EP3 - Informe de Certificacion - Atlas.md` y su DOCX.*