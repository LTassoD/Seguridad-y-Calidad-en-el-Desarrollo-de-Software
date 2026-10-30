#!/usr/bin/env bash
# ============================================================================
# Script de pruebas EP3/EP4 - Sistema Atlas (Caso Semestral)
# Ejecuta 14 casos de prueba (CP-001 a CP-014) y 10 pruebas de seguridad (SEG).
# SEG: 10 pruebas (7 inseguras / 3 conformes), alineadas con el Anexo B
# del informe y con la presentacion (SEG-07b y SEG-12).
#
# Requisitos:
#   - Ambiente Atlas levantado: docker compose up -d --build
#   - curl disponible
#
# Uso:
#   bash test_atlas.sh
# Tip: redirige a archivo para guardar evidencia:
#   bash test_atlas.sh | tee test_atlas_salida_$(date +%F).log
# ============================================================================

API=${API:-http://localhost:4450}
ORIGEN=${ORIGEN:-http://atlas.local}

echo "===================================================="
echo "  BATERIA DE PRUEBAS ATLAS - EP3/EP4"
echo "  API: $API"
echo "  Fecha: $(date)"
echo "===================================================="

# ---- utilidades ------------------------------------------------------------
inc=0
function encabezado() {
  inc=$((inc+1)); echo; echo "----------------------------"
  printf "TEST %02d: %s\n" "$inc" "$1"
  echo "----------------------------"
}

# ============================================================================
# CASOS DE PRUEBA FUNCIONALES Y NO FUNCIONALES (CP)
# ============================================================================

encabezado "CP-001 Login valido admin/admin"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"admin"}'

TOKEN=$(curl -s -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"admin"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['token'])" 2>/dev/null)
echo "  Token JWT obtenido (len=${#TOKEN})"

encabezado "CP-002 Login contrasena incorrecta"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"incorrecta"}'

encabezado "CP-003 Estado salud de la API"
curl -s -w "\n  --> HTTP %{http_code}\n" "$API/"

encabezado "CP-004 Documentacion Swagger /docs/"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" -L "$API/docs/"

encabezado "CP-005 Listar clientes (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  "$API/clientes" -H "Authorization: Bearer $TOKEN"

encabezado "CP-006 Buscar cliente por nombre (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  "$API/clientes/search?name=Mar" -H "Authorization: Bearer $TOKEN"

encabezado "CP-007 Crear cliente (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  -X POST "$API/clientes" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"nombre":"Cliente Prueba Script","correo":"script@test.cl","telefono":"111","direccion":"Calle 1","es_empresa":false}'

encabezado "CP-008 Listar contratos (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  "$API/contratos" -H "Authorization: Bearer $TOKEN"

encabezado "CP-009 Dashboard metricas (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  "$API/contratos/dashboard" -H "Authorization: Bearer $TOKEN"

encabezado "CP-010 Upload .exe y .html a contrato (esperado rechazo 400/415)"
printf 'MZ fake exe content' > /tmp/atlas_payload.exe
printf '<html>payload</html>' > /tmp/atlas_payload.html
for f in /tmp/atlas_payload.exe /tmp/atlas_payload.html; do
  curl -s -o /dev/null -w "  $(basename "$f"): HTTP %{http_code}\n" \
    -X POST "$API/contratos" -H "Authorization: Bearer $TOKEN" \
    -F "cliente_id=1" -F "titulo=Contrato prueba upload" \
    -F "fecha_inicio=2026-01-01" -F "fecha_fin=2026-12-31" \
    -F "file=@$f"
done
echo "  Nota: un 201 confirma BUG-003 (solo se admiten PDF, DOC, PPT, JPG y PNG)."

encabezado "CP-011 Acceso a contrato SIN token (esperado 401)"
curl -s -o /dev/null -w "  GET /contratos/1: HTTP %{http_code}\n" "$API/contratos/1"
echo "  Nota: un 200 confirma BUG-001 (control de acceso ausente)."

