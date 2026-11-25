"""Genera un dashboard HTML local a partir de los CSV de la EVA3."""
import csv
import html
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "registro_pruebas.csv"
RESOURCES = ROOT / "mediciones_recursos.csv"
OUTPUT = ROOT / "dashboard.html"


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def money(value):
    if not value:
        return "—"
    return "$" + f"{int(value):,}".replace(",", ".")


def main():
    rows = read_csv(TESTS)
    resources = read_csv(RESOURCES)
    numeric = [r for r in rows if r.get("esperado_ingresos_clp") and r.get("observado_ingresos_clp")]
    latencies = [int(r["duracion_segundos"]) for r in rows if r.get("duracion_segundos")]
    matches = [
        r for r in numeric
        if r["esperado_ingresos_clp"] == r["observado_ingresos_clp"]
        and r["esperado_gastos_clp"] == r["observado_gastos_clp"]
    ]
    repeated = [r for r in rows if r["test_id"] == "OBS-01" and r.get("duracion_segundos")]
    consistent = [
        r for r in repeated
        if r["esperado_ingresos_clp"] == r["observado_ingresos_clp"]
        and r["esperado_gastos_clp"] == r["observado_gastos_clp"]
    ]
    failures = [r for r in rows if "error" in (r.get("resultado") or "").lower()]
    companies = sorted({r.get("empresa", "") for r in rows if r.get("empresa")})
    test_ids = sorted({r.get("test_id", "") for r in rows if r.get("test_id")})

    by_id = {r["test_id"]: r for r in rows}
    run_labels = []
    for row in rows:
        if row.get("duracion_segundos"):
            test_id = row["test_id"]
            same = [r for r in rows if r["test_id"] == test_id]
            position = same.index(row) + 1
            run_labels.append({
                "label": f"{test_id} · intento {position}",
                "seconds": int(row["duracion_segundos"]),
            })

    resource_values = []
    for row in resources:
        resource_values.append({
            "state": row["estado"],
            "cpu_min": float(row["cpu_min_pct"]),
            "cpu_max": float(row["cpu_max_pct"]),
            "memory": float(row["memoria_mib"]),
        })

    details = []
    for row in rows:
        details.append({
            "test_id": row["test_id"],
            "company": row["empresa"],
            "period": row["periodo"] or "—",
            "expected_sales": money(row["esperado_ingresos_clp"]),
            "actual_sales": money(row["observado_ingresos_clp"]),
            "expected_purchases": money(row["esperado_gastos_clp"]),
            "actual_purchases": money(row["observado_gastos_clp"]),
            "seconds": row["duracion_segundos"] or "—",
            "result": row["resultado"],
        })

    stats = {
        "numeric_correct": len(matches),
        "numeric_total": len(numeric),
        "consistency_correct": len(consistent),
        "consistency_total": len(repeated),
        "median_seconds": statistics.median(latencies) if latencies else None,
        "mean_seconds": round(statistics.mean(latencies), 1) if latencies else None,
        "failures": len(failures),
        "executions": len(rows),
    }
    data = json.dumps({
        "stats": stats,
        "runs": run_labels,
        "resources": resource_values,
        "details": details,
        "companies": companies,
        "test_ids": test_ids,
    }, ensure_ascii=False)

    page = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Observabilidad del agente IA</title>
