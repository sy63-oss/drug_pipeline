from pipeline.ingestion import load_pubmed_json, load_pubmed_csv, load_clinical_trials
from pipeline.utils import normalize_date
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
# __file__         → /workspaces/drug_pipeline/tests/test_ingestion.py
# .parent          → /workspaces/drug_pipeline/tests/
# .parent.parent   → /workspaces/drug_pipeline/

def test_normalize_date_formats():
    assert normalize_date("01/01/2020") == "2020-01-01"
    assert normalize_date("2020-01-01") == "2020-01-01"
    assert normalize_date("1 January 2020") == "2020-01-01"

def test_pubmed_json_missing_id():
    records = load_pubmed_json(DATA_DIR / "pubmed.json")
    ids = [r["id"] for r in records]
    assert 13 in ids          # l'ID vide a bien été incrémenté

def test_pubmed_json_id_types():
    records = load_pubmed_json(DATA_DIR / "pubmed.json")
    assert all(isinstance(r["id"], int) for r in records)
