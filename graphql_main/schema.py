import graphene
from graphene_django.types import DjangoObjectType
import requests
from django.urls import reverse
from django.http import HttpRequest        

class Binding(graphene.ObjectType):
    distribution = graphene.String()
    title = graphene.String()
    mediaType = graphene.String()
    modified = graphene.String()
    identifier = graphene.String()
    accessURL = graphene.String()
    description = graphene.String()
    geometry = graphene.String()
    license = graphene.String()
    publisherName = graphene.String()
    maintainerEmail = graphene.String()

class Results(graphene.ObjectType):
    distinct = graphene.Boolean()
    ordered = graphene.Boolean()
    bindings = graphene.List(Binding)

class Head(graphene.ObjectType):
    link = graphene.List(graphene.String)
    vars = graphene.List(graphene.String)

class Root(graphene.ObjectType):
    head = graphene.Field(Head)
    results = graphene.Field(Results)

class Query(graphene.ObjectType):
    data = graphene.Field(Root)

    def resolve_data(self, info):
        request: HttpRequest = info.context["request"]
        machine_data_url = request.build_absolute_uri(reverse("machine_data"))
        response = requests.get(machine_data_url)
        json_data = response.json()
        return json_data

schema = graphene.Schema(query=Query)
