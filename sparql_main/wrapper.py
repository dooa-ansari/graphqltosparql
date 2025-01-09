from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

def sparqlWrapperTest():
    try:
     _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
     pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
        
    sparql = SPARQLWrapper("https://data.europa.eu/sparql")
    dataset = "http://data.europa.eu/88u/dataset/https-portal-chemnitz-opendata-arcgis-com-datasets-chemnitz-tierparks"
    sparql.addParameter("default-graph-uri", dataset)
    sparql.addParameter("distinct", "true")
    sparql.setQuery("""
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX locn: <http://www.w3.org/ns/locn#>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX dcatapde: <http://dcat-ap.de/def/dcatde/>

SELECT ?distribution ?title ?mediaType ?modified ?identifier ?accessURL ?description ?geometry ?license ?publisherName ?maintainerEmail
WHERE {
  ?distribution a dcat:Distribution ;
                dct:title ?title ;
                dcat:mediaType ?mediaType ;
                dct:modified ?modified ;
                dct:identifier ?identifier ;
                dcat:accessURL ?accessURL ;
                dct:license ?license .

  OPTIONAL { ?distribution dct:format ?format . }
  
  OPTIONAL {
    ?dataset a dcat:Dataset ;
             dct:description ?description ;
             dct:spatial ?location ;
             dct:publisher ?publisher .
    ?location locn:geometry ?geometry .
    ?publisher foaf:name ?publisherName .
  }

  OPTIONAL {
    ?dataset dcatapde:maintainer ?maintainer .
    ?maintainer foaf:mbox ?maintainerEmail .
  }
}
LIMIT 2
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    return results
