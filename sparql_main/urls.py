from django.urls import path
from .views import get_rdf_data, get_search_chemnitz_list, get_available_graph_iris

urlpatterns = [
    path('machine_data',get_rdf_data, name='machine_data'),
    path('chemnitz_datasets', get_search_chemnitz_list, name='chemnitz_datasets'),
    path('available_graph_iris', get_available_graph_iris, name='available_graph_iris'),
]
# http://127.0.0.1:8000/machine_data/chemnitz_datasets