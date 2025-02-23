from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

def graphIRIs(limit):
    try:
     _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
     pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
        
    sparql = SPARQLWrapper("https://data.europa.eu/sparql")
    
    sparql.addParameter("distinct", "true")
    sparql.setQuery(f"""
    PREFIX dcat: <http://www.w3.org/ns/dcat#>

    SELECT DISTINCT ?graph
    WHERE {{
      GRAPH ?graph {{
        ?dataset a dcat:Dataset .
      }}
    }}
    LIMIT {limit}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    results_data = results.get('results', {}).get('bindings', [])
    
    return {"message": "data saved successfully", "data": results_data}
