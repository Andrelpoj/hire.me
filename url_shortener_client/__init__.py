import requests
from exceptions import AliasNotFound, AliasAlreadyExists, AliasNotFound

class URLShortenerClient():
    service_url = 'http://localhost:5000'

    def retrieve_url(alias):
        """ 
            Receives an alias and returns the associated long_url.

            Possible Exceptions:
                - AliasNotFound: alias was not found in the database.
                - UnexpectedServerResponse: response from url-shortener service has an unexpected status
        """

        response = requests.get(URLShortenerClient.service_url + f'/{alias}')
        
        if response.status_code == 404:
            raise AliasNotFound(alias)
        elif response.status_code == 200:
            return response.url
        else:
            raise UnexpectedServerResponse(response) 
    
    def shorten_url(url, alias=None):
        """ 
            Receives an url and optionally an alias, registers the link between url and alias and returns the alias.
            An alias is automatically generated if no alias was passed to the function.

            
            Possible Exceptions:
                - AliasAlreadyExists: alias is already in use.
                - UnexpectedServerResponse: response from url-shortener service has an unexpected status
        """

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
        """ 
            Returns the top 10 most accessed short_urls.

            Possible Exceptions:
                - UnexpectedServerResponse: response from url-shortener service has an unexpected status
        """

        response = requests.get(URLShortenerClient.service_url + '/top')
        
        if response.status_code == 200:            
            top_links = response.json()

            ordered_list = []
            for alias in top_links.keys():
                ordered_list.append( (f"{URLShortenerClient.service_url}/{alias}", top_links[alias]) )
            
            return ordered_list
        else:
            raise UnexpectedServerResponse(response)

