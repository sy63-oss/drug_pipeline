from pipeline.transformer import find_mentions

def test_find_mentions_pubmed():
    publications = [
        {"title": "Effect of betamethasone on patients", "journal": "Journal A", "date": "2020-01-01"},
        {"title": "Study on aspirin", "journal": "Journal B", "date": "2020-01-01"},
    ]
    drugs = [{"drug": "BETAMETHASONE"}, {"drug": "ASPIRIN"}]

    mentions = find_mentions(publications, drugs, source="pubmed")

    assert len(mentions) == 2
    assert mentions[0]["drug"] == "BETAMETHASONE"
    assert mentions[0]["source"] == "pubmed"
