
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.urls import include, path
from graphql_main.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/',csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)) ),
    path("machine_data/", include("sparql_main.urls")),
]
