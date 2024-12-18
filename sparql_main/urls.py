from django.urls import path
from .views import get_rdf_data

urlpatterns = [
    path('machine_data/',get_rdf_data, name='machine_data')
]
