import urllib.request
import ssl
from rdflib import Namespace
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD
from urllib.parse import urlencode
import urllib3

graph = Graph()

def open_sparql_url(sparql_query):
    europa_sparql_endpoint = "https://data.europa.eu/sparql"
    default_graph_uri = 'http://data.europa.eu/88u/dataset/https-portal-chemnitz-opendata-arcgis-com-datasets-chemnitz-tierparks'
    query =  sparql_query
    format = "application/rdf+xml"
    timeout = 120000
    signal_void="on"
    params = {
    "default-graph-uri": default_graph_uri,
    "query": query,
    "format":format,
    "timeout": timeout,
    "signal_void": signal_void,
    }
    encoded_params = urlencode(params)

    try:
     _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
     pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    output_file = "response_data.rdf"    
    urllib.request.urlretrieve(f"{europa_sparql_endpoint}?{encoded_params}", output_file)
    
    # with open(output_file, "r", encoding="utf-8") as file:
    #  content = file.read()
    # print(content)
    return output_file    