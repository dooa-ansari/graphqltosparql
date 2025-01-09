from rdflib import Graph
from .sparql_query import *

def readRDFFile(file):
 print(file)   
 graph = Graph()
 
 graph.parse(data = file, format="xml")
 
#  all_data = graph.query(tierpark_query)
 return ""
 
