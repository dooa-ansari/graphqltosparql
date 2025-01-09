tierpark_query = """PREFIX dcat: <http://www.w3.org/ns/dcat#>
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
LIMIT 500"""