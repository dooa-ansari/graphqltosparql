from pymantic import sparql
from .wrapper import *
from .euro_data_fetcher import open_sparql_url
from .sparql_query import *
from .rdf_file_reader import *
import requests
from django.http import JsonResponse

def get_rdf_data(data):
    response = sparqlWrapperTest()
    # response = open_sparql_url(tierpark_query)
    # graph_data = readRDFFile(response)
    # for row in graph_data:
    #     print(row)
    response_data = {
                        'message': "File saved successfully",
                        'data': response
                    }
    return JsonResponse(response_data)