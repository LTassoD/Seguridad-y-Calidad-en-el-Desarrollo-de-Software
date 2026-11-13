# -*- coding: utf-8 -*-
"""
AUDITOR TRANSVERSAL AUTOMÁTICO PARA ATLAS (UNIDADES 1, 2 Y 3)
=============================================================
Propósito:
  Cuando entreguen el nuevo código de Atlas modificado con nuevas fallas para la
  Evaluación de Unidad 3 / Examen Transversal, este script hace 3 cosas en segundos:

  1) DIFF AUTOMÁTICO DE CÓDIGO (Caja Blanca):
     Compara archivo por archivo el Atlas original (CodigoFuenteA) contra la nueva
     carpeta que entregue el profesor y muestra EXACTAMENTE qué líneas cambiaron.
  2) ESCÁNER SAST DE NUEVAS FALLAS (Unidades 1 y 2):
     Analiza automáticamente todos los archivos .js, .jsx y .sql buscando:
       - Nuevas inyecciones SQL (interpolación `${...}` o concatenación en `pool.query`)
       - Endpoints Express sin middleware de autenticación (IDOR / Broken Access Control)
       - Latencias artificiales (`delay`, `setTimeout`), bucles o condiciones de error
       - Secretos expuestos, contraseñas en texto claro, CORS abierto, Multer sin filtro
       - Vectores XSS (`dangerouslySetInnerHTML`, `eval`, `innerHTML`)
  3) REPORTE HTML CONSOLIDADO (`reporte_auditoria_transversal_atlas.html`):
     Genera la matriz lista para pegar en el Informe actualizado y defender.

Uso en PyCharm:
  - Clic derecho -> Run 'auditor_transversal_atlas'
  - Cuando recibas el nuevo código, solo cambia la variable RUTA_ATLAS_NUEVO abajo
    (o pásala por argumento: python auditor_transversal_atlas.py "C:/ruta/nuevo_atlas")
"""
import os
import re
import sys
import time
import difflib
from pathlib import Path

RUTA_ATLAS_ORIGINAL = Path(
    r"C:\Users\User\Desktop\Duoc\Duoc 6 semestre\Seguridad y calidad en el desarrollo de software\Código\CodigoFuenteA\CodigoFuenteA"
)
# Cuando recibas el nuevo código con fallas, pon su ruta aquí (por defecto audita el actual):
RUTA_ATLAS_NUEVO = Path(
    sys.argv[1] if len(sys.argv) > 1 else str(RUTA_ATLAS_ORIGINAL)
)

REPORT_OUT = Path(__file__).parent / "reporte_auditoria_transversal_atlas.html"

IGNORAR_DIRS = {"node_modules", ".git", "dist", "build", ".pytest_cache", "__pycache__", "uploads"}
EXTENSIONES_CODIGO = {".js", ".jsx", ".ts", ".tsx", ".sql", ".json", ".yml", ".yaml", ".conf"}


# ==============================================================================
# 1. COMPARADOR DIFERENCIAL (ORIGINAL VS. NUEVO ATLAS CON FALLAS)
# ==============================================================================

def listar_archivos(base: Path) -> dict[str, Path]:
    archivos = {}
    if not base.exists():
        return archivos
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in EXTENSIONES_CODIGO or f.startswith("Dockerfile"):
                rel = str(p.relative_to(base)).replace("\\", "/")
                archivos[rel] = p
    return archivos


