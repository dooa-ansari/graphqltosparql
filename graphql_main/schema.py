import graphene
from graphene_django.types import DjangoObjectType
from sparql_main.models import Head, Binding, Results, Data

class PropertyTypeG(graphene.ObjectType):
    type = graphene.String()
    datatype = graphene.String()
    value = graphene.String()
    xmlLang = graphene.String()


class HeadType(DjangoObjectType):
    class Meta:
        model = Head
        fields = ("vars", "link")


class BindingType(graphene.ObjectType):
    distribution = graphene.Field(PropertyTypeG)
    title = graphene.Field(PropertyTypeG)
    mediaType = graphene.Field(PropertyTypeG)
    modified = graphene.Field(PropertyTypeG)
    identifier = graphene.Field(PropertyTypeG)
    accessURL = graphene.Field(PropertyTypeG)
    description = graphene.Field(PropertyTypeG)
    geometry = graphene.Field(PropertyTypeG)
    license = graphene.Field(PropertyTypeG)
    publisherName = graphene.Field(PropertyTypeG)
    maintainerEmail = graphene.Field(PropertyTypeG)


class ResultsType(graphene.ObjectType):
    distinct = graphene.Boolean()
    ordered = graphene.Boolean()
    bindings = graphene.List(BindingType)

    def resolve_bindings(self, info):
        return self.bindings.all() if hasattr(self, "bindings") else []


# class DataType(DjangoObjectType):
#     class Meta:
#         model = Data
#         fields = ("head", "results")


class Query(graphene.ObjectType):
    head = graphene.Field(HeadType)
    results = graphene.Field(ResultsType)

    def resolve_head(self, info):
        data_instance = Data.objects.first()
        return data_instance.head if data_instance else None

    def resolve_results(self, info):
        data_instance = Data.objects.first()
        return data_instance.results if data_instance else None


schema = graphene.Schema(query=Query)
