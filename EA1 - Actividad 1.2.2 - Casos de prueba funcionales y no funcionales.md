# Actividad 1.2.2 · Casos de prueba para evaluar requisitos funcionales y no funcionales

**Sigla:** ISY1102 · **Asignatura:** Seguridad y calidad en el desarrollo de Software · **EA1**
**Tiempo:** 45 minutos · **Modalidad:** Individual · **Indicador de Logro:** IL1.2

**Objetivo:** Distingue las diferencias entre pruebas funcionales y no funcionales, analizando su relevancia en el aseguramiento de la calidad del software e integrando los criterios legales y normativos que sustentan su aplicación.

---

## I. Comprensión lectora: definición de pruebas funcionales

**1. El objetivo principal de una prueba funcional es:**

- [ ] Medir el tiempo de respuesta del sistema bajo carga máxima.
- [x] **Verificar si cada característica y acción del software cumple con los requisitos y especificaciones definidos por el cliente.**
- [ ] Evaluar la facilidad con la que el usuario promedio puede operar la interfaz.
- [ ] Determinar la robustez del sistema frente a fallos de hardware.

> La prueba funcional responde al *¿qué hace?* el software. Verifica que cada funcionalidad opere según lo especificado. Medir tiempos (carga) y robustez frente a fallos es no funcional; la usabilidad se evalúa con pruebas no funcionales.

**2. Una prueba de rendimiento (Performance Testing) tiene como propósito principal:**

- [ ] Comprobar si un botón realiza correctamente la acción de "Guardar".
- [x] **Evaluar atributos de calidad como la velocidad, escalabilidad y estabilidad del sistema.**
- [ ] Asegurar que los datos introducidos cumplen con las reglas de negocio.
- [ ] Verificar la correcta integración entre dos módulos distintos.

> El rendimiento es una prueba no funcional: mide *¿cómo* lo hace?* el sistema (tiempos de respuesta, procesamiento, estabilidad). Verificar un botón o reglas de negocio es funcional; la integración entre módulos es una prueba funcional de integración.

**3. ¿Cuál de los siguientes es un ejemplo de un caso de prueba puramente funcional?**

- [ ] El sistema debe cargar la página principal en menos de 2 segundos.
- [x] **Al ingresar credenciales válidas y hacer clic en "Iniciar Sesión", el usuario es redirigido al Dashboard.**
- [ ] La aplicación debe soportar 1,000 usuarios concurrentes sin degradación.
- [ ] El código fuente debe ser fácil de mantener y modificar.

> El flujo "login → Dashboard" valida una acción funcional esperada. Cargar en <2 s y soportar 1,000 usuarios concurrentes son no funcionales (rendimiento/carga); la mantenibilidad del código es una característica no funcional de ISO 25010.

---

## II. Clasificación (Funcional vs No funcional)

| Requisito para verificar | Clasificación (F / NF) |
|---|---|
| 1. Comprobar que el campo de contraseña en el registro solo acepta caracteres alfanuméricos. | **F** (valida una regla de negocio/entrada del sistema, el *qué*) |
| 2. Verificar que la aplicación sea utilizable por personas con discapacidad visual (Accesibilidad). | **NF** (usabilidad) |
| 3. Medir el uso de memoria RAM por el servidor bajo un volumen de datos elevado. | **NF** (rendimiento / uso de recursos) |
| 4. Asegurar que el cálculo de impuestos es matemáticamente correcto. | **F** (valida un proceso/regla de negocio, el *qué*) |
| 5. Probar que el sistema puede ser instalado correctamente en Windows y Linux. | **NF** (portabilidad / instalabilidad) |
| 6. Validar que el link "Contáctenos" lleva a la página de soporte. | **F** (valida una acción/navegación funcional esperada) |

---

## III. Análisis de escenarios

**1. Explique la principal diferencia en el foco de validación entre una prueba funcional y una prueba no funcional de seguridad.**

> La prueba **funcional** valida el **qué**: que el control de seguridad *haga lo que debe*, por ejemplo que al ingresar una contraseña incorrecta se deniegue el acceso, que un usuario sin permisos no pueda ejecutar una acción o que la autenticación multifactor funcione correctamente. Verifica el comportamiento esperado de la función de seguridad.
>
> La prueba **no funcional** de seguridad valida el **cómo**: la robustez y resistencia del sistema frente a amenazas y vulnerabilidades, como escaneo de vulnerabilidades (inyección SQL, XSS), cifrado de datos, protección contra accesos no autorizados y cumplimiento de confidencialidad, integridad y disponibilidad. Mide la *fortaleza* del sistema ante ataques, no solo que el control responda.

**2. Escenario:** Un equipo de QA reporta que todas las pruebas funcionales han pasado con éxito. Sin embargo, al liberar el producto, los usuarios se quejan de que el sistema se congela cuando 50 o más personas intentan usarlo a la vez.

**A. ¿Qué tipo de prueba no funcional fue omitida o falló?**

> Fue omitida o falló la **prueba de carga/rendimiento (performance y load testing)**, específicamente la evaluación de **escalabilidad y capacidad** bajo un número específico de usuarios concurrentes. Simular 50+ usuarios simultáneos habría detectado la degradación del sistema (aumento de tiempos de respuesta, saturación de recursos) antes de la liberación.

**B. ¿Por qué es un error común depender solo del éxito de las pruebas funcionales?**

> Porque las pruebas funcionales solo confirman que el software **hace lo que debe** (el *qué*), pero no que lo haga **bien, rápido y seguro** (el *cómo*). Un software puede ser funcionalmente correcto pero inutilizable si es lento, se congela o no escala, tal como indica el material: *"un software puede ser funcionalmente correcto, pero inutilizable si es lento o inseguro"*. Depender solo de pruebas funcionales genera una falsa sensación de calidad y deja sin validar los atributos no funcionales (rendimiento, estabilidad) que afectan directamente la experiencia y confianza del usuario final.

---

## IV. Reflexión final

**Mencione una ventaja clave de priorizar las pruebas funcionales al comienzo del ciclo de vida y una ventaja de programar las pruebas no funcionales de rendimiento hacia las fases finales.**

> **Ventaja de priorizar las pruebas funcionales al inicio del SDLC:** permiten validar tempranamente que el software cumple los requisitos y reglas de negocio, detectando y corrigiendo defectos funcionales de forma rápida y económica cuando el costo de corregirlos es menor. Además, una base funcional estable permite construir sobre ella las mediciones de rendimiento.
>
> **Ventaja de programar las pruebas no funcionales de rendimiento en las fases finales:** el sistema ya se encuentra en un estado cercano a producción y con los módulos integrados, por lo que las mediciones de tiempos de respuesta, carga y estabilidad reflejan el comportamiento real del producto final. También permite optimizar la infraestructura y configuración una vez que la funcionalidad está definida, validando el sistema completo en lugar de partes aisladas.

---

## Recursos de apoyo

- PPT Clase 1.2.1 "Pruebas funcionales y no funcionales": pruebas funcionales (unitarias, integración, sistema, aceptación) y no funcionales (rendimiento, carga, seguridad, usabilidad)
- Normas y regulaciones: ISO/IEC 25010, GDPR, Ley 19.628 (protección de datos, Chile)
- Herramientas: Selenium/JUnit/Cucumber/Postman (funcionales); JMeter, OWASP ZAP, New Relic/Datadog (no funcionales)
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
