from scholarly import scholarly

def get_exact_author(full_name):
    search_query = scholarly.search_author(full_name)
    for author in search_query:
        if author.get("name", "").lower() == full_name.lower():
            return scholarly.fill(author)
    return None

def save_publications_to_bibtex(author_data, output_file="publications.bib"):
    with open(output_file, "w", encoding="utf-8") as bibfile:
        for i, pub in enumerate(author_data['publications']):
            pub_filled = scholarly.fill(pub)
            bib = pub_filled.get('bib', {})
            title = bib.get('title', 'Untitled')
            year = bib.get('pub_year', 'n.d.')
            authors = bib.get('author', 'Unknown').replace('\n', ' ')
            journal = bib.get('journal', bib.get('publisher', 'Unknown'))
            entry_type = "article"
            key = f"brunet{i+1}"

            bib_entry = f"@{entry_type}{{{key},\n" \
                        f"  title={{ {title} }},\n" \
                        f"  author={{ {authors} }},\n" \
                        f"  journal={{ {journal} }},\n" \
                        f"  year={{ {year} }}\n" \
                        f"}}\n\n"

            bibfile.write(bib_entry)

    print(f"\n✅ Saved {len(author_data['publications'])} publications to '{output_file}'")

def print_author_info(author_data):
    print(f"\n👤 Name: {author_data['name']}")
    print(f"🏢 Affiliation: {author_data.get('affiliation', 'N/A')}")
    print(f"📈 h-index: {author_data.get('hindex', 'N/A')}")
    print(f"📊 Total Citations (from profile): {author_data.get('citedby', 'N/A')}\n")

    total_citations = 0
    print("📚 Publications:\n")
    for i, pub in enumerate(author_data['publications']):
        pub_filled = scholarly.fill(pub)
        title = pub_filled['bib'].get('title', 'Untitled')
        year = pub_filled['bib'].get('pub_year', 'N/A')
        citations = pub_filled.get('num_citations', 0)
        total_citations += citations
        print(f"{i+1}. \"{title}\" ({year}) — 📑 Citations: {citations}")

    print(f"\n🧮 Total Citations (recalculated): {total_citations}")

# === MAIN ===

author = get_exact_author("Joseph Brunet")
if author:
    print_author_info(author)
    save_publications_to_bibtex(author)
else:
    print("❌ Author not found.")
