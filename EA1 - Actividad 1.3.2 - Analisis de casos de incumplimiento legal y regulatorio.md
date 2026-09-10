# Actividad 1.3.2 · Análisis de casos de incumplimiento legal y regulatorio, repercusiones

**Sigla:** ISY1102 · **Asignatura:** Seguridad y calidad en el desarrollo de Software · **EA1**
**Tiempo:** 45 minutos · **Modalidad:** Individual · **Indicador de Logro:** IL1.3

**Objetivo:** Identifica pruebas de usabilidad, rendimiento y compatibilidad, reconociendo su impacto en la calidad, seguridad y conformidad normativa del software, y su aporte a la accesibilidad, confiabilidad y ética del producto final.

---

## I. Matriz de hallazgos

Completa la tabla identificando qué norma o ley se está incumpliendo en el escenario de HealthConnect.

| Situación detectada | Norma / Estándar afectado | Ley aplicable |
|---|---|---|
| **Falta de cifrado en el chat del médico** | ISO/IEC 27001 (Seguridad de la Información): compromete la **confidencialidad e integridad** de la comunicación entre paciente y médico | Ley 19.628 (Protección de Datos Personales) y Ley 21.719 (Protección de Datos Personales, GDPR chileno): exigen cifrado robusto y seguridad de datos de salud (datos sensibles) |
| **Uso de librería GPLv3 en software cerrado** | Leyes de **Propiedad Intelectual** (Derechos de Autor) y licencias de software (copyleft GPLv3) | Ley 19.628 no aplica aquí; se incumple la **licencia GPLv3**, que exige redistribuir el código bajo la misma licencia. Aplica legislación de propiedad intelectual / derechos de autor |
| **Falta de soporte para lectores de pantalla** | ISO/IEC 25010 → subcaracterística de **Usabilidad** (accesibilidad); estándar **WCAG** de accesibilidad web | Normativas chilenas de **inclusión digital** y accesibilidad; en el extranjero (p. ej., ADA en EE.UU.) puede constituir discriminación. ISO 25010 incluye "usabilidad accesible" |
| **Almacenamiento de datos sin política de borrado** | ISO/IEC 27001 (gestión de activos de información) | Ley 19.628 / Ley 21.719: se viola el principio de **Limitación del Plazo de Conservación** (no guardar los datos más tiempo del necesario y permitir su eliminación) |

---

## II. Evaluación de riesgos y mitigación

### Riesgo de Licenciamiento

**¿Qué consecuencias legales enfrentaría según el marco de Propiedad Intelectual?**

> Al usar una librería con licencia **GPLv3** (copyleft fuerte) y vender el software como **código cerrado (propietario)**, se infringe la licencia y los derechos de autor del autor original. Las consecuencias son:
> - **Infracción de derechos de autor:** el titular de la librería puede demandar por uso no autorizado.
> - **Pérdida del derecho a distribuir:** la GPLv3 obliga a que cualquier distribución del software que integra la librería se haga bajo GPLv3 y se entregue el **código fuente completo** de los componentes derivados. Al venderlo cerrado se viola esa obligación.
> - **Medidas judiciales:** cese y desistimiento, prohibición de distribución, **indemnización de daños** y posibles multas.
> - **Daño reputacional y de confianza** en el mercado (pérdida de contratos).

**¿Qué solución técnica o legal sugieres?**

> **Técnica / legal (opciones):**
> - **Reemplazar** la librería por una con licencia permisiva (MIT, Apache 2.0) o por software propio, manteniendo el modelo de código cerrado.
> - **Usar la librería como proceso separado (componente externo/servicio)**, sin incorporarla al código cerrado (si el licenciamiento y la arquitectura lo permiten).
> - **Cambiar el modelo de negocio** a **código abierto** bajo GPLv3, liberando el software bajo la misma licencia, si la estrategia comercial lo permite.
> - Consultar con el **área legal** y realizar una **auditoría de licencias** (compliance/SCA - Software Composition Analysis) antes de integrar librerías de terceros.

### Protección de Datos (datos de salud = datos sensibles)

