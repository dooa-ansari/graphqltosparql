import graphene
from graphene_django.types import DjangoObjectType
from sparql_main.models import Head, Binding, Results, Data
from collections import defaultdict

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

class GroupedMaintainerEmailType(graphene.ObjectType):
    maintainerEmail = graphene.String()
    bindings = graphene.List(BindingType)
    
class GroupedBindingsType(graphene.ObjectType):
    xmlLang = graphene.String()
    bindings = graphene.List(BindingType)

class ResultsType(graphene.ObjectType):
    distinct = graphene.Boolean()
    ordered = graphene.Boolean()
    bindings = graphene.List(BindingType, xml_lang=graphene.String(), type=graphene.String(), order_by=graphene.String()) 
    grouped_bindings = graphene.List(GroupedBindingsType)
    grouped_maintainer_email = graphene.List(GroupedMaintainerEmailType)
   
    def resolve_bindings(self, info, xml_lang=None, type=None, order_by=None):
        if not hasattr(self, "bindings"):
            return []

        filtered_bindings = []
        for binding in self.bindings.all():
            match_xml_lang = True
            match_type = True

            if xml_lang:
                match_xml_lang = False
                if (
                    (binding.distribution and binding.distribution.xmlLang and binding.distribution.xmlLang.lower() == xml_lang.lower()) or
                    (binding.title and binding.title.xmlLang and binding.title.xmlLang.lower() == xml_lang.lower()) or
                    (binding.mediaType and binding.mediaType.xmlLang and binding.mediaType.xmlLang.lower() == xml_lang.lower()) or
                    (binding.modified and binding.modified.xmlLang and binding.modified.xmlLang.lower() == xml_lang.lower()) or
                    (binding.identifier and binding.identifier.xmlLang and binding.identifier.xmlLang.lower() == xml_lang.lower()) or
                    (binding.accessURL and binding.accessURL.xmlLang and binding.accessURL.xmlLang.lower() == xml_lang.lower()) or
                    (binding.description and binding.description.xmlLang and binding.description.xmlLang.lower() == xml_lang.lower()) or
                    (binding.geometry and binding.geometry.xmlLang and binding.geometry.xmlLang.lower() == xml_lang.lower()) or
                    (binding.license and binding.license.xmlLang and binding.license.xmlLang.lower() == xml_lang.lower()) or
                    (binding.publisherName and binding.publisherName.xmlLang and binding.publisherName.xmlLang.lower() == xml_lang.lower()) or
                    (binding.maintainerEmail and binding.maintainerEmail.xmlLang and binding.maintainerEmail.xmlLang.lower() == xml_lang.lower())
                ):
                    match_xml_lang = True

            if type:
                match_type = False
                if (
                    (binding.distribution and binding.distribution.type and binding.distribution.type.lower() == type.lower()) or
                    (binding.title and binding.title.type and binding.title.type.lower() == type.lower()) or
                    (binding.mediaType and binding.mediaType.type and binding.mediaType.type.lower() == type.lower()) or
                    (binding.modified and binding.modified.type and binding.modified.type.lower() == type.lower()) or
                    (binding.identifier and binding.identifier.type and binding.identifier.type.lower() == type.lower()) or
                    (binding.accessURL and binding.accessURL.type and binding.accessURL.type.lower() == type.lower()) or
                    (binding.description and binding.description.type and binding.description.type.lower() == type.lower()) or
                    (binding.geometry and binding.geometry.type and binding.geometry.type.lower() == type.lower()) or
                    (binding.license and binding.license.type and binding.license.type.lower() == type.lower()) or
                    (binding.publisherName and binding.publisherName.type and binding.publisherName.type.lower() == type.lower()) or
                    (binding.maintainerEmail and binding.maintainerEmail.type and binding.maintainerEmail.type.lower() == type.lower())
                ):
                    match_type = True

            if match_xml_lang and match_type:
                filtered_bindings.append(binding)

        if order_by:
            if order_by == "title__value":
                filtered_bindings.sort(key=lambda b: b.title.value if b.title and b.title.value else "")
            elif order_by == "description__value":
                filtered_bindings.sort(key=lambda b: b.description.value if b.description and b.description.value else "")
            elif order_by == "title__xmlLang":
                filtered_bindings.sort(key=lambda b: b.title.xmlLang if b.title and b.title.xmlLang else "")
            elif order_by == "description__xmlLang":
                filtered_bindings.sort(key=lambda b: b.description.xmlLang if b.description and b.description.xmlLang else "")

        return filtered_bindings
    
    def resolve_grouped_bindings(self, info):
        if not hasattr(self, "bindings"):
            return []

        grouped_data = defaultdict(list)
        for binding in self.bindings.all():
            if binding.title and binding.title.xmlLang:
                grouped_data[binding.title.xmlLang].append(binding)

        result = [
            GroupedBindingsType(xmlLang=xmlLang, bindings=bindings)
            for xmlLang, bindings in grouped_data.items()
        ]
        return result
    
    def resolve_grouped_maintainer_email(self, info):
        if not hasattr(self, "bindings"):
            return []

        grouped_data = defaultdict(list)
        for binding in self.bindings.all():
            if binding.maintainerEmail and binding.maintainerEmail.value:
                grouped_data[binding.maintainerEmail.value].append(binding)

        result = [
            GroupedMaintainerEmailType(maintainerEmail=maintainerEmail, bindings=bindings)
            for maintainerEmail, bindings in grouped_data.items()
        ]
        return result

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