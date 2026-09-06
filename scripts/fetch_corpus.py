#!/usr/bin/env python3
"""Fetch human-side corpus (2018-2022.6, CC-BY biomedical) from Europe PMC.

For every accepted article:
  - save human-written sections: abstract (unstructured) / introduction / discussion
    to data/human/<section>/<pmcid>.md
  - export AI-side generation facts (title, keywords, results extract) to
    data/seeds/seeds.json   -> paired design: same PMCID on both sides
  - append a manifest row (PMCID/DOI/journal/year/license/word counts)

Usage:
  python -X utf8 scripts/fetch_corpus.py            # full run
  python -X utf8 scripts/fetch_corpus.py --pilot    # 3 journals, tiny caps
"""
import csv
import json
import random
import re
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HUM = DATA / "human"
SECTIONS = ["abstracts", "introductions", "discussions"]

JOURNALS = [
    "Journal of Translational Medicine", "Molecular Cancer", "BMC Cancer",
    "Cancers", "Frontiers in Oncology", "Cell Death & Disease", "BMC Medicine",
    "Scientific Reports", "Nature Communications", "eLife", "PLOS Biology",
    "Breast Cancer Research", "Journal of Experimental & Clinical Cancer Research",
    "Cancer Communications", "Cell Death Discovery", "Genome Medicine",
    "Cancer Cell International",
]
DATE_Q = "FIRST_PDATE:[2018-01-01 TO 2022-06-30]"
N_HUMAN, N_SEED = 45, 10
MINW = {"abstracts": 80, "introductions": 120, "discussions": 120}
MAXW_ABSTRACT = 400
LICENSE_OK = {"by", "by-sa"}
DROP_LOCAL = {"math", "graphic", "inline-graphic", "tex-math", "private-char"}
BAD_TITLE = re.compile(r"systematic review|meta[- ]analysis|scoping review", re.I)
CC_RE = re.compile(r"creativecommons\.org/licenses/([a-z\-]+)")

WORD = re.compile(r"[A-Za-z][A-Za-z'\u2019-]*")