def comparar_versiones(orig_dir: Path, nuevo_dir: Path) -> list[dict]:
    cambios = []
    if orig_dir.resolve() == nuevo_dir.resolve():
        return [{
            "archivo": "(Misma carpeta base: modo auditoría sobre CodigoFuenteA)",
            "tipo": "INFO",
            "resumen": "Cuando recibas el nuevo código de Atlas, apunta RUTA_ATLAS_NUEVO a la nueva carpeta para ver el diff exacto línea por línea.",
            "diff": "",
        }]

    arch_orig = listar_archivos(orig_dir)
    arch_nuevo = listar_archivos(nuevo_dir)

    for rel, p_nuevo in sorted(arch_nuevo.items()):
        if rel not in arch_orig:
            cambios.append({
                "archivo": rel,
                "tipo": "ARCHIVO NUEVO",
                "resumen": "Archivo agregado en la nueva versión de Atlas",
                "diff": p_nuevo.read_text(encoding="utf-8", errors="replace")[:1500],
            })
        else:
            t1 = arch_orig[rel].read_text(encoding="utf-8", errors="replace").splitlines()
            t2 = p_nuevo.read_text(encoding="utf-8", errors="replace").splitlines()
            if t1 != t2:
                diff_lines = list(difflib.unified_diff(t1, t2, fromfile=f"original/{rel}", tofile=f"nuevo/{rel}", lineterm="", n=2))
                cambios.append({
                    "archivo": rel,
                    "tipo": "MODIFICADO",
                    "resumen": f"{sum(1 for l in diff_lines if l.startswith('+') and not l.startswith('+++'))} líneas añadidas / {sum(1 for l in diff_lines if l.startswith('-') and not l.startswith('---'))} eliminadas",
                    "diff": "\n".join(diff_lines[:120]),
                })

    for rel in sorted(arch_orig.keys() - arch_nuevo.keys()):
        cambios.append({
            "archivo": rel,
            "tipo": "ELIMINADO",
            "resumen": "Archivo eliminado respecto a la versión original",
            "diff": "",
        })
    return cambios


# ==============================================================================
# 2. ESCÁNER SAST DE PATRONES DE FALLAS (UNIDADES 1, 2 Y 3)
# ==============================================================================

REGLAS_SAST = [
    {
        "id": "SAST-SQLI",
        "unidad": "U1/U2/U3 (Seguridad - OWASP A03)",
        "severidad": "CRÍTICO",
        "patron": re.compile(r"pool\.query\s*\(\s*`[^`]*\$\{"),
        "descripcion": "Posible Inyección SQL por interpolación directa `${...}` dentro de `pool.query` sin parámetros `$1`.",
    },
    {
        "id": "SAST-PLAIN-PWD",
        "unidad": "U1/U2 (Seguridad - OWASP A02 / A07)",
        "severidad": "CRÍTICO",
        "patron": re.compile(r"contrasena_hash\s*[!=]==?\s*password"),
        "descripcion": "Comparación de contraseña en texto claro sin algoritmo de hashing (bcrypt/argon2).",
    },
    {
        "id": "SAST-HARDCODED-SECRET",
        "unidad": "U2/U3 (Shift-Left Secrets - OWASP A02)",
        "severidad": "CRÍTICO",
        "patron": re.compile(r"(JWT_SECRET\s*\|\|\s*['\"][^'\"]+['\"]|postgresql://[^'\"\s]+:[^'\"\s]+@)"),
        "descripcion": "Secreto o credencial de base de datos hardcodeada en el código fuente.",
    },
    {
        "id": "SAST-MULTER-NO-FILTER",
        "unidad": "U2/U3 (Integridad - OWASP A08 / RF-5.2)",
        "severidad": "CRÍTICO",
        "patron": re.compile(r"multer\s*\(\s*\{\s*storage\s*\}\s*\)"),
        "descripcion": "Configuración de `multer` sin `fileFilter` ni límite de tamaño (permite subir `.exe` y `.html`).",
    },
    {
        "id": "SAST-CORS-OPEN",
        "unidad": "U2/U3 (Configuración DAST - OWASP A05)",
        "severidad": "GRAVE",
        "patron": re.compile(r"app\.use\s*\(\s*cors\s*\(\s*\)\s*\)"),
        "descripcion": "CORS completamente abierto (`Access-Control-Allow-Origin: *`) sin restricción de orígenes.",
    },
    {
        "id": "SAST-DELAY-PERF",
        "unidad": "U1/U2/U3 (Rendimiento y Estrés - NFR-PERF-1)",
        "severidad": "GRAVE",
        "patron": re.compile(r"await\s+delay\s*\(\s*\d+\s*\)|setTimeout\s*\([^,]+,\s*[1-9]\d{3,}\s*\)"),
        "descripcion": "Latencia artificial (`delay` / `setTimeout` >= 1 s) que degrada tiempos CRUD y satura hilos bajo estrés.",
    },
    {
        "id": "SAST-LOCALSTORAGE-JWT",
        "unidad": "U2/U3 (Sesión y XSS - OWASP A07)",
        "severidad": "GRAVE",
        "patron": re.compile(r"localStorage\.(setItem|getItem)\s*\(\s*['\"]token['\"]"),
        "descripcion": "Almacenamiento de token JWT en `localStorage` expuesto a exfiltración mediante XSS.",
    },
    {
        "id": "SAST-XSS-SINK",
        "unidad": "U3 (Pentesting XSS - Guía 3.1.2)",
        "severidad": "CRÍTICO",
        "patron": re.compile(r"dangerouslySetInnerHTML|\.innerHTML\s*=|\beval\s*\("),
        "descripcion": "Uso de sink peligroso (`dangerouslySetInnerHTML`, `innerHTML` o `eval`) vulnerable a XSS.",
    },
    {
        "id": "SAST-ERROR-LEAK",
        "unidad": "U2/U3 (Fuga de Información - OWASP A05)",
        "severidad": "MODERADO",
        "patron": re.compile(r"glosa:\s*err\.message"),
        "descripcion": "Respuesta HTTP 500 expone `err.message` interno de PostgreSQL/Node al cliente.",
    },
]


