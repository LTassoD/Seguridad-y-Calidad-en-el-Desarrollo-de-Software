# EA2 · Guía 2.1.3 — Levantamiento de imágenes en Docker del caso semestral (Atlas)

**Asignatura:** ISY1102 · Seguridad y calidad en el desarrollo de software
**Guía:** 2.1.3 | **IL2.1** | **Tiempo:** 2 horas | **Modalidad:** Individual

**Caso semestral:** A — Sistema de Gestión Atlas (`CodigoFuenteA.zip`)

---

## Objetivo

Levantar y conocer el ambiente de entorno utilizado para el desarrollo del caso semestral, a fin de verificar la calidad, seguridad y cumplimiento legal y normativo en un software real.

## Prerrequisitos

- Docker instalado (descarga desde https://www.docker.com/).
- Código fuente del caso A (`CodigoFuenteA.zip`) descomprimido.
- Visual Studio Code (opcional; opcionalmente el levantamiento también es posible por terminal).

## Proceso de levantamiento (ejecutado)

### 1. Descomprimir el código fuente

Se extrajo `CodigoFuenteA.zip` en la carpeta de la asignatura:

```
Servicio/…/CodigoFuenteA/CodigoFuenteA/
```

### 2. Abrir la carpeta del proyecto

Se abrió la carpeta raíz del proyecto en Visual Studio Code mediante "Abrir Carpeta".

### 3. Reconocer la estructura de carpetas

```
CodigoFuenteA/
├── .env                  → variables de entorno para Docker (personalizables)
├── docker-compose.yml    → construcción de imágenes, variables y orquestación
├── README.md             → información descriptiva del proyecto
├── package.json
├── BACKEND/              → código fuente de la API (Express/Node.js) + SQL
└── FRONTEND/             → código fuente del cliente (React / Vite / Nginx)
```

### 4. Archivo `.env` (variables del caso Atlas)

```env
JWT_SECRET=0d1d8132f0fde5beabb417b434ff10f1cae8635a461686b0f46ac9c2bbfbd0e8
PORT_POSTGRES=15432
PORT_BACKEND=4450
PORT_FRONTEND=3350
COMPOSE_PROJECT_NAME=atlas
```

**Puertos configurados para el caso Atlas:**
- Frontend: `http://localhost:3350`
- API: `http://localhost:4450`
- PostgreSQL: `localhost:15432`

> Los puertos del caso Atlas difieren del ejemplo de la guía (3333/4444/15442); cada caso (A o B) define los suyos en el `.env`. El contenido de este archivo se revisa luego desde la perspectiva de seguridad (ej. el `JWT_SECRET` viene incluido en el repositorio).

### 5. Iniciar Docker

Se inició Docker Desktop y se esperó a que el engine estuviera disponible:

```
$ docker info --format '{{.ServerVersion}}'
29.5.2
```

### 6. Ejecutar el comando de levantamiento

Desde el directorio raíz del proyecto:

```bash
docker compose up -d --build
```

Salida (resumen):

```
Image atlas-atlas-backend Built
Image atlas-atlas-frontend Built
Network atlas-network Created
Volume atlas_postgres_data Created
Container atlas-postgres Created   → Started → Healthy
Container atlas-backend  Created   → Started
Container atlas-frontend Created   → Started
```

Se usó `--build` para construir las imágenes desde los `Dockerfile` de BACKEND y FRONTEND; sin cambio en el código, `docker compose up -d` reutiliza las imágenes ya construidas.

### 7. Verificar los contenedores (Docker → Containers)

```bash
$ docker ps
NAME              STATUS                  PORTS
atlas-frontend    Up                      0.0.0.0:3350->80/tcp
atlas-backend     Up                      0.0.0.0:4450->4000/tcp
atlas-postgres    Up (healthy)            0.0.0.0:15432->5432/tcp
```

Se crearon los **3 componentes** del caso Atlas: `atlas-postgres`, `atlas-backend` y `atlas-frontend`.

### 8. Verificar el cliente (frontend) en el navegador

Dirigirse a `http://localhost:3350`:

```bash
$ curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:3350/
HTTP 200
```

Aparece la plataforma del Sistema de Gestión Atlas (login).

### 9. Verificar la definición de la API (Swagger)

Dirigirse a `http://localhost:4450/docs`:

```bash
$ curl -sL -o /dev/null -w "HTTP %{http_code} -> %{url_effective}\n" http://localhost:4450/docs
HTTP 200 -> http://localhost:4450/docs/
```

Se muestra la documentación Swagger de los servicios REST de la API. La API raíz también responde:

```bash
$ curl -s http://localhost:4450/
{"name":"Atlas","status":"ok"}
```

---

## Componentes levantados (resumen)

| Componente | Imagen / Base | Contenedor | Puertos | Estado |
|---|---|---|---|---|
| **Base de datos** | postgres:15-alpine | atlas-postgres | `15432 → 5432` | Healthy |
| **Backend (API)** | atlas-atlas-backend (Node/Express) | atlas-backend | `4450 → 4000` | Up |
| **Frontend (cliente)** | atlas-atlas-frontend (React + Nginx) | atlas-frontend | `3350 → 80` | Up |

## Comandos útiles para la práctica

```bash
docker compose up -d          # levantar los contenedores
docker compose down           # detener y eliminar contenedores (mantiene volumenes)
docker compose down -v        # detener y eliminar también los datos (volumen)
docker compose ps             # estado de los servicios
docker logs -f atlas-backend  # ver logs de la API
docker logs -f atlas-frontend # ver logs del cliente
docker ps                     # listar contenedores activos
```

## Observaciones para el análisis de calidad y seguridad

El ambiente ya levantado permite verificar en un software real los criterios de la EA2:

- **Calidad funcional:** la plataforma es operable en `http://localhost:3350` y la API expone sus servicios en `http://localhost:4450/docs`.
- **Seguridad (hallazgos preliminares):** el `.env` viene con el `JWT_SECRET` incluido en el repositorio (secreto comprometido); esto será verificado con las herramientas de la asignatura (escaneo estático y dinámico).
- **Traza:** al estar todo ambiente bajo Docker, los logs y el código fuente quedan disponibles para auditoría y pruebas (Postman/Selenium/JMeter/OWASP ZAP).

## Referencia

- Guía oficial de la asignatura 2.1.3 — "Levantamiento de imágenes en docker del caso semestral".
- Documentación de Docker: https://docs.docker.com/compose/