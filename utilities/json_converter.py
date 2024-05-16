import json

class Json:
    
    def ConvertJsontoObject(self, jsonAsString:str):
        data = json.loads(jsonAsString)
        return data