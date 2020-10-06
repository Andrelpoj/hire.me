import requests

class URLShortenerClient():
    service_url = 'http://localhost:5000'

    def retrieve_url(alias):
        response = requests.get(URLShortenerClient.service_url + f'/{alias}')
        
        if response.status_code == 404:
            raise AliasNotFound(alias)
            
        return response
    
    def shorten_url(url, alias=None):
        req_url = URLShortenerClient.service_url + f'/addlink?url={url}'
        if alias:
            req_url += f'&custom_alias={alias}'
        
        response = requests.post(req_url)

        if response.status_code == 400:
            raise AliasAlreadyExists(alias)

        return response
    
    def get_top_links():        
        response = requests.get(URLShortenerClient.service_url + '/top')
        return response

class AliasNotFound(Exception):
    def __init__(self, alias):
        self.alias = alias 

class AliasAlreadyExists(Exception):
    def __init__(self, alias):
        self.alias = alias 