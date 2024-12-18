
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path("machine_data/", include("sparql_main.urls")),
]
