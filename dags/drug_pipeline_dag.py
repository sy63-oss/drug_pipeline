from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from pipeline.ingestion import load_drugs, load_pubmed_csv, load_pubmed_json, load_clinical_trials
from pipeline.transformer import find_mentions
from pipeline.builder import build_graph
import json
from pathlib import Path

def ingest(**context):
    drugs           = load_drugs("data/drugs.csv")
    pubmed_csv      = load_pubmed_csv("data/pubmed.csv")
    pubmed_json     = load_pubmed_json("data/pubmed.json")
    clinical_trials = load_clinical_trials("data/clinical_trials.csv")
    context["ti"].xcom_push(key="drugs", value=drugs)
    context["ti"].xcom_push(key="publications", value=pubmed_csv + pubmed_json)
    context["ti"].xcom_push(key="clinical_trials", value=clinical_trials)

def transform(**context):
    ti = context["ti"]
    drugs           = ti.xcom_pull(key="drugs")
    publications    = ti.xcom_pull(key="publications")
    clinical_trials = ti.xcom_pull(key="clinical_trials")
    mentions = (
        find_mentions(publications, drugs, "pubmed") +
        find_mentions(clinical_trials, drugs, "clinical_trials")
    )
    ti.xcom_push(key="mentions", value=mentions)

def build(**context):
    mentions = context["ti"].xcom_pull(key="mentions")
    graph = build_graph(mentions)
    output_path = Path("output/graph.json")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)

with DAG(
    dag_id="drug_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="ingest",    python_callable=ingest)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="build",     python_callable=build)

    t1 >> t2 >> t3
