from sparql_endpoint import SparqlEndpoint

wikidata_query_endpoint = SparqlEndpoint("https://query.wikidata.org/sparql")


def label_entity(entity):
    entity_id = entity.split('/Q')[-1]
    query = f"""
    SELECT ?label WHERE {{
        wd:Q{entity_id} rdfs:label ?label.
        FILTER(LANGMATCHES(LANG(?label), "EN")).
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}"""
    return next(wikidata_query_endpoint.query(query))['label']
