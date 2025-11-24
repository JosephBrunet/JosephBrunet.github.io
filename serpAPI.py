import os
import json
import re
from pathlib import Path

import requests
import yaml


SERPAPI_KEY = "70a043ec264d8041ba24facd8d5cb834e4e112e23abc4849a6487b25915393b8"
AUTHOR_ID = "7T_yo4UAAAAJ&hl=en&oi=ao" 


# =========================
# SerpAPI - Google Scholar
# =========================

def fetch_scholar_profile(author_id: str) -> dict:
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_scholar_author",
        "author_id": author_id,
        "hl": "en",
        "num": 200,        # ask for up to 100 articles
        "sort": "pubdate", # optional, sort by year instead of citations
    }
    r = requests.get("https://serpapi.com/search", params=params, timeout=20)
    r.raise_for_status()
    return r.json()



# =============
# Crossref API
# =============

def crossref_lookup(title: str) -> dict:
    url = "https://api.crossref.org/works"
    params = {
        "query.bibliographic": title,
        "rows": 1,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
    except Exception:
        return {}

    data = r.json()
    items = data.get("message", {}).get("items", [])
    if not items:
        return {}

    item = items[0]

    # Year
    year = None
    for key in ("published-print", "published-online", "issued"):
        date_parts = item.get(key, {}).get("date-parts")
        if date_parts and len(date_parts[0]) > 0:
            year = date_parts[0][0]
            break

    # Authors "Given Family"
    authors = []
    for a in item.get("author", []):
        name = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        if name:
            authors.append(name)

    container = item.get("container-title") or []
    journal = container[0] if container else None

    return {
        "doi": item.get("DOI"),
        "journal": journal,
        "volume": item.get("volume"),
        "issue": item.get("issue"),
        "pages": item.get("page"),
        "year": year,
        "authors": authors,
        "type": item.get("type"),  # e.g. "journal-article"
    }


def crossref_to_bibtex_type(cr_type: str) -> str:
    if not cr_type:
        return "article"
    mapping = {
        "journal-article": "article",
        "proceedings-article": "inproceedings",
        "proceedings-paper": "inproceedings",
        "posted-content": "article",      # bioRxiv, arXiv
        "dissertation": "phdthesis",
        "thesis": "phdthesis",
    }
    return mapping.get(cr_type, "article")


# =====================
# Author info for JSON
# =====================

def build_author_info(raw: dict) -> dict:
    author = raw.get("author", {})
    cited_by = raw.get("cited_by", {})
    table = cited_by.get("table", [])
    metrics = table[0] if table else {}

    citations = metrics.get("citations", {}) or {}
    h_index = metrics.get("h_index", {}) or {}
    i10_index = metrics.get("i10_index", {}) or {}

    return {
        "name": author.get("name"),
        "affiliation": author.get("affiliations"),
        "interests": author.get("interests"),
        "profile_link": author.get("link"),
        "thumbnail": author.get("thumbnail"),
        "citations_all": citations.get("all"),
        "citations_since_2019": citations.get("since_2019"),
        "h_index_all": h_index.get("all"),
        "h_index_since_2019": h_index.get("since_2019"),
        "i10_index_all": i10_index.get("all"),
        "i10_index_since_2019": i10_index.get("since_2019"),
    }


# ======================
# Publications for JSON
# ======================

def merge_field(primary, secondary):
    """
    Keep 'primary' if it is non empty.
    Use secondary only if primary is None, empty string, or empty list.
    """
    if primary is None:
        return secondary
    if isinstance(primary, str) and primary.strip() == "":
        return secondary
    if isinstance(primary, list) and len(primary) == 0:
        return secondary
    return primary


def build_publications(raw: dict, overrides: dict) -> list:
    pubs = []

    for pub in raw.get("articles", []):
        title = pub.get("title")
        if not title:
            continue
        
        # ---- Google Scholar data (primary source) ----
        gs_authors_str = pub.get("authors")
        gs_authors = [a.strip() for a in gs_authors_str.split(",")] if gs_authors_str else []
        gs_year = pub.get("year")
        gs_publication = pub.get("publication")  # "bioRxiv, 2023.03...", "arXiv preprint...", etc.
        gs_citations = pub.get("cited_by", {}).get("value")
        gs_url = pub.get("link")

        # Detect preprint from Scholar publication string
        pub_lower = (gs_publication or "").lower()
        is_preprint = any(x in pub_lower for x in ["biorxiv", "bioRxiv", "arxiv"])

        # ---- Crossref secondary enrichment ----
        cr = crossref_lookup(title)

        # Determine BibTeX type
        bibtex_type = crossref_to_bibtex_type(cr.get("type"))

        # -----------------------
        # Journal / booktitle
        # -----------------------
        if is_preprint:
            # Trust Scholar for preprints
            journal = gs_publication
        else:
            # Prefer Crossref's clean journal name, fallback to Scholar
            journal = cr.get("journal") or gs_publication

        # For proceedings, move journal → booktitle
        booktitle = None
        if bibtex_type == "inproceedings":
            booktitle = journal
            journal = None

        # Normalize journal for preprints (bioRxiv/arXiv shortened)
        if journal:
            jlow = journal.lower()
            if "biorxiv" in jlow:
                journal = "bioRxiv"
            elif "arxiv" in jlow:
                journal = "arXiv"

        # -----------------------
        # Authors
        # -----------------------
        authors = merge_field(gs_authors, cr.get("authors"))

        # -----------------------
        # Year
        # -----------------------
        if is_preprint:
            # For preprints, keep Scholar's year, ignore Crossref "final" year
            year = gs_year
        else:
            year = merge_field(gs_year, cr.get("year"))

        # 🔹 FILTER: skip papers before 2019
        year_int = None
        try:
            if year is not None:
                year_int = int(year)
        except (TypeError, ValueError):
            year_int = None

        if year_int is not None and year_int < 2019:
            continue

        # -----------------------
        # Volume / issue / pages
        # -----------------------
        if is_preprint:
            # Preprints do not meaningfully have these; avoid Crossref pollution
            volume = None
            issue = None
            pages = None
        else:
            volume = cr.get("volume")
            issue = cr.get("issue")
            pages = cr.get("pages")

        # -----------------------
        # DOI (more strict for preprints)
        # -----------------------
        cr_doi = cr.get("doi")

        if is_preprint:
            doi = None
            if cr_doi:
                dlow = cr_doi.lower()
                # Accept only typical preprint DOIs
                if dlow.startswith("10.1101") or "arxiv" in dlow:
                    doi = cr_doi
        else:
            doi = cr_doi

        # ---- Overrides ----
        override_key = doi or title
        override = overrides.get(override_key, {})

        entry = {
            "title": title,
            "authors": authors,
            "journal": journal,
            "booktitle": booktitle,
            "year": year,
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi": doi,
            "citations": gs_citations,
            "url": gs_url,
            "note": override.get("note"),
            "role": override.get("role"),
            "bibtex_type": bibtex_type,
        }
        pubs.append(entry)

    # ---- Sort by year ----
    def sort_key(p):
        y = p.get("year")
        try:
            return int(y)
        except:
            return -1

    pubs.sort(key=sort_key, reverse=True)
    return pubs





# ==================
# BibTex generation
# ==================

def make_cite_key(pub: dict, existing_keys: set) -> str:
    """Generate something like brunet2024multidimensional, ensure uniqueness."""
    year = pub.get("year") or ""
    try:
        year_str = str(int(year))
    except (TypeError, ValueError):
        year_str = ""

    authors = pub.get("authors") or []
    if authors:
        first_author = authors[0]
    else:
        first_author = "unknown"

    # Take last word as surname
    last_name = first_author.split()[-1]
    last_name = re.sub(r"[^A-Za-z]", "", last_name).lower()

    title = pub.get("title") or ""
    m = re.search(r"\b\w+\b", title)
    first_word = m.group(0).lower() if m else ""

    base = ""
    if last_name and year_str:
        base = f"{last_name}{year_str}{first_word}"
    elif last_name:
        base = f"{last_name}{first_word}"
    else:
        base = "pub"

    key = base or "pub"
    if key not in existing_keys:
        existing_keys.add(key)
        return key

    # If duplicate, add letters a, b, c...
    suffix_ord = ord("a")
    while True:
        candidate = f"{base}{chr(suffix_ord)}"
        if candidate not in existing_keys:
            existing_keys.add(candidate)
            return candidate
        suffix_ord += 1


def publications_to_bibtex(publications: list) -> str:
    lines = []
    existing_keys = set()

    for pub in publications:
        entry_type = pub.get("bibtex_type", "article")
        key = make_cite_key(pub, existing_keys)

        lines.append(f"@{entry_type}{{{key},")

        def add_field(field_name: str, value):
            if not value:
                return
            value_str = str(value).replace("\n", " ")
            lines.append(f"  {field_name} = {{{value_str}}},")

        add_field("title", pub["title"])
        add_field("author", " and ".join(pub.get("authors", [])))

        if entry_type == "inproceedings":
            add_field("booktitle", pub.get("booktitle"))
        else:
            add_field("journal", pub.get("journal"))

        add_field("year", pub.get("year"))
        add_field("volume", pub.get("volume"))
        add_field("number", pub.get("issue"))
        add_field("pages", pub.get("pages"))
        add_field("doi", pub.get("doi"))
        add_field("note", pub.get("note"))
        add_field("url", pub.get("url"))

        # Remove trailing comma from last field
        if lines[-1].endswith(","):
            lines[-1] = lines[-1][:-1]
        lines.append("}\n")

    return "\n".join(lines)


# =====
# MAIN
# =====

def main():
    if not SERPAPI_KEY:
        raise RuntimeError("Please set SERPAPI_KEY environment variable.")

    # Adjust this if serpAPI.py is not inside your Hugo repo
    data_dir = Path(__file__).resolve().parent

    # Optional overrides for note/role, keyed by DOI or title
    overrides_path = data_dir / "publication_overrides.yaml"
    if overrides_path.exists():
        overrides = yaml.safe_load(overrides_path.read_text(encoding="utf-8")) or {}
    else:
        overrides = {}

    raw = fetch_scholar_profile(AUTHOR_ID)

    author_info = build_author_info(raw)
    publications = build_publications(raw, overrides)

    # # 1) Publications JSON for Hugo
    # publications_json_path = data_dir / "publications.json"
    # publications_json_path.write_text(
    #     json.dumps(publications, indent=2),
    #     encoding="utf-8",
    # )
    # print(f"Wrote {publications_json_path}")

    # # 2) Author JSON for Hugo
    # author_json_path = data_dir / "author.json"
    # author_json_path.write_text(
    #     json.dumps(author_info, indent=2),
    #     encoding="utf-8",
    # )
    # print(f"Wrote {author_json_path}")

    # 3) BibTeX file
    bibtex = publications_to_bibtex(publications)
    bib_dir = data_dir
    bib_dir.mkdir(parents=True, exist_ok=True)
    bib_path = bib_dir / "publications.bib"
    bib_path.write_text(bibtex, encoding="utf-8")
    print(f"Wrote {bib_path}")


if __name__ == "__main__":
    main()