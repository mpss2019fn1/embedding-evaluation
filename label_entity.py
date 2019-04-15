import requests

wikidata_query_endpoint = "https://query.wikidata.org/sparql"


def label_entity(entity):
    entity_id = entity.split('/Q')[-1]
    query = f"""
    SELECT ?label WHERE {{
        wd:Q{entity_id} rdfs:label ?label.
        FILTER(LANGMATCHES(LANG(?label), "EN")).
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}"""
    r = requests.get(wikidata_query_endpoint, params={"format": "json", "query": query})
    return r.json()["results"]["bindings"][0]["label"]["value"]
