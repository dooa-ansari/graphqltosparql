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
        # Get the response from the view
        response = self.get_response(request)

        # Check if the request is for GraphQL and content type is JSON
        if request.path == "/graphql/" and response.get("Content-Type") == "application/json":
            try:
                # Parse the response body to manipulate the data
                data = json.loads(response.content)

                # Apply the function to replace 'xmlLang' with 'xml:lang'
                if 'data' in data:
                    data['data'] = self.replace_xml_lang(data['data'])

                # Convert the manipulated data back to JSON
                response.content = json.dumps(data)
                
            except Exception as e:
                print(f"Error processing response: {e}")

        return response

    def replace_xml_lang(self, data):
        """
        Recursively replace 'xmlLang' with 'xml:lang' in the data.
        """
        if isinstance(data, dict):
            # If the data is a dictionary, recursively check each key
            return {
                (k.replace("xmlLang", "xml:lang") if "xmlLang" in k else k): self.replace_xml_lang(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            # If the data is a list, recursively process each item
            return [self.replace_xml_lang(item) for item in data]
        else:
            # Return the value as is for other types
            return data