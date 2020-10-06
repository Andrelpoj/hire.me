import requests

class URLShortenerClient():
    service_url = 'http://localhost:5000'

    def retrieve_url(alias):
        response = requests.get(URLShortenerClient.service_url + f'/{alias}')
        
        if response.status_code == 404:
            raise AliasNotFound(alias)
        elif response.status_code == 200:
            return response.url
        else:
            raise UnexpectedServerResponse(response) 
    
    def shorten_url(url, alias=None):
        req_url = URLShortenerClient.service_url + f'/addlink?url={url}'
        if alias:
            req_url += f'&custom_alias={alias}'
        
        response = requests.post(req_url)

        if response.status_code == 400:
            raise AliasAlreadyExists(alias)
        elif response.status_code == 201:
            return response.json()['alias']
        else:
            raise UnexpectedServerResponse(response)

    
    def get_top_links():        
        response = requests.get(URLShortenerClient.service_url + '/top')
        
        if response.status_code == 200:            
            top_links = response.json()

            ordered_list = []
            for alias in top_links.keys():
                ordered_list.append( (alias, top_links[alias]) )
            
            return ordered_list
        else:
            raise UnexpectedServerResponse(response)

class AliasNotFound(Exception):
    def __init__(self, alias):
        self.alias = alias 

class AliasAlreadyExists(Exception):
    def __init__(self, alias):
        self.alias = alias 

class UnexpectedServerResponse(Exception):
    def __init__(self, response):
        self.response = response
