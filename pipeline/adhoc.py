def journal_with_most_drugs(graph: list[dict]) -> str:
    journal_drugs = {}

    for entry in graph:
        drug = entry["drug"]
        for mention in entry["pubmed"] + entry["clinical_trials"]:
            journal = mention["journal"]
            journal_drugs.setdefault(journal, set()).add(drug)

    return max(journal_drugs, key=lambda j: len(journal_drugs[j]))


def related_drugs_via_pubmed(graph: list[dict], drug_name: str) -> set[str]:
    pubmed_journals = set()

    for entry in graph:
        if entry["drug"] == drug_name:
            for mention in entry["pubmed"]:
                pubmed_journals.add(mention["journal"])

    related_drugs = set()

    for entry in graph:
        drug = entry["drug"]

        if drug == drug_name:
            continue

        for mention in entry["pubmed"]:
            if mention["journal"] in pubmed_journals:
                related_drugs.add(drug)

    clinical_trials_drugs = set()

    for entry in graph:
        drug = entry["drug"]

        for mention in entry["clinical_trials"]:
            if mention["journal"] in pubmed_journals:
                clinical_trials_drugs.add(drug)

    return related_drugs - clinical_trials_drugs