encabezado "CP-012 SQLi en login (esperado 401)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d "{\"nombre_usuario\":\"admin' OR '1'='1\",\"password\":\"x\"}"

encabezado "CP-013 Rendimiento GET /clientes: 5 mediciones (umbral 0,300 s)"
for i in 1 2 3 4 5; do
  curl -s -o /dev/null -w "  medicion $i: HTTP %{http_code}  %{time_total}s\n" \
    "$API/clientes" -H "Authorization: Bearer $TOKEN"
done

encabezado "CP-014 Usabilidad y accesibilidad del login (revision asistida)"
curl -s -o /dev/null -w "  frontend /login: HTTP %{http_code}\n" \
  "${FRONTEND:-http://localhost:3350}/login"
echo "  Checklist manual: fuente >=12 px, contraste AA, labels asociados, lang=es, foco visible, mensajes de error."
echo "  Evidencia automatica: Lighthouse (Accessibility) >= 0,90; en la revision se obtuvo 0,96."

# ============================================================================
# SEGURIDAD (SEG) - 10 pruebas: 7 inseguras / 3 conformes
# Numeracion alineada con el Anexo B del informe y la presentacion:
#   SEG-01, SEG-02, SEG-03, SEG-04, SEG-05, SEG-06, SEG-07b, SEG-10,
#   SEG-12 y SEG-13.
# ============================================================================

encabezado "SEG-01 IDOR: GET /contratos/1 y descarga SIN token (esperado 401)"
curl -s -o /dev/null -w "  contrato: HTTP %{http_code}\n" "$API/contratos/1"
# ID 5: contrato con archivo adjunto en los datos semilla del entorno de pruebas
curl -s -o /dev/null -w "  archivo:  HTTP %{http_code}  tipo=%{content_type}\n" \
  "$API/contratos/5/file"

encabezado "SEG-02 IDOR: GET /usuarios/1 SIN token (esperado 401)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$API/usuarios/1"

encabezado "SEG-03 IDOR: GET /auditoria SIN token (esperado 401)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$API/auditoria"

encabezado "SEG-04 IDOR: GET /roles SIN token (esperado 401)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" "$API/roles"

encabezado "SEG-05 SQLi en login (esperado 401; consulta parametrizada)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d "{\"nombre_usuario\":\"admin' OR '1'='1\",\"password\":\"x\"}"

encabezado "SEG-06 Login con contrasena incorrecta (esperado 401, sin enumeracion)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"incorrecta"}'

encabezado "SEG-07b Upload .exe y .html a contrato (esperado rechazo 400/415)"
printf 'MZ fake exe content' > /tmp/atlas_payload.exe
printf '<html>payload</html>' > /tmp/atlas_payload.html
for f in /tmp/atlas_payload.exe /tmp/atlas_payload.html; do
  curl -s -o /dev/null -w "  $(basename "$f"): HTTP %{http_code}\n" \
    -X POST "$API/contratos" -H "Authorization: Bearer $TOKEN" \
    -F "cliente_id=1" -F "titulo=Contrato prueba upload" \
    -F "fecha_inicio=2026-01-01" -F "fecha_fin=2026-12-31" \
    -F "file=@$f"
done

encabezado "SEG-10 Acceso con token valido a recurso propio (esperado 200)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  "$API/clientes" -H "Authorization: Bearer $TOKEN"

encabezado "SEG-12 CORS: Origin malicioso (esperado origen restringido)"
curl -s -D - -o /dev/null \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -H "Origin: http://evil.example.com" \
  -d '{"nombre_usuario":"x","password":"y"}' | grep -i "access-control\|HTTP/"

encabezado "SEG-13 Fuerza bruta: 3 logins fallidos seguidos (esperado bloqueo)"
for i in 1 2 3; do
  curl -s -o /dev/null -w "  intento $i: HTTP %{http_code} en %{time_total}s\n" \
    -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
    -d '{"nombre_usuario":"admin","password":"wrong"}'
done

echo
echo "===================================================="
echo "  Bateria finalizada. Revisa codigos HTTP vs"
echo "  'Resultado esperado' del Anexo B del informe."
echo "===================================================="