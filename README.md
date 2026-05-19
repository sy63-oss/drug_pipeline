# Drug Pipeline

Pipeline de données Python qui analyse les mentions de médicaments dans des publications scientifiques (PubMed) et des essais cliniques (Clinical Trials), et produit un graphe de liaison au format JSON.

## Fonctionnement

```
Ingestion → Nettoyage → Détection des mentions → Graphe JSON
```

Pour chaque médicament, le pipeline détecte ses mentions dans les titres des publications et les regroupe par journal et par source (PubMed ou Clinical Trials).

## Structure du projet

```
drug_pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── logger.py         ← logging centralisé
│   ├── ingestion.py      ← chargement et nettoyage des données
│   ├── utils.py          ← normalize_date (réutilisable)
│   ├── transformer.py    ← détection des mentions dans les titres
│   ├── builder.py        ← construction du graphe JSON
│   └── adhoc.py          ← requêtes analytiques ad-hoc
├── dags/
│   └── drug_pipeline_dag.py   ← orchestration Airflow
├── data/
│   ├── drugs.csv
│   ├── pubmed.csv
│   ├── pubmed.json
│   └── clinical_trials.csv
├── tests/
├── Dockerfile
└── main.py
```

## Installation

```bash
git clone <repo-url>
cd drug_pipeline

python -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate

pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

Le résultat est généré dans `output/graph.json`.

## Tests

```bash
pytest tests/ -v
```

## Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow_home
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags

airflow db init
airflow users create --username admin --password admin \
    --firstname Admin --lastname Admin \
    --role Admin --email admin@example.com

# Terminal 1
airflow webserver --port 8080

# Terminal 2
airflow scheduler
```

Interface disponible sur `http://localhost:8080`.

## Docker

```bash
docker build -t drug-pipeline .
docker run drug-pipeline
```

## Format de sortie

```json
[
  {
    "drug": "BETAMETHASONE",
    "pubmed": [
      { "journal": "Journal of back and musculoskeletal rehabilitation", "date": "2020-01-01" }
    ],
    "clinical_trials": [
      { "journal": "Hôpitaux Universitaires de Genève", "date": "2020-01-01" }
    ]
  }
]
```

## Fonctions ad-hoc

```python
from pipeline.adhoc import journal_with_most_drugs, related_drugs_via_pubmed
import json

with open("output/graph.json") as f:
    graph = json.load(f)

# Journal citant le plus de médicaments différents
print(journal_with_most_drugs(graph))

# Médicaments co-mentionnés via PubMed uniquement
print(related_drugs_via_pubmed(graph, "BETAMETHASONE"))
```

## Choix techniques

**Nettoyage à l'ingestion**
Les dates sont normalisées en `YYYY-MM-DD` et les champs hétérogènes (`scientific_title` → `title`) sont standardisés dès le chargement. Les couches suivantes reçoivent toujours des données propres, sans connaître les particularités de chaque source.

**Séparation des responsabilités**
`utils.py` contient des fonctions génériques réutilisables par d'autres pipelines. `transformer.py` et `builder.py` sont indépendants des sources de données — ils reçoivent des listes de dicts standardisées.

**Dict temporaire dans `build_graph`**
Regrouper les mentions dans un `dict {drug: {...}}` permet une recherche en O(1) à chaque itération, contre O(n) si on cherchait dans une liste. Converti en liste en sortie.

**Compatibilité DAG**
Chaque étape (`ingest`, `transform`, `build`) est une fonction autonome avec des entrées/sorties claires. L'intégration dans un orchestrateur Airflow est directe — chaque fonction devient une `PythonOperator`.

## Pour aller plus loin — Grandes volumétries

Pour traiter des fichiers de plusieurs To ou des millions de fichiers :

- **Apache Spark** : remplacer les boucles Python par des transformations distribuées (`DataFrame.filter`, `DataFrame.join`)
- **Traitement par chunks** : lire les fichiers CSV par blocs avec `pandas.read_csv(chunksize=...)`
- **Stockage distribué** : remplacer les fichiers locaux par S3 / GCS / HDFS
- **Parallélisation** : utiliser les `PythonOperator` en parallèle dans Airflow ou passer à un moteur comme Spark/Dask
- **Format de fichier** : privilégier Parquet (compressé, columnar) plutôt que CSV/JSON pour les grands volumes
