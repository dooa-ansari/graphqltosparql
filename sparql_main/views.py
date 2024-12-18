from pymantic import sparql
from .rdf_fetcher import open_sparql_url
import requests
from django.http import JsonResponse

def get_rdf_data(data):
    response = open_sparql_url()
    print(response)
    response_data = {
                        'message': "File saved successfully",
                    }
    return response_data