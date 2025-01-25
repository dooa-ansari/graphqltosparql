from pymantic import sparql
from .wrapper import *
from .euro_data_fetcher import open_sparql_url
from .sparql_query import *
from .rdf_file_reader import *
import requests
from django.http import JsonResponse

def get_rdf_data(request):
    dataset_name = request.GET.get("dataset", "")
    response = sparqlWrapperTest(dataset_name)
    # response = open_sparql_url(tierpark_query)
    # graph_data = readRDFFile(response)
    # for row in graph_data:
    #     print(row)
    response_data = {
                        'message': "File saved successfully",
                        'data': response
                    }
    return JsonResponse(response_data)

# https://data.europa.eu/data/datasets?locale=en&page=1&query=chemnitz+&publisher=Stadtverwaltung+Chemnitz
def get_search_chemnitz_list(data):
    api_url_chemnitz_datasets = "https://data.europa.eu/api/hub/search/search?q=chemnitz%20&filter=dataset&includes=id,title.en,description.en,languages,modified,issued,catalog.id,catalog.title,catalog.country.id,distributions.id,distributions.format.label,distributions.format.id,distributions.license,categories.label,publisher&facets=%7B%22is_hvd%22:[],%22hvdCategory%22:[],%22country%22:[],%22publisher%22:[%22Stadtverwaltung%20Chemnitz%22],%22catalog%22:[],%22format%22:[],%22categories%22:[],%22keywords%22:[],%22subject%22:[],%22scoring%22:[],%22license%22:[],%22dataServices%22:[],%22superCatalog%22:[]%7D"
    
    try:
        response = requests.get(api_url_chemnitz_datasets)
        response.raise_for_status() 
        
        data = response.json()
        only_list = data.get("result", {}).get("results", [])
        
        return JsonResponse(only_list, safe=False)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)