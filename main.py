from pipeline.ingestion import load_pubmed_json, load_clinical_trials,load_drugs,load_pubmed_csv
from pipeline.builder import build_graph
from pipeline.transformer import find_mentions
import json
from pathlib import Path
from pipeline.logger import get_logger
logger = get_logger(__name__)
#  Détecter les mentions

drugs           = load_drugs("data/drugs.csv")
pubmed_json     = load_pubmed_json("data/pubmed.json")
pubmed_csv      = load_pubmed_csv("data/pubmed.csv")
clinical_trials = load_clinical_trials("data/clinical_trials.csv")

pubmed_mentions = find_mentions(pubmed_csv + pubmed_json, drugs, source="pubmed")
ct_mentions     = find_mentions(clinical_trials, drugs, source="clinical_trials")

# Fusionner
all_mentions = pubmed_mentions + ct_mentions

# Construire le graphe
graph = build_graph(all_mentions)

output_path = Path("output/graph.json")
output_path.parent.mkdir(exist_ok=True)   # crée le dossier output/ s'il n'existe pas

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(graph, f, indent=2, ensure_ascii=False)

logger.info("Graphe généré : %s (%d médicaments)", output_path, len(graph))

