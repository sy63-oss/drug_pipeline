def build_graph(mentions: list[dict]) -> list[dict]:
    graph = {}
    for mention in mentions:
        drug = mention["drug"]
        if drug not in graph:
            graph[drug] = {"drug": drug, "pubmed": [], "clinical_trials": []}
        entry = {"journal": mention["journal"], "date": mention["date"]}
        graph[drug][mention["source"]].append(entry)
    return list(graph.values())
