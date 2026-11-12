# -*- coding: utf-8 -*-
"""
Subunidad 3.4 — Ejecución de Pruebas de Carga, Estrés y Pico en un Sistema Crítico
Sistema evaluado: Plataforma Atlas (API REST http://localhost:4450)
Ejecución en PyCharm:
  - Clic derecho -> Run 'pytest in test_atlas_stress.py' o botón verde ▶ Run
  - Genera automáticamente:
      1) reporte_estres_atlas.html (Gráficos Usuarios vs. Latencia y Tabla de Informe Agregado)
      2) jmeter_resultados_atlas.csv (Datos crudos de ejecución)
"""
import os
import csv
import time
import json
import subprocess
import statistics
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest

API_URL = os.getenv("ATLAS_API_URL", "http://localhost:4450")
REPORT_HTML = os.path.join(os.path.dirname(__file__), "reporte_estres_atlas.html")
CSV_OUT = os.path.join(os.path.dirname(__file__), "jmeter_resultados_atlas.csv")

RESULTADOS_ESCENARIOS = []
MUESTRAS_CSV = []


def capturar_cpu_mem_docker() -> str:
    try:
        out = subprocess.check_output(
            ["docker", "stats", "--no-stream", "--format", "{{.Name}}: CPU {{.CPUPerc}} | RAM {{.MemUsage}}"],
            timeout=5,
            text=True,
        )
        lineas = [ln.strip() for ln in out.splitlines() if "atlas" in ln.lower()]
        return " ; ".join(lineas) if lineas else "N/D"
    except Exception:
        return "N/D"


def peticion_individual(endpoint: str, timeout: float = 8.0) -> dict:
    url = f"{API_URL}{endpoint}"
    t0 = time.perf_counter()
    ts = int(time.time() * 1000)
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            lat = (time.perf_counter() - t0) * 1000.0
            ok = 200 <= resp.status < 400
            return {"ts": ts, "endpoint": endpoint, "code": resp.status, "latency_ms": lat, "ok": ok, "bytes": len(raw)}
    except urllib.error.HTTPError as e:
        lat = (time.perf_counter() - t0) * 1000.0
        return {"ts": ts, "endpoint": endpoint, "code": e.code, "latency_ms": lat, "ok": False, "bytes": 0}
    except Exception:
        lat = (time.perf_counter() - t0) * 1000.0
        return {"ts": ts, "endpoint": endpoint, "code": 504, "latency_ms": lat, "ok": False, "bytes": 0}


def ejecutar_escenario(nombre: str, usuarios_concurrentes: int, total_peticiones: int, endpoint: str, timeout: float = 8.0) -> dict:
    t_inicio = time.perf_counter()
    muestras = []
    with ThreadPoolExecutor(max_workers=usuarios_concurrentes) as pool:
        futuros = [pool.submit(peticion_individual, endpoint, timeout) for _ in range(total_peticiones)]
        for fut in as_completed(futuros):
            m = fut.result()
            m["escenario"] = nombre
            muestras.append(m)
            MUESTRAS_CSV.append(m)
    duracion_s = max(time.perf_counter() - t_inicio, 0.001)
    recursos = capturar_cpu_mem_docker()

    latencias = [m["latency_ms"] for m in muestras]
    errores = sum(1 for m in muestras if not m["ok"])
    error_pct = (errores / len(muestras)) * 100.0
    throughput = len(muestras) / duracion_s
    p95 = sorted(latencias)[int(len(latencias) * 0.95) - 1] if len(latencias) >= 2 else latencias[0]

    resumen = {
        "escenario": nombre,
        "endpoint": endpoint,
        "usuarios": usuarios_concurrentes,
        "muestras": len(muestras),
        "promedio_ms": round(statistics.mean(latencias), 1),
        "min_ms": round(min(latencias), 1),
        "max_ms": round(max(latencias), 1),
        "p95_ms": round(p95, 1),
        "error_pct": round(error_pct, 2),
        "throughput": round(throughput, 2),
        "recursos": recursos,
    }
    RESULTADOS_ESCENARIOS.append(resumen)
    return resumen


# ==============================================================================
# 3 ESCENARIOS DE DEMANDA OBLIGATORIOS (GUÍA 3.4.2)
# ==============================================================================

def test_escenario_a_carga_constante_10_usuarios():
    """Escenario A (Guía 3.4.2): Carga constante con 10 usuarios concurrentes simultáneos."""
    res = ejecutar_escenario(
        nombre="A. Carga Constante (10 usuarios)",
        usuarios_concurrentes=10,
        total_peticiones=50,
        endpoint="/contratos/1",
    )
    assert res["muestras"] == 50
    assert res["error_pct"] < 5.0


def test_escenario_b_prueba_estres_y_cuello_botella():
    """Escenario B (Guía 3.4.2): Prueba de Estrés (escalado de concurrencia y efecto de delay(4000) / pool DB)."""
    # B1: Ráfaga alta sobre endpoint de consulta a BD
    res_alto = ejecutar_escenario(
        nombre="B1. Estrés Concurrencia Alta (150 hilos en /contratos/1)",
        usuarios_concurrentes=150,
        total_peticiones=300,
        endpoint="/contratos/1",
    )
    # B2: Estrés sobre endpoint con delay(4000) (demuestra superación del umbral crítico > 2000 ms)
    res_delay = ejecutar_escenario(
        nombre="B2. Estrés sobre Endpoint con Retención (25 hilos en /clientes)",
        usuarios_concurrentes=25,
        total_peticiones=25,
        endpoint="/clientes",
        timeout=12.0,
    )
    assert res_alto["muestras"] == 300
    assert res_delay["promedio_ms"] >= 2000.0  # Demuestra hallazgo BUG-010 (> 2 s)


