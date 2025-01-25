from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import json

from .date_parser import parse_date
from .models import Binding, Data, Head, Results

def sparqlWrapperTest(dataset_name):
    try:
     _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
     pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
        
    sparql = SPARQLWrapper("https://data.europa.eu/sparql")
    dataset = ""
    
    if dataset_name == "Animal Parks":
     dataset = "http://data.europa.eu/88u/dataset/https-portal-chemnitz-opendata-arcgis-com-datasets-chemnitz-tierparks"
    elif dataset_name == "Parking ticket machines":
     dataset = "http://data.europa.eu/88u/dataset/https-portal-chemnitz-opendata-arcgis-com-datasets-chemnitz-parkscheinautomaten"
    elif dataset_name == "Schools":
     dataset = "http://data.europa.eu/88u/dataset/https-portal-chemnitz-opendata-arcgis-com-datasets-chemnitz-schulen"
    else:
     dataset = None 
        
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
    
    head_data = results.get('head', {})
    head = Head.objects.create(
        vars=head_data.get('vars', []),
        link=head_data.get('link', [])
    )
    results_data = results.get('results', {})
    bindings = []
    
    for binding in results_data.get('bindings', []):
        binding_obj = Binding.objects.create(
            distribution=binding.get('distribution', {}).get('value'),
            title=binding.get('title', {}).get('value'),
            mediaType=binding.get('mediaType', {}).get('value'),
            modified=parse_date(binding.get('modified', {}).get('value')),
            identifier=binding.get('identifier', {}).get('value'),
            accessURL=binding.get('accessURL', {}).get('value'),
            description=binding.get('description', {}).get('value'),
            geometry=json.loads(binding.get('geometry', {}).get('value', "{}")), 
            license=binding.get('license', {}).get('value'),
            publisherName=binding.get('publisherName', {}).get('value'),
            maintainerEmail=binding.get('maintainerEmail', {}).get('value'),
        )
        bindings.append(binding_obj)
        
    
    
    results = Results.objects.create(
        distinct=results_data.get('distinct', False),
        ordered=results_data.get('ordered', True),
    )
    results.bindings.set(bindings)
    json_entry = Data.objects.create(
        head=head,
        results=results
    )
    json_entry = Data.objects.first()
    print(json_entry.head.vars)
    print(json_entry.results.bindings.all())
    bindings_queryset = json_entry.results.bindings.all()
    for binding in bindings_queryset:
      print(f"Distribution: {binding.distribution}")
      print(f"Title: {binding.title}")
      print(f"Media Type: {binding.mediaType}")
      print(f"Modified: {binding.modified}")
      print(f"Identifier: {binding.identifier}")
      print(f"Access URL: {binding.accessURL}")
      print(f"Description: {binding.description}")
      print(f"Geometry: {binding.geometry}")
      print(f"License: {binding.license}")
      print(f"Publisher Name: {binding.publisherName}")
      print(f"Maintainer Email: {binding.maintainerEmail}")
      print("-" * 40) 
    return {"message": "data saved successfully"}
