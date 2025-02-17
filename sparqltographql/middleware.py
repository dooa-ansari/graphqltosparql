import json
from django.http import JsonResponse

class RemoveGraphQLDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path == "/graphql/" and response.get("Content-Type") == "application/json":
            try:
                data = json.loads(response.content.decode("utf-8"))
                if "data" in data:
                    return JsonResponse(data["data"])  
            except json.JSONDecodeError:
                pass 

        return response
    
    
class CleanNullAndEmptyObjectsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        if request.path == "/graphql/" and response.get("Content-Type") == "application/json":
            try:
                data = json.loads(response.content.decode("utf-8"))

                if "data" in data:
                    cleaned_data = self.clean_null_and_empty_objects(data["data"])
                    response.content = json.dumps({"data": cleaned_data})
                return response
            except json.JSONDecodeError:
                pass  

        return response

    def clean_null_and_empty_objects(self, obj):
        if isinstance(obj, dict):
            cleaned_dict = {}
            for k, v in obj.items():
                cleaned_value = self.clean_null_and_empty_objects(v)
                if cleaned_value not in [None, {}, []]:
                    cleaned_dict[k] = cleaned_value
            return cleaned_dict
        elif isinstance(obj, list):
            cleaned_list = [self.clean_null_and_empty_objects(i) for i in obj if i not in [None, {}, []]]
            return cleaned_list
        return obj

class ReplaceXmlLangMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == "/graphql/" and response.get("Content-Type") == "application/json":
            try:
                data = json.loads(response.content)

                if 'data' in data:
                    data['data'] = self.replace_xml_lang(data['data'])

                response.content = json.dumps(data)
                
            except Exception as e:
                print(f"Error processing response: {e}")

        return response

    def replace_xml_lang(self, data):
        if isinstance(data, dict):
            return {
                (k.replace("xmlLang", "xml:lang") if "xmlLang" in k else k): self.replace_xml_lang(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self.replace_xml_lang(item) for item in data]
        else:
            return data