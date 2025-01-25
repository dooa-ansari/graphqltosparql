import graphene
from graphene_django.types import DjangoObjectType
from sparql_main.models import Head, Binding, Results, Data

class HeadType(graphene.ObjectType):
    vars = graphene.List(graphene.String)
    link = graphene.List(graphene.String)

class BindingType(graphene.ObjectType):
    distribution = graphene.String()
    title = graphene.String()
    mediaType = graphene.String()
    modified = graphene.DateTime()
    identifier = graphene.String()
    accessURL = graphene.String()
    description = graphene.String()
    geometry = graphene.JSONString()
    license = graphene.String()
    publisherName = graphene.String()
    maintainerEmail = graphene.String()

class ResultsType(graphene.ObjectType):
    distinct = graphene.Boolean()
    ordered = graphene.Boolean()
    bindings = graphene.List(BindingType)
    def resolve_bindings(self, info):
        if hasattr(self, "bindings"):
            print("bindings")
            print(self.bindings.all())
            return self.bindings.all()
        return []

class DataType(graphene.ObjectType):
    head = graphene.Field(HeadType)
    results = graphene.Field(ResultsType)
    print(head)
    print(results)
    def resolve_head(self, info):
        return self.head

    def resolve_results(self, info):
        return self.results

class Query(graphene.ObjectType):
    head = graphene.Field(HeadType)  
    results = graphene.Field(ResultsType) 

    def resolve_head(self, info):
        data_instance = Data.objects.first()
        if data_instance:
            return data_instance.head  
        return None

    def resolve_results(self, info):
        data_instance = Data.objects.first()
        if data_instance:
            return data_instance.results  
        return None

schema = graphene.Schema(query=Query)
