#!/usr/bin/env python3
"""Live progress dashboard for AI-side generation.

Usage:
  python -X utf8 scripts/progress.py             # one-shot terminal table
  python -X utf8 scripts/progress.py --serve     # browser dashboard at http://127.0.0.1:8768

Reads only the filesystem: data/ai/<model>/<section>/*.md vs cap 70,
per-worker rate from file mtimes (last 15 min), fail counts from gen_*.log.
"""
import http.server
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AI = ROOT / "data" / "ai"
CAP = 70
SECTIONS = ["abstract", "introduction", "discussion"]
RATE_WIN = 15.0  # minutes
STALE = 20.0     # minutes without a new file -> stuck


def snapshot():
    now = time.time()
    rows = []
    for mdir in sorted(AI.iterdir()) if AI.exists() else []:
        if not mdir.is_dir():
            continue
        for sec in SECTIONS:
            files = list((mdir / sec).glob("*.md"))
            n = len(files)
            recent = sum(1 for f in files if now - f.stat().st_mtime < RATE_WIN * 60)
            rate = recent / RATE_WIN
            mt = max((f.stat().st_mtime for f in files), default=0)
            idle = (now - mt) / 60 if mt else None
            done = n >= CAP
            eta = None
            if not done and rate > 0.05:
                eta = (CAP - n) / rate
            stuck = (not done) and idle is not None and idle > STALE
            log = ROOT / ("gen_" + mdir.name.replace("-", "_") + ".log")
            fails = 0
            if log.exists():
                fails = sum(1 for line in log.read_text(encoding="utf-8",
                            errors="ignore").splitlines() if line.startswith("[fail]"))
            rows.append({"model": mdir.name, "sec": sec, "n": n, "rate": rate,
                         "eta": eta, "idle": idle, "done": done, "stuck": stuck,
                         "fails": fails})
    return rows


def bar(n, width=22):
    filled = round(width * min(n, CAP) / CAP)
    return "#" * filled + "." * (width - filled)


def render_text(rows):
    total_n = sum(r["n"] for r in rows)
    total_cap = CAP * len({r["model"] for r in rows}) * len(SECTIONS)
    print(f"AI-side generation progress   {total_n}/{total_cap} files   "
          f"{time.strftime('%H:%M:%S')}\n")
    print(f"{'model/section':<42}{'progress':<26}{'rate':>9}{'eta':>10}  status")
    print("-" * 100)
    cur = None
    for r in rows:
        if r["model"] != cur:
            cur = r["model"]
            fr = next((x for x in rows if x["model"] == cur), None)
        line = f"{r['model'] + '/' + r['sec']:<42}"
        if r["done"]:
            line += f"[{bar(r['n'])}] {r['n']}/{CAP}  DONE"
        else:
            eta = f"{r['eta']:.0f}min" if r["eta"] else "--"
            line += f"[{bar(r['n'])}] {r['n']}/{CAP}"
            line += f"{r['rate']:>8.1f}/m{eta:>10}"
        status = "STUCK" if r["stuck"] else ("fails:" + str(r["fails"]) if r["fails"] else "ok")
        print(f"{line}  {status}")


CSS = """body{font-family:Segoe UI,system-ui,sans-serif;background:#111;color:#ddd;
margin:24px}h1{font-size:18px}table{border-collapse:collapse;width:100%}
td,th{padding:6px 10px;border-bottom:1px solid #333;font-size:14px;text-align:left}
.bar{background:#2b2b2b;border-radius:4px;height:16px;width:220px;position:relative}
.fill{height:16px;border-radius:4px;background:#4caf50}
.running .fill{background:#e0a63c}.stuck .fill{background:#d05050}
.small{color:#888;font-size:12px}.meta{color:#6cf}"""


def render_html(rows):
    total_n = sum(r["n"] for r in rows)
    n_models = len({r["model"] for r in rows})
    total_cap = CAP * n_models * len(SECTIONS)
    trs = []
    for r in rows:
        pct = min(100, 100 * r["n"] / CAP)
        cls = "done" if r["done"] else ("stuck" if r["stuck"] else "running")
        extra = "DONE" if r["done"] else (
            f"{r['rate']:.1f}/min, ETA {r['eta']:.0f}min" if r["eta"] else
            (f"idle {r['idle']:.0f}min" if r["idle"] else "waiting"))
        trs.append(
            f"<tr class='{cls}'><td><span class='meta'>{r['model']}</span>/{r['sec']}</td>"
            f"<td><div class='bar'><div class='fill' style='width:{pct}%'></div></div></td>"
            f"<td>{r['n']}/{CAP}</td><td>{extra}</td><td>fails {r['fails']}</td></tr>")
    return f"""<!doctype html><html><head><meta charset='utf-8'>
<meta http-equiv='refresh' content='10'><title>deai generation progress</title>
<style>{CSS}</style></head><body>
<h1>AI-side generation — {total_n}/{total_cap} files ({100*total_n/max(total_cap,1):.0f}%)</h1>
<table><tr><th>model / section</th><th style='width:240px'>progress</th><th>count</th>
<th>rate / eta</th><th>errors</th></tr>{''.join(trs)}</table>
<p class='small'>auto-refresh 10s · cap {CAP}/model/section · data/ai · {time.strftime('%H:%M:%S')}</p>
</body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = render_html(snapshot()).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if "--serve" in sys.argv:
        print("dashboard: http://127.0.0.1:8768")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8768), Handler).serve_forever()
    else:
        render_text(snapshot())
