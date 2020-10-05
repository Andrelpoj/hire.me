import pytest 
from types import SimpleNamespace

def test_retrieve_url(client, mocker):
    mocker.patch(
        "src.models.Link.find_by_alias",
        return_value= SimpleNamespace(**
            {
                'long_url': 'https://www.google.com', 
                'increment_visits': (lambda: True)
            })
    )
    
    response = client.get('/tes')
    assert response.status == '302 FOUND'
    assert 'https://www.google.com'.encode() in response.data

def test_shorten_url_without_alias(client, mocker):
    mocker.patch('src.routes.shorten_url', return_value='mockedup')
    mocker.patch(
        'src.routes.Link', 
        wraps= (lambda long_url, alias : SimpleNamespace(**
                {
                    'long_url': long_url, 
                    'alias': alias,
                    'save_to_database': (lambda: True)
                }
            )
        )
    )

    url = 'https://www.bemobi.com'
    
    response = client.post(f'/addlink?url={url}')

    assert response.status == '201 CREATED'
    assert 'https://www.bemobi.com' in response.data.decode()    

#TODO test_shorten_url_with_alias (with and without conflict)
#TODO test_top_urls
