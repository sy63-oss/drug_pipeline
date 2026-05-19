

def find_mentions(publications: list[dict], drugs: list[dict], source: str) -> list[dict]:
    """Fonction permettant de détecter les mentions des médicaments dans les titres"""
    mentions = []

    for drug in drugs:
        drug_name = drug["drug"]

        for pub in publications:
            title = pub.get("title","")

            if drug_name.lower() in title.lower():
                mentions.append({
                    "drug": drug_name,
                    "journal": pub["journal"],
                    "date": pub["date"],
                    "source": source  # "pubmed" ou "clinical_trials"
                })
    return mentions


