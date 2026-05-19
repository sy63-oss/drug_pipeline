from pipeline.adhoc import journal_with_most_drugs, related_drugs_via_pubmed

GRAPH = [
    {
        "drug": "BETAMETHASONE",
        "pubmed": [
            {"journal": "Journal A", "date": "2020-01-01"},
            {"journal": "Journal B", "date": "2020-01-01"},
        ],
        "clinical_trials": [
            {"journal": "Journal C", "date": "2020-01-01"},
        ],
    },
    {
        "drug": "ATROPINE",
        "pubmed": [
            {"journal": "Journal A", "date": "2020-01-01"},
        ],
        "clinical_trials": [],
    },
    {
        "drug": "EPINEPHRINE",
        "pubmed": [],
        "clinical_trials": [
            {"journal": "Journal A", "date": "2020-01-01"},
        ],
    },
]

def test_journal_with_most_drugs():
    assert journal_with_most_drugs(GRAPH) == "Journal A"  # mentionné par 2 drugs

def test_related_drugs_via_pubmed():
    result = related_drugs_via_pubmed(GRAPH, "BETAMETHASONE")
    assert "ATROPINE" in result        # partage Journal A via PubMed
    assert "EPINEPHRINE" not in result # Journal A via Clinical Trials seulement
    assert "BETAMETHASONE" not in result
