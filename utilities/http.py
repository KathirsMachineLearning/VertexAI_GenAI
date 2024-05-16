import requests
import base64
from requests.api import request
from requests.exceptions import HTTPError

class Http:  
    
  def HttpGet(self, url:str, authentication:str):
    print(f'Processing Http Get for {url}')
    response = None
    try:
        token = f'{authentication}:'
        message_bytes = token.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        payload={}
        headers = {
                      'Authorization': f'Basic {base64_message}'
                  }
        
        response = requests.request("GET", url, headers=headers, data=payload, verify = False)
        response.raise_for_status()
        print(f'Processing Http Get for {url} is successfull')

    except HTTPError as http_err:
        print(f'HTTP Error Occured for Http Post for {url} and error details: {http_err}')  

    except Exception as err:
        print(f'General Error Occured for Http Post for {url} and error details: {err}') 
        
    return response
  
  def HttpPost(self, url:str, authentication:str):
    print(f'Processing Http Post for {url}')
    response = None
    try:
        token = f'{authentication}:'
        message_bytes = token.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        payload={}
        headers = {
                      'Content-Type': 'application/json',
  		              'Accept': 'application/json',
                      'Authorization': f'Basic {base64_message}'
                  }
        
        response = requests.request("POST", url, headers=headers, data=payload, verify = False)
        response.raise_for_status()
        print(f'Processing Http Post for {url} is successfull')

    except HTTPError as http_err:
        print(f'Http Error Occured for Http Post for {url} and error details: {http_err}')  

    except Exception as err:
        print(f'General Error Occured for Http Post for {url} and error details: {err}') 
        
    return response