<style>
:root{--ink:#19324b;--muted:#66788a;--blue:#2b6cb0;--pale:#eaf2fb;--green:#16794b;--border:#dce4ec;--bg:#f4f7fb}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1150px;margin:0 auto;padding:32px 24px 48px}header{margin-bottom:22px}h1{font-size:28px;margin:0 0 5px}h2{font-size:19px;margin:0 0 18px}.muted{color:var(--muted)}
.notice{background:#fff8df;border:1px solid #f0dda1;border-radius:10px;padding:12px 15px;margin:18px 0 22px;color:#634e12}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}.card,.panel{background:white;border:1px solid var(--border);border-radius:12px;padding:18px;box-shadow:0 2px 8px #1b3a5710}.card .label{color:var(--muted);font-size:13px}.card strong{display:block;font-size:25px;margin-top:7px}.panel{margin:16px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.chart{display:grid;gap:11px}.barrow{display:grid;grid-template-columns:140px 1fr 55px;gap:9px;align-items:center;font-size:13px}.bar-bg{height:14px;background:#edf2f7;border-radius:9px;overflow:hidden}.bar{height:100%;background:var(--blue);border-radius:9px;min-width:2px}.bar.cpu{background:#dd8b24}.bar.mem{background:#48a27a}.filters{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 14px}select{padding:8px 10px;border:1px solid var(--border);border-radius:8px;background:white;color:var(--ink)}
.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:9px 8px;border-bottom:1px solid var(--border);white-space:nowrap}th{color:var(--muted);font-weight:600}.ok{color:var(--green);font-weight:600}.empty{color:var(--muted);padding:12px 0}.foot{font-size:12px;color:var(--muted);margin-top:22px}
@media(max-width:800px){.cards{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}.barrow{grid-template-columns:105px 1fr 45px}}
@media(max-width:480px){main{padding:22px 14px}.cards{grid-template-columns:1fr 1fr}.card{padding:13px}.card strong{font-size:21px}}
</style>
</head>
<body><main>
<header><p class="muted">EVA3 · evaluación manual registrada</p><h1>Observabilidad del agente IA</h1><p class="muted">Resumen de respuestas, latencia y recursos observados.</p></header>
<div class="notice">Muestra inicial. Las métricas reflejan únicamente las ejecuciones registradas en los archivos CSV; no representan todavía una evaluación general del agente.</div>
<section class="cards" id="cards"></section>
<div class="grid">
<section class="panel"><h2>Tiempo de respuesta por ejecución</h2><div class="chart" id="latency-chart"></div></section>
<section class="panel"><h2>CPU observado</h2><div class="chart" id="cpu-chart"></div><p class="muted">Porcentaje informado por Docker.</p></section>
</div>
<section class="panel"><h2>Memoria observada</h2><div class="chart" id="memory-chart"></div><p class="muted">Memoria del contenedor durante las observaciones.</p></section>
<section class="panel"><h2>Registro de pruebas</h2>
<div class="filters"><label>Empresa <select id="company-filter"><option value="">Todas</option></select></label><label>Prueba <select id="test-filter"><option value="">Todas</option></select></label></div>
<div class="table-wrap"><table><thead><tr><th>Prueba</th><th>Empresa</th><th>Período</th><th>Ventas esperadas/observadas</th><th>Compras esperadas/observadas</th><th>Tiempo</th><th>Resultado</th></tr></thead><tbody id="results-body"></tbody></table></div>
</section>
<p class="foot">Generado localmente desde registro_pruebas.csv y mediciones_recursos.csv. Para actualizar el dashboard, vuelve a ejecutar el generador.</p>
</main>
<script id="dashboard-data" type="application/json">__DATA__</script>
<script>
const d=JSON.parse(document.getElementById('dashboard-data').textContent);
const pct=(a,b)=>b?Math.round(100*a/b)+'%':'—';
const median=d.stats.median_seconds===null?'—':d.stats.median_seconds+' s';
const cards=[
 ['Consultas numéricas correctas',d.stats.numeric_correct+'/'+d.stats.numeric_total+' · '+pct(d.stats.numeric_correct,d.stats.numeric_total)],
 ['Consistencia en OBS-01',d.stats.consistency_correct+'/'+d.stats.consistency_total+' · '+pct(d.stats.consistency_correct,d.stats.consistency_total)],
 ['Latencia mediana',median],
 ['Errores registrados',d.stats.failures+'/'+d.stats.executions]
];
document.getElementById('cards').innerHTML=cards.map(x=>'<article class="card"><span class="label">'+x[0]+'</span><strong>'+x[1]+'</strong></article>').join('');
function drawBars(target,items,max,key,labelFn,kind){
 const el=document.getElementById(target); if(!items.length){el.innerHTML='<div class="empty">No hay mediciones registradas.</div>';return;}
 el.innerHTML=items.map(item=>{const val=item[key];const w=max?Math.max(2,val/max*100):0;return '<div class="barrow"><span>'+labelFn(item)+'</span><div class="bar-bg"><div class="bar '+kind+'" style="width:'+w+'%"></div></div><b>'+val+'</b></div>';}).join('');
}
const maxTime=Math.max(1,...d.runs.map(x=>x.seconds));
drawBars('latency-chart',d.runs,maxTime,'seconds',x=>x.label,'');
const cpu=d.resources.map(x=>({label:x.state==='sin_consulta'?'En reposo':'Durante consulta',min:x.cpu_min,max:x.cpu_max}));
const maxCpu=Math.max(1,...cpu.map(x=>x.max));
document.getElementById('cpu-chart').innerHTML=cpu.length?cpu.map(x=>'<div class="barrow"><span>'+x.label+'</span><div class="bar-bg"><div class="bar cpu" style="width:'+Math.max(2,x.max/maxCpu*100)+'%"></div></div><b>'+x.min+'–'+x.max+'%</b></div>').join(''):'<div class="empty">No hay mediciones registradas.</div>';
const maxMem=Math.max(1,...d.resources.map(x=>x.memory));
drawBars('memory-chart',d.resources,maxMem,'memory',x=>x.state==='sin_consulta'?'En reposo':'Durante consulta','mem');
const company=document.getElementById('company-filter'), test=document.getElementById('test-filter');
d.companies.forEach(x=>company.add(new Option(x,x)));d.test_ids.forEach(x=>test.add(new Option(x,x)));
function renderTable(){const filtered=d.details.filter(x=>(!company.value||x.company===company.value)&&(!test.value||x.test_id===test.value));document.getElementById('results-body').innerHTML=filtered.map(x=>'<tr><td>'+x.test_id+'</td><td>'+x.company+'</td><td>'+x.period+'</td><td>'+x.expected_sales+' / '+x.actual_sales+'</td><td>'+x.expected_purchases+' / '+x.actual_purchases+'</td><td>'+x.seconds+(x.seconds==='—'?'':' s')+'</td><td class="ok">'+x.result+'</td></tr>').join('');}
company.addEventListener('change',renderTable);test.addEventListener('change',renderTable);renderTable();
</script></body></html>'''
    OUTPUT.write_text(page.replace("__DATA__", data), encoding="utf-8")
    print(f"Dashboard generado: {OUTPUT}")


if __name__ == "__main__":
    main()