def http_get(url, timeout=45, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "deai-corpus-study/0.1"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def search_journal(journal):
    q = (f'(JOURNAL:"{journal}") AND (OPEN_ACCESS:Y) AND (HAS_FULLTEXT:Y) '
         f'AND {DATE_Q} AND NOT (ARTICLE_TYPE:"review article")')
    url = (f"{BASE}/search?query={urllib.parse.quote(q)}&format=json"
           f"&pageSize=1000&resultType=core")
    d = json.loads(http_get(url))
    out = []
    for doc in d.get("resultList", {}).get("result", []):
        pmcid = doc.get("pmcid", "")
        if pmcid.startswith("PMC") and doc.get("title") and not BAD_TITLE.search(doc["title"]):
            out.append(doc)
    return out


def local(tag):
    return tag.rsplit("}", 1)[-1]


def strip_to_text(el):
    """Element -> plain text, dropping math/graphics."""
    parts = []
    def walk(e):
        if local(e.tag) in DROP_LOCAL:
            return
        if e.text:
            parts.append(e.text)
        for c in e:
            walk(c)
            if c.tail:
                parts.append(c.tail)
    walk(el)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def build_parents(root):
    return {c: p for p in root.iter() for c in p}


def in_bad_container(p, parents):
    e = parents.get(p)
    while e is not None:
        if local(e.tag) in {"fig", "table-wrap", "caption", "speech", "statement"}:
            return True
        e = parents.get(e)
    return False


def find_sec(body, types, title_rx, parents):
    for sec in body.iter("sec"):
        st = (sec.get("sec-type") or "").lower()
        t_el = sec.find("title")
        title = strip_to_text(t_el).lower() if t_el is not None else ""
        if st in types or title_rx.search(title):
            paras = [strip_to_text(p) for p in sec.iter("p")
                     if in_bad_container(p, parents) is False]
            paras = [p for p in paras if p and WORD.match(p)]
            return paras
    return []


def parse_article(xml_bytes):
    root = ET.fromstring(xml_bytes)
    parents = build_parents(root)

    title_el = root.find(".//article-title")
    title = strip_to_text(title_el) if title_el is not None else ""
    doi = ""
    for aid in root.iter("article-id"):
        if aid.get("pub-id-type") == "doi":
            doi = (aid.text or "").strip()
    journal = ""
    jt = root.find(".//journal-title")
    if jt is not None:
        journal = strip_to_text(jt)
    year = ""
    y = root.find(".//article-meta//year")
    if y is None:
        y = root.find(".//year")
    if y is not None and y.text:
        year = y.text
    kw = [strip_to_text(k) for k in root.iter("kwd") if strip_to_text(k)]
    m = CC_RE.search(xml_bytes.decode("utf-8", "ignore"))
    license = m.group(1) if m else ""

    abstract = ""
    abstract_structured = False
    abstract_labels = []
    for ab in root.iter("abstract"):
        if (ab.get("abstract-type") or "") in ("graphical", "graphical-abstract"):
            continue
        labels = [strip_to_text(x) for x in ab
                  if local(x.tag) in ("title", "label") and strip_to_text(x)]
        paras = [strip_to_text(p) for p in ab.iter("p") if strip_to_text(p)]
        abstract_structured = bool(labels)
        abstract_labels = labels
        abstract = "\n\n".join(paras) if paras else strip_to_text(ab)
        break

    body = root.find(".//body")
    intro = find_sec(body, {"intro", "introduction"},
                     re.compile(r"^(introduction|background)\b"), parents) if body is not None else []
    disc = find_sec(body, {"discussion", "conclusion", "conclusions"},
                    re.compile(r"^(discussion|conclusion)"), parents) if body is not None else []
    results = find_sec(body, {"results", "result"},
                       re.compile(r"^results?\b"), parents) if body is not None else []

    return {
        "title": title, "doi": doi, "journal": journal, "year": year,
        "keywords": "; ".join(kw[:8]), "license": license,
        "abstract": abstract, "abstract_structured": abstract_structured,
        "abstract_labels": abstract_labels,
        "introduction": "\n\n".join(intro), "discussion": "\n\n".join(disc),
        "results": " ".join(results),
    }


def wc(text):
    return len(WORD.findall(text))


def main():
    pilot = "--pilot" in sys.argv
    rng = random.Random(42)
    if pilot:
        journals, n_human, n_seed = JOURNALS[:3], 6, 3
    else:
        journals, n_human, n_seed = JOURNALS, N_HUMAN, N_SEED

    for s in SECTIONS:
        (HUM / s).mkdir(parents=True, exist_ok=True)
    (DATA / "seeds").mkdir(parents=True, exist_ok=True)

    manifest_path = DATA / "manifest.csv"
    seeds_path = DATA / "seeds" / "seeds.json"
    manifest_f = open(manifest_path, "w", newline="", encoding="utf-8-sig")
    wr = csv.writer(manifest_f)
    wr.writerow(["pmcid", "journal", "year", "doi", "license", "kept_abstract",
                 "kept_intro", "kept_disc", "w_abstract", "w_intro", "w_disc",
                 "in_seeds", "abstract_structured", "title"])
    seeds, seen = [], set()
    stats = {"fetched": 0, "bad_license": 0, "no_body": 0, "parse_err": 0,
             "kept_abstract": 0, "kept_intro": 0, "kept_disc": 0}

    for jname in journals:
        try:
            docs = search_journal(jname)
        except Exception as e:  # noqa: BLE001
            print(f"[search-fail] {jname}: {e}", flush=True)
            continue
        rng.shuffle(docs)
        take = docs[: n_human + n_seed]
        print(f"[{jname}] hits={len(docs)} fetch={len(take)}", flush=True)

        for doc in take:
            pmcid = doc["pmcid"]
            if pmcid in seen:
                continue
            seen.add(pmcid)
            try:
                xml_bytes = http_get(f"{BASE}/{pmcid}/fullTextXML")
                art = parse_article(xml_bytes)
                stats["fetched"] += 1
            except Exception as e:  # noqa: BLE001
                stats["parse_err"] += 1
                wr.writerow([pmcid, jname, doc.get("pubYear", ""), "", "", 0, 0, 0,
                             0, 0, 0, 0, 0, f"ERROR {type(e).__name__}"])
                continue
            if art["license"] not in LICENSE_OK:
                stats["bad_license"] += 1
                wr.writerow([pmcid, art["journal"] or jname, art["year"], art["doi"],
                             art["license"], 0, 0, 0, 0, 0, 0, 0, 0, art["title"][:120]])
                continue

            kept = {"abstracts": 0, "introductions": 0, "discussions": 0}
            ab = art["abstract"]
            wa = wc(ab)
            if ab and MINW["abstracts"] <= wa <= MAXW_ABSTRACT:
                (HUM / "abstracts" / f"{pmcid}.md").write_text(ab, encoding="utf-8")
                kept["abstracts"], stats["kept_abstract"] = 1, stats["kept_abstract"] + 1
            wi = wc(art["introduction"])
            if wi >= MINW["introductions"]:
                (HUM / "introductions" / f"{pmcid}.md").write_text(art["introduction"], encoding="utf-8")
                kept["introductions"], stats["kept_intro"] = 1, stats["kept_intro"] + 1
            wd = wc(art["discussion"])
            if wd >= MINW["discussions"]:
                (HUM / "discussions" / f"{pmcid}.md").write_text(art["discussion"], encoding="utf-8")
                kept["discussions"], stats["kept_disc"] = 1, stats["kept_disc"] + 1

            res_w = wc(art["results"])
            if res_w >= 60:
                cut = art["results"]
                if len(cut) > 2400:
                    cut = cut[:2400].rsplit(" ", 1)[0] + " ..."
                seeds.append({"pmcid": pmcid, "journal": art["journal"], "year": art["year"],
                              "title": art["title"], "keywords": art["keywords"],
                              "results": cut,
                              "abstract_labels": art["abstract_labels"]})

            wr.writerow([pmcid, art["journal"] or jname, art["year"], art["doi"],
                         art["license"], kept["abstracts"], kept["introductions"],
                         kept["discussions"], wa, wi, wd, 1 if res_w >= 60 else 0,
                         1 if art["abstract_structured"] else 0, art["title"][:120]])
            time.sleep(0.12)
        manifest_f.flush()

    manifest_f.close()
    seeds_path.write_text(json.dumps(seeds, ensure_ascii=False, indent=1), encoding="utf-8")
    stats["seeds"] = len(seeds)
    (DATA / "fetch_summary.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    print("DONE", json.dumps(stats), flush=True)


if __name__ == "__main__":
    main()
