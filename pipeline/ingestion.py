import csv
from pathlib import Path
import re
import json
from pipeline.utils import normalize_date


def load_drugs(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_clinical_trials(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        records= list(csv.DictReader(f))
    for record in records:
        record["title"] = record.pop("scientific_title")
        record["date"] = normalize_date(record["date"])
    return records

def load_pubmed_csv(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    records = [r for r in records if r.get("date")]   # ← filtre les lignes vides
    for record in records:
        record["date"] = normalize_date(record["date"])
    return records

def load_pubmed_json(path: str | Path) -> list[dict]:
    """Charge pubmed.json en corrigeant les virgules finales et les IDs manquants."""
    text = Path(path).read_text(encoding="utf-8")
    #1. Supprimer les virgules finales avant  ] ou } (JSON invalide)
    text = re.sub(r",\s*(\]|\})",r"\1", text)
    records = json.loads(text)
    last_id = 0  # on garde une trace de l'id précédent

    for record in records:
        raw_id = record.get("id")

        if raw_id is None or str(raw_id).strip() == "":
            record["id"] = last_id + 1   # incrémente le précédent
        else:
            record["id"] = int(raw_id)   # normalise string → int

        last_id = record["id"]
        record["date"] = normalize_date(record["date"])
    return records
