#!/usr/bin/env python3
"""Generate AI-side sections from seeds.json (paired with human corpus by PMCID).

Controlled conditions: prompt contains facts only (title/keywords/results),
NO style instructions. Structure mirrors the paired human abstract.

Providers (enable whichever API keys exist in env):
  OPENROUTER_API_KEY   -> OpenRouter, one key routes many models (models: list)
  OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY / DEEPSEEK_API_KEY / MOONSHOT_API_KEY

Models come from config.json: {"models": {"openrouter": ["id1", "id2", ...], ...}}
Resume-safe: existing output files are skipped. Retries 429/5xx with backoff.

Usage:
  python -X utf8 scripts/generate_ai_side.py                          # all
  python -X utf8 scripts/generate_ai_side.py --provider openrouter --model z-ai/glm-5.2:free
  python -X utf8 scripts/generate_ai_side.py --limit 3 --sections abstract   # pilot
"""
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEEDS = DATA / "seeds" / "seeds.json"
OUT = DATA / "ai"
MANIFEST = DATA / "manifest_ai.csv"

PROVIDERS = {
    "openrouter": {"base": "https://openrouter.ai/api/v1", "env": "OPENROUTER_API_KEY", "kind": "openai"},
    "openai":     {"base": "https://api.openai.com/v1",    "env": "OPENAI_API_KEY",    "kind": "openai"},
    "deepseek":   {"base": "https://api.deepseek.com/v1",  "env": "DEEPSEEK_API_KEY",  "kind": "openai"},
    "moonshot":   {"base": "https://api.moonshot.cn/v1",   "env": "MOONSHOT_API_KEY",  "kind": "openai"},
    "anthropic":  {"base": "https://api.anthropic.com/v1", "env": "ANTHROPIC_API_KEY", "kind": "anthropic"},
    "gemini":     {"base": "https://generativelanguage.googleapis.com/v1beta",
                   "env": "GEMINI_API_KEY", "kind": "gemini"},
}
SECTIONS = ["abstract", "introduction", "discussion"]
TASK = {
    "abstract": "Write the abstract of this manuscript.",
    "introduction": "Write the introduction of this manuscript (3-4 paragraphs, no subheadings).",
    "discussion": "Write the discussion of this manuscript (4-6 paragraphs, no subheadings).",
}


def load_models():
    models = {}
    cfg = ROOT / "config.json"
    if cfg.exists():
        models.update(json.loads(cfg.read_text(encoding="utf-8")).get("models", {}))
    return models


def build_prompt(seed, section):
    lines = [
        "You are drafting part of a research manuscript for submission to a peer-reviewed journal.",
        "",
        f"Article title: {seed['title']}",
        f"Journal: {seed['journal']} ({seed['year']})",
    ]
    if seed.get("keywords"):
        lines.append(f"Keywords: {seed['keywords']}")
    lines += ["", "Main findings (from the results section):", seed["results"], "", TASK[section]]
    if section == "abstract":
        labels = seed.get("abstract_labels") or []
        if labels:
            lines.append("The journal requires a structured abstract. Use exactly these "
                         f"section labels, each followed by its text: {', '.join(labels)}.")
        else:
            lines.append("Write a single unstructured paragraph without section labels.")
    lines.append("Do not invent facts that are not supported by the information above.")
    return "\n".join(lines)


def call_once(provider, model, prompt):
    cfg = PROVIDERS[provider]
    key = os.environ[cfg["env"]]
    kind = cfg["kind"]
    if kind == "openai":
        body = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}",
                   "X-Title": "deai-corpus-study"}
        req = urllib.request.Request(cfg["base"] + "/chat/completions",
                                     data=json.dumps(body).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=240) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"]
    if kind == "anthropic":
        body = {"model": model, "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt}]}
        req = urllib.request.Request(cfg["base"] + "/v1/messages",
                                     data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json",
                                              "x-api-key": key,
                                              "anthropic-version": "2023-06-01"})
        with urllib.request.urlopen(req, timeout=240) as r:
            return json.loads(r.read())["content"][0]["text"]
    if kind == "gemini":
        url = f"{cfg['base']}/models/{model}:generateContent?key={key}"
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=240) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    raise ValueError(kind)