def auditar_rutas_sin_auth(ruta_js: Path, rel: str) -> list[dict]:
    """Detecta endpoints Express (`router.get/post/put/delete`) que no verifican token."""
    hallazgos = []
    if "routes/" not in rel or rel.endswith("auth.js"):
        return hallazgos
    lineas = ruta_js.read_text(encoding="utf-8", errors="replace").splitlines()
    pat_ruta = re.compile(r"^\s*router\.(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"](.*)$")
    for idx, ln in enumerate(lineas, 1):
        m = pat_ruta.match(ln)
        if m:
            metodo, endpoint, resto = m.group(1).upper(), m.group(2), m.group(3)
            # Revisar las siguientes 12 líneas del handler para ver si valida token/auth
            ventana = "\n".join(lineas[idx - 1 : min(idx + 12, len(lineas))])
            if not any(k in ventana for k in ("auth", "verify", "authorization", "Bearer", "req.user", "getUserFromToken")):
                hallazgos.append({
                    "id": "SAST-MISSING-AUTH",
                    "unidad": "U2/U3 (Control de Acceso IDOR - OWASP A01)",
                    "severidad": "CRÍTICO",
                    "archivo": f"{rel}:{idx}",
                    "codigo": ln.strip(),
                    "descripcion": f"Endpoint `{metodo} {endpoint}` definido sin validación de token JWT ni rol.",
                })
    return hallazgos


def ejecutar_escaner_sast(base: Path) -> list[dict]:
    hallazgos = []
    archivos = listar_archivos(base)
    for rel, path in sorted(archivos.items()):
        if path.suffix.lower() not in {".js", ".jsx", ".sql"}:
            continue
        lineas = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for idx, ln in enumerate(lineas, 1):
            for regla in REGLAS_SAST:
                if regla["patron"].search(ln):
                    hallazgos.append({
                        "id": regla["id"],
                        "unidad": regla["unidad"],
                        "severidad": regla["severidad"],
                        "archivo": f"{rel}:{idx}",
                        "codigo": ln.strip()[:140],
                        "descripcion": regla["descripcion"],
                    })
        if path.suffix.lower() == ".js":
            hallazgos.extend(auditar_rutas_sin_auth(path, rel))
    return hallazgos


