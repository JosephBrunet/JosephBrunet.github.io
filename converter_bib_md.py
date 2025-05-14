import os
from pathlib import Path
from collections import defaultdict
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

# === Configuration ===
bib_file = "publications.bib"
output_path = "content/publications/_index.md"

# === Create output folder if needed ===
Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)

# === Load and parse the BibTeX file ===
with open(bib_file, encoding="utf-8") as bibtex_file:
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    bib_database = bibtexparser.load(bibtex_file, parser=parser)

# === Group entries by year ===
by_year = defaultdict(list)
for entry in bib_database.entries:
    pub = {
        "title": entry.get("title", "Untitled").strip().replace("\n", " "),
        "authors": entry.get("author", "Unknown").strip().replace("\n", " "),
        "journal": entry.get("journal") or entry.get("booktitle") or entry.get("publisher", "Unknown"),
        "doi": entry.get("doi", entry.get("eprint", "")).strip(),
        "note": entry.get("note", "").strip(),
    }
    year = entry.get("year", "n.d.").strip()
    by_year[year].append(pub)

# === Format a single publication entry ===
def format_publication(pub, year):
    authors = pub["authors"].split(' and ')
    
    authors_reduced = []
    me_flag = False
    for idx, author in enumerate(authors):
        if idx < 3 or me_flag is False:
            authors_reduced.append(author)
            if "brunet" in author.lower():
                me_flag = True
    
    authors_formatted = ", ".join(f"**{a.strip()}**" if "Brunet" in a else a.strip() for a in authors_reduced)
    authors_formatted += ", et al."


    # authors_formatted = ", ".join(f"**{a.strip()}**" if "Brunet" in a else a.strip() for a in authors)


    line = f"- {authors_formatted}, {pub['title']}, _{pub['journal']}_"
    line += f", {year}"
    if pub["note"]:
        line += f" **({pub['note']})**"


    if pub["doi"]:
        doi_url = pub["doi"] if pub["doi"].startswith("http") else f"https://doi.org/{pub['doi']}"
        line += f". <a href='{doi_url}' class='text-link'><i class='fas fa-solid fa-file'></i> {pub['doi']}</a>"

    return line + "\n"

# === Write the Markdown index file ===
with open(output_path, "w", encoding="utf-8") as f:
    f.write("""---
title: "Publications"
---

You can also find my scientific publications on <a href="https://scholar.google.com/citations?user=7T_yo4UAAAAJ" class="text-link">Google Scholar</a>
""")
    for year in sorted(by_year.keys(), reverse=True):
        f.write(f"### {year}\n\n")
        for pub in by_year[year]:
            # f.write("<div class='pub-entry'>" + "\n")
            f.write(format_publication(pub, year) + "\n")
            # f.write("</div>" + "\n")


print(f"✅ Successfully created {output_path} with {sum(len(p) for p in by_year.values())} publications.")