**¿Cuáles son las 3 medidas mínimas que exige el GDPR / Ley 21.719 que NO se están cumpliendo actualmente?**

> 1. **Cifrado de los datos** (Integridad y Confidencialidad/Seguridad): los datos de salud deben procesarse con medidas de seguridad adecuadas. El chat sin cifrado de punto a punto y la falta de cifrado en el almacenamiento incumplen este requisito.
> 2. **Política clara de retención y eliminación** (Limitación del Plazo de Conservación): los datos no deben conservarse indefinidamente; debe definirse un plazo y un mecanismo de borrado, y permitir al titular ejercer sus derechos (supresión).
> 3. **Consentimiento explícito e informado del titular** (Licitud, Lealtad y Transparencia): tratándose de datos sensibles de salud, se requiere consentimiento explícito y específico, informando claramente la finalidad del tratamiento.

### Calidad del Producto (ISO/IEC 25010)

**¿Qué subcaracterística de calidad se ignora al no tener compatibilidad con lectores de pantalla y por qué podría generar una demanda por discriminación?**

> Se ignora la subcaracterística de **Usabilidad → "Accesibilidad"** (ISO/IEC 25010: la medida en que el producto puede ser usado por personas con el más amplio rango de características y capacidades, incluidas personas con discapacidad). Al no ser compatible con lectores de pantalla ni permitir ajustar tamaño de fuente, el software excluye a usuarios con discapacidad visual.
>
> Esto puede generar una demanda por **discriminación** porque se impide el acceso a un servicio esencial (salud) a un grupo de personas por su condición, vulnerando normativas de **accesibilidad e inclusión digital** y de no discriminación. En sistemas de salud, el derecho a acceder a la atención médica en igualdad de condiciones tiene respaldo legal y ético, por lo que la exclusión es considerada discriminatoria y sancionable.

---

## III. Propuesta de sello de calidad (Checklist pre-producción)

Lista de verificación de **5 puntos esenciales** que todo nuevo módulo de HealthConnect debe pasar antes de ir a producción para asegurar el cumplimiento del marco normativo legal:

- [ ] **1. Cifrado y seguridad de datos (confidencialidad/integridad):** verificar cifrado en tránsito (TLS) y en reposo, y cifrado punto a punto en el chat; validar que los accesos estén controlados y autenticados (cumplimiento Ley 21.719/19.628 e ISO 27001).
- [ ] **2. Cumplimiento de licencias de código de terceros:** auditar todas las librerías del módulo (SCA) y confirmar que sus licencias (MIT/Apache/GPL/etc.) son compatibles con el modelo de distribución del software.
- [ ] **3. Políticas de retención y borrado de datos:** definir plazos de conservación, mecanismos de eliminación y permisos de supresión, respetando los derechos del titular (limitación del plazo de conservación).
- [ ] **4. Accesibilidad e inclusión (usabilidad WCAG):** probar compatibilidad con lectores de pantalla, contraste, navegación por teclado y ajuste de tamaño de fuente, para garantizar acceso igualitario y evitar discriminación.
- [ ] **5. Consentimiento informado y trazabilidad (accountability):** verificar que se obtiene consentimiento explícito e informado para datos sensibles, y que quede **evidencia documentada y trazable** de cada requisito legal → caso de prueba → resultado para auditorías (ISO 25010 e ISO 27001).

---

## Recursos de apoyo

- PPT Clase 1.3.1 "Código con Ley: Auditoría de Calidad y Legalidad en el Software": auditoría de calidad vs legal, ISO 9001/25010/27001, Ley 19.628, Ley 21.180, CMF NCG 386/461, acceso/web WCAG
- Leyes chilenas: Ley 19.628 (protección de datos personales), Ley 21.719, Ley 21.180 (transformación digital)
- Estándares: ISO/IEC 25010 (usabilidad/accesibilidad), ISO/IEC 27001 (SGSI), licencias GPLv3/MIT
- OWASP / WCAG: https://www.w3.org/WAI/standards-guidelines/wcag/
