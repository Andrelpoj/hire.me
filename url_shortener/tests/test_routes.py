import pytest 
from types import SimpleNamespace

def test_retrieve_url(client, mocker):
    mocker.patch(
        "src.models.Link.find_by_alias",
        return_value= SimpleNamespace(**{'long_url': 'https://www.google.com', 'increment_visits': (lambda: True)})
    )
    
    response = client.get('/tes')
    assert response.status == '302 FOUND'
    assert 'https://www.google.com'.encode() in response.data

#TODO test_top_urls
#TODO test_shorten_url