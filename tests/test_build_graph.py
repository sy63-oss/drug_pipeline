from pipeline.builder import build_graph

def test_build_graph_groups_by_drug():
    mentions = [
        {"drug": "BETAMETHASONE", "journal": "Journal A", "date": "2020-01-01", "source": "pubmed"},
        {"drug": "BETAMETHASONE", "journal": "Journal B", "date": "2020-01-03", "source": "clinical_trials"},
        {"drug": "ATROPINE",      "journal": "Journal A", "date": "2020-01-01", "source": "pubmed"},
    ]

    result = build_graph(mentions)

    assert len(result) == 2                          # 2 médicaments distincts
    beta = next(r for r in result if r["drug"] == "BETAMETHASONE")
    assert len(beta["pubmed"]) == 1
    assert len(beta["clinical_trials"]) == 1