def generar_html(cambios: list[dict], hallazgos: list[dict]):
    filas_diff = "\n".join(
        f"<tr><td><code>{c['archivo']}</code></td><td><b>{c['tipo']}</b></td><td>{c['resumen']}</td>"
        f"<td><pre style='margin:0;font-size:11px;max-height:160px;overflow:auto;'>{c['diff']}</pre></td></tr>"
        for c in cambios
    )
    filas_sast = "\n".join(
        f"<tr><td><b>{h['id']}</b></td><td>{h['unidad']}</td>"
        f"<td><span class='badge {h['severidad'].lower()}'>{h['severidad']}</span></td>"
        f"<td><code>{h['archivo']}</code></td><td><code>{h['codigo']}</code></td><td>{h['descripcion']}</td></tr>"
        for h in hallazgos
    )
    resumen_sev = {
        sev: sum(1 for h in hallazgos if h["severidad"] == sev)
        for sev in ("CRÍTICO", "GRAVE", "MODERADO")
    }
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Auditoría Transversal Automática — Sistema Atlas (Unidades 1, 2 y 3)</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 28px; color: #1f2937; background: #f8fafc; }}
  h1, h2 {{ color: #0f4c5c; }}
  .card {{ background: #fff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px; margin-top: 18px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 10px; }}
  th, td {{ border: 1px solid #cbd5e1; padding: 7px 9px; text-align: left; vertical-align: top; }}
  th {{ background: #e8f1f2; color: #0f4c5c; }}
  .badge {{ padding: 3px 7px; border-radius: 4px; font-weight: bold; font-size: 11px; }}
  .crítico {{ background: #fee2e2; color: #991b1b; }}
  .grave {{ background: #ffedd5; color: #9a3412; }}
  .moderado {{ background: #fef9c3; color: #854d0e; }}
</style>
</head>
<body>
  <h1>Reporte del Auditor Transversal Automático — Sistema Atlas</h1>
  <p><b>Carpeta auditada:</b> <code>{RUTA_ATLAS_NUEVO}</code> · <b>Fecha:</b> {time.strftime('%d-%m-%Y %H:%M:%S')}</p>
  <p><b>Resumen de hallazgos en código:</b> {len(hallazgos)} detectados
     (<b>{resumen_sev['CRÍTICO']} CRÍTICOS</b> · <b>{resumen_sev['GRAVE']} GRAVES</b> · <b>{resumen_sev['MODERADO']} MODERADOS</b>)</p>

  <div class="card">
    <h2>1. Comparación Diferencial contra Atlas Original (Detección de Cambios del Examen)</h2>
    <table>
      <thead><tr><th>Archivo</th><th>Estado</th><th>Resumen</th><th>Diff de líneas modificadas</th></tr></thead>
      <tbody>{filas_diff}</tbody>
    </table>
  </div>

  <div class="card">
    <h2>2. Hallazgos Automáticos SAST por Ubicación Exacta (Archivo y Línea)</h2>
    <table>
      <thead><tr><th>Regla</th><th>Unidad / Marco</th><th>Severidad</th><th>Archivo:Línea</th><th> Evidencia en Código</th><th>Descripción Técnica</th></tr></thead>
      <tbody>{filas_sast}</tbody>
    </table>
  </div>
</body>
</html>"""
    REPORT_OUT.write_text(html, encoding="utf-8")


def main():
    print("=" * 78)
    print("  AUDITOR TRANSVERSAL ATLAS — UNIDADES 1, 2 Y 3")
    print("=" * 78)
    print(f"Carpeta original : {RUTA_ATLAS_ORIGINAL}")
    print(f"Carpeta auditada : {RUTA_ATLAS_NUEVO}")
    cambios = comparar_versiones(RUTA_ATLAS_ORIGINAL, RUTA_ATLAS_NUEVO)
    hallazgos = ejecutar_escaner_sast(RUTA_ATLAS_NUEVO)
    generar_html(cambios, hallazgos)
    print(f"\nTotal de hallazgos detectados en código: {len(hallazgos)}")
    for h in hallazgos[:15]:
        print(f"  [{h['severidad']:8s}] {h['id']:22s} | {h['archivo']:36s} | {h['descripcion'][:55]}")
    if len(hallazgos) > 15:
        print(f"  ... y {len(hallazgos) - 15} hallazgos adicionales en el reporte HTML.")
    print(f"\n[OK] Reporte HTML generado en: {REPORT_OUT}")


if __name__ == "__main__":
    main()