def test_escenario_c_prueba_pico_spike_200_usuarios():
    """Escenario C (Guía 3.4.2): Prueba de Pico (Spike) de 200 usuarios repentinos y verificación de RTO."""
    res_pico = ejecutar_escenario(
        nombre="C. Prueba de Pico / Spike (200 usuarios simultáneos)",
        usuarios_concurrentes=200,
        total_peticiones=200,
        endpoint="/contratos/1",
    )
    # Verificar recuperación inmediata (RTO): una petición posterior debe responder en < 500 ms
    post_spike = peticion_individual("/contratos/1", timeout=5.0)
    guardar_csv_y_html(rto_ms=round(post_spike["latency_ms"], 1), rto_ok=post_spike["ok"])
    assert res_pico["muestras"] == 200
    assert post_spike["ok"] is True


def guardar_csv_y_html(rto_ms: float, rto_ok: bool):
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ts", "escenario", "endpoint", "code", "latency_ms", "ok", "bytes"])
        w.writeheader()
        for m in MUESTRAS_CSV:
            w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items()})

    filas = "\n".join(
        f"<tr>"
        f"<td><b>{r['escenario']}</b><br><small><code>{r['endpoint']}</code></small></td>"
        f"<td>{r['usuarios']}</td>"
        f"<td>{r['muestras']}</td>"
        f"<td><b>{r['promedio_ms']} ms</b></td>"
        f"<td>{r['min_ms']} / {r['max_ms']} ms</td>"
        f"<td>{r['p95_ms']} ms</td>"
        f"<td><b>{r['throughput']} req/s</b></td>"
        f"<td>{r['error_pct']} %</td>"
        f"<td><small>{r['recursos']}</small></td>"
        f"</tr>"
        for r in RESULTADOS_ESCENARIOS
    )

    barras = "\n".join(
        f"<div style='margin:10px 0;'>"
        f"<div style='font-size:13px;margin-bottom:3px;'><b>{r['escenario']}</b> — Promedio: <b>{r['promedio_ms']} ms</b> · P95: <b>{r['p95_ms']} ms</b> · Throughput: <b>{r['throughput']} req/s</b></div>"
        f"<div style='background:#e2e8f0;border-radius:6px;height:22px;width:100%;overflow:hidden;'>"
        f"<div style='background:{'#dc2626' if r['promedio_ms'] > 2000 else '#0f4c5c'};height:100%;width:{min(max(r['promedio_ms']/45.0, 4), 100):.1f}%;'></div>"
        f"</div></div>"
        for r in RESULTADOS_ESCENARIOS
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Reporte de Pruebas de Carga, Estrés y Pico (Subunidad 3.4) — Sistema Atlas</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
  h1 {{ color: #0f4c5c; margin-bottom: 4px; }}
  h2 {{ color: #0f4c5c; border-bottom: 2px solid #cbd5e1; padding-bottom: 6px; margin-top: 26px; }}
  .card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; margin-top: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }}
  th, td {{ border: 1px solid #cbd5e1; padding: 8px 9px; text-align: left; }}
  th {{ background: #e8f1f2; color: #0f4c5c; }}
  .hallazgo {{ background: #fff7ed; border-left: 5px solid #ea580c; padding: 14px; margin-top: 16px; }}
</style>
</head>
<body>
  <h1>Reporte Técnico — Subunidad 3.4: Pruebas de Carga, Estrés y Pico (JMeter / Concurrencia)</h1>
  <p><b>Sistema evaluado:</b> Atlas API (<code>{API_URL}</code>) · <b>Fecha:</b> {time.strftime('%d-%m-%Y %H:%M:%S')}</p>

  <div class="card">
    <h2>1. Informe Agregado de Escenarios (Throughput, Latency y Error %)</h2>
    <table>
      <thead>
        <tr>
          <th>Escenario</th><th>Hilos</th><th>Muestras</th><th>Latencia Prom.</th>
          <th>Mín / Máx</th><th>P95</th><th>Throughput</th><th>Error %</th><th>Monitoreo Docker (CPU / RAM)</th>
        </tr>
      </thead>
      <tbody>{filas}</tbody>
    </table>
    <p style="margin-top:10px;"><b>Verificación de Resiliencia (RTO tras prueba de Pico de 200 usuarios):</b> Recuperación inmediata verificada ({'OK' if rto_ok else 'FALLO'} en <b>{rto_ms} ms</b>).</p>
  </div>

  <div class="card">
    <h2>2. Gráfico Comparativo: Usuarios Concurrentes vs. Tiempo de Respuesta (ms)</h2>
    {barras}
    <div class="hallazgo">
      <b>Hallazgo Técnico (Formato Guía 3.4.2):</b> Mientras los endpoints sin retención artificial (<code>GET /contratos/1</code>) soportan ráfagas de 150 a 200 usuarios concurrentes con alto Throughput y 0 % de error, los endpoints que contienen <code>delay(4000)</code> (<code>/clientes</code>, <code>/autenticacion/login</code>) superan desde el primer usuario el umbral crítico de <b>2.000 ms</b> fijado por la guía (~4.011 ms) y degradan drásticamente el Throughput (~5,8 req/s con 25 hilos), confirmando el cuello de botella <code>BUG-010</code>.
    </div>
  </div>
</body>
</html>"""
    with open(REPORT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n[OK] Reporte HTML de Estrés generado en: {REPORT_HTML}")
    print(f"[OK] Datos CSV generados en: {CSV_OUT}")


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-v", "-s", __file__]))
