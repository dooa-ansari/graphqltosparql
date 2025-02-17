from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import json

# introduce filters and dropdowns for different types of queries like filter etc

from .date_parser import parse_date
from .models import Binding, Data, Head, Results, PropertyType



def parse_geometry(value):
    if not value:
        return None

    try:
        parsed_value = json.loads(value) 
        if isinstance(parsed_value, dict) and "type" in parsed_value and "coordinates" in parsed_value:
            return parsed_value 
    except json.JSONDecodeError:
        pass 

    return value

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
LIMIT 200
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
    
    Data.objects.all().delete()      
    Results.objects.all().delete()  
    Binding.objects.all().delete()   
    PropertyType.objects.all().delete() 
    
    for binding in results_data.get('bindings', []):
        print(binding)
        binding_obj = Binding.objects.create(
            distribution=PropertyType.objects.create(
              type = binding.get('distribution', {}).get('type'),
              value = binding.get('distribution', {}).get('value'),
              datatype = binding.get('distribution', {}).get('datatype'),
              xmlLang = binding.get('distribution', {}).get('xml:lang'),
            ),
            title=PropertyType.objects.create(
              type = binding.get('title', {}).get('type'),
              value = binding.get('title', {}).get('value'),
              xmlLang = binding.get('title', {}).get('xml:lang'),
            ),
            mediaType=PropertyType.objects.create(
              type = binding.get('mediaType', {}).get('type'),
              value = binding.get('mediaType', {}).get('value'),
              xmlLang = binding.get('mediaType', {}).get('xml:lang'),
            ),
            modified=PropertyType.objects.create(
              type = binding.get('modified', {}).get('type'),
              value = binding.get('modified', {}).get('value'),
              datatype = binding.get('modified', {}).get('datatype'),
              xmlLang = binding.get('modified', {}).get('xml:lang'),
            ),
            identifier=PropertyType.objects.create(
              type = binding.get('identifier', {}).get('type'),
              value = binding.get('identifier', {}).get('value'),
              datatype = binding.get('identifier', {}).get('datatype'),
              xmlLang = binding.get('identifier', {}).get('xml:lang'),
            ),
            accessURL=PropertyType.objects.create(
              type = binding.get('accessUrl', {}).get('type'),
              value = binding.get('accessUrl', {}).get('value'),
              datatype = binding.get('accessUrl', {}).get('datatype'),
              xmlLang = binding.get('accessUrl', {}).get('xml:lang'),
            ),
            description=PropertyType.objects.create(
              type = binding.get('description', {}).get('type'),
              value = binding.get('description', {}).get('value'),
              datatype = binding.get('description', {}).get('datatype'),
              xmlLang = binding.get('description', {}).get('xml:lang'),
            ),
            geometry= PropertyType.objects.create(
              type = binding.get('geometry', {}).get('type'),
              value = parse_geometry(binding.get('geometry', {}).get('value', "{}")), 
              datatype = binding.get('geometry', {}).get('datatype'),
              xmlLang = binding.get('geometry', {}).get('xml:lang'),
            ),
            license=PropertyType.objects.create(
              type = binding.get('license', {}).get('type'),
              value = binding.get('license', {}).get('value'),
              datatype = binding.get('license', {}).get('datatype'),
              xmlLang = binding.get('license', {}).get('xml:lang'),
            ),
            publisherName=PropertyType.objects.create(
              type = binding.get('publisherName', {}).get('type'),
              value = binding.get('publisherName', {}).get('value'),
              datatype = binding.get('publisherName', {}).get('datatype'),
              xmlLang = binding.get('publisherName', {}).get('xml:lang'),
            ),
            maintainerEmail=PropertyType.objects.create(
              type = binding.get('maintainerEmail', {}).get('type'),
              value = binding.get('maintainerEmail', {}).get('value'),
              datatype = binding.get('maintainerEmail', {}).get('datatype'),
              xmlLang = binding.get('maintainerEmail', {}).get('xml:lang'),
            )
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