def call_with_retry(provider, model, prompt, tries=10):
    delay = 4.0
    for i in range(tries):
        try:
            return call_once(provider, model, prompt)
        except urllib.error.HTTPError as e:
            transient = e.code in (408, 429, 500, 502, 503, 504)
            retry_after = e.headers.get("Retry-After") if e.headers else None
            if not transient or i == tries - 1:
                raise
            wait = float(retry_after) if retry_after else delay
            time.sleep(min(wait, 90) + random.uniform(0, 2))
            delay = min(delay * 1.7, 90)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if i == tries - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 1.7, 90)
    raise RuntimeError("unreachable")


def main():
    def argval(flag, default=None):
        return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

    limit = int(argval("--limit", "0"))
    cap = int(argval("--cap", "0"))  # max files per model per section; 0 = unlimited
    only_prov = argval("--provider")
    only_model = argval("--model")
    secs = (argval("--sections") or ",".join(SECTIONS)).split(",")

    models = load_models()
    seeds = json.loads(SEEDS.read_text(encoding="utf-8"))
    # deterministic shuffle so cap-limited runs cover all journals proportionally
    random.Random(42).shuffle(seeds)
    if limit:
        seeds = seeds[:limit]

    jobs = []  # (provider, model)
    for p, ms in models.items():
        if only_prov and p != only_prov:
            continue
        if not os.environ.get(PROVIDERS[p]["env"]):
            continue
        for m in ([ms] if isinstance(ms, str) else ms):
            if only_model and m != only_model:
                continue
            jobs.append((p, m))
    if not jobs:
        print("No (provider, model) jobs. Check env keys and config.json.")
        sys.exit(1)
    print("Jobs:", ", ".join(f"{p}/{m}" for p, m in jobs), flush=True)

    OUT.mkdir(parents=True, exist_ok=True)
    import csv
    new_manifest = not MANIFEST.exists()
    mf = open(MANIFEST, "a", newline="", encoding="utf-8-sig")
    wr = csv.writer(mf)
    if new_manifest:
        wr.writerow(["provider", "model", "section", "pmcid", "chars", "sec"])

    n_ok = n_fail = n_skip = 0
    for provider, model in jobs:
        mshort = model.replace("/", "_").replace(":", "-")
        for section in secs:
            d = OUT / mshort / section
            d.mkdir(parents=True, exist_ok=True)
            if cap and len(list(d.glob("*.md"))) >= cap:
                print(f"  [{model} / {section}] cap {cap} reached, skip", flush=True)
                continue
            for i, seed in enumerate(seeds):
                path = d / f"{seed['pmcid']}.md"
                if path.exists():
                    n_skip += 1
                    continue
                try:
                    text = call_with_retry(provider, model, build_prompt(seed, section))
                    if text and len(text) > 200:
                        path.write_text(text, encoding="utf-8")
                        wr.writerow([provider, model, section, seed["pmcid"], len(text),
                                     time.strftime("%Y-%m-%d %H:%M:%S")])
                        n_ok += 1
                    else:
                        n_fail += 1
                        print(f"[empty] {model}/{section}/{seed['pmcid']}", flush=True)
                except Exception as e:  # noqa: BLE001
                    n_fail += 1
                    print(f"[fail] {model}/{section}/{seed['pmcid']}: "
                          f"{type(e).__name__} {str(e)[:140]}", flush=True)
                    time.sleep(5)
                if (n_ok + n_fail) % 25 == 0 and n_ok + n_fail:
                    mf.flush()
                    print(f"  [{model} / {section}] {i + 1}/{len(seeds)} "
                          f"(ok={n_ok} fail={n_fail} skip={n_skip})", flush=True)
                time.sleep(0.4)
    mf.close()
    print(f"DONE ok={n_ok} fail={n_fail} skip={n_skip}", flush=True)


if __name__ == "__main__":
    main()
