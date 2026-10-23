#!/usr/bin/env bash
# ============================================================================
# Script de pruebas EP3/EP4 - Sistema Atlas (Caso Semestral)
# Ejecuta la bateria de pruebas funcionales (FN) y de seguridad (SEG).
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
# FUNCIONALES (FN)
# ============================================================================

encabezado "FN-01 Login valido admin/admin"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"admin"}'

TOKEN=$(curl -s -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"admin"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['token'])" 2>/dev/null)
echo "  Token JWT obtenido (len=${#TOKEN})"

encabezado "FN-02 Login contrasena incorrecta"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  -X POST "$API/autenticacion/login" -H "Content-Type: application/json" \
  -d '{"nombre_usuario":"admin","password":"incorrecta"}'

encabezado "FN-03 Estado salud de la API"
curl -s -w "\n  --> HTTP %{http_code}\n" "$API/"

encabezado "FN-04 Documentacion Swagger /docs/"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" -L "$API/docs/"

encabezado "FN-05 Listar clientes (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  "$API/clientes" -H "Authorization: Bearer $TOKEN"

encabezado "FN-06 Buscar cliente por nombre (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  "$API/clientes/search?name=Mar" -H "Authorization: Bearer $TOKEN"

encabezado "FN-07 Crear cliente (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  -X POST "$API/clientes" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"nombre":"Cliente Prueba Script","correo":"script@test.cl","telefono":"111","direccion":"Calle 1","es_empresa":false}'

encabezado "FN-08 Listar contratos (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}  tiempo=%{time_total}s\n" \
  "$API/contratos" -H "Authorization: Bearer $TOKEN"

encabezado "FN-09 Dashboard metricas (token)"
curl -s -o /dev/null -w "  HTTP %{http_code}\n" \
  "$API/contratos/dashboard" -H "Authorization: Bearer $TOKEN"

# ============================================================================
# SEGURIDAD (SEG) - 10 pruebas: 7 inseguras / 3 conformes
# Numeracion alineada con el Anexo B del informe y la presentacion:
#   SEG-01, SEG-02, SEG-03, SEG-04, SEG-05, SEG-06, SEG-07b, SEG-10,
#   SEG-12 y SEG-13.
# ============================================================================

encabezado "SEG-01 IDOR: GET /contratos/1 y descarga SIN token (esperado 401)"
curl -s -o /dev/null -w "  contrato: HTTP %{http_code}\n" "$API/contratos/1"
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