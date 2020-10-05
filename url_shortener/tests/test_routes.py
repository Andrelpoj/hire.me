import pytest 
from types import SimpleNamespace

from src.models import AliasAlreadyExists


def test_retrieve_url(client, mocker):
    url = 'https://www.google.com'
    mocker.patch(
        "src.models.Link.find_by_alias",
        return_value= SimpleNamespace(**
            {
                'long_url': url, 
                'increment_visits': (lambda: True)
            })
    )
    
    response = client.get('/tes')
    assert response.status == '302 FOUND'
    assert url.encode() in response.data

def test_retrieve_url_not_found(client, mocker):
    alias = 'tes'
    mocker.patch(
        "src.models.Link.find_by_alias",
        return_value= {}
    )
    
    response = client.get('/'+alias)

    assert response.status == '404 NOT FOUND'
    assert alias.encode() in response.data


def test_shorten_url_without_alias(client, mocker):
    url = 'https://www.bemobi.com'
    mocker.patch('src.routes.shorten_url', return_value='mockedup')
    mocker.patch('src.routes.Link', wraps= mocked_link_creator)
    
    response = client.post(f'/addlink?url={url}')

    assert response.status == '201 CREATED'
    assert url in response.data.decode()    

def test_shorten_url_with_alias(client, mocker): 
    url = 'https://www.bemobi.com'
    custom_alias = 'mockedup'
    mocker.patch('src.routes.Link', wraps= mocked_link_creator)
    
    response = client.post(f'/addlink?url={url}&custom_alias={custom_alias}')

    assert response.status == '201 CREATED'
    assert url in response.data.decode()
    assert custom_alias in response.data.decode()
    
def test_shorten_url_with_conflicted_alias(client, mocker):
    url = 'https://www.bemobi.com'
    custom_alias = 'bemobi'
    mocker.patch('src.routes.Link', side_effect= AliasAlreadyExists(custom_alias))

    response = client.post(f'/addlink?url={url}&custom_alias={custom_alias}')

    assert response.status == '400 BAD REQUEST'
    assert custom_alias in response.data.decode()


def test_top_urls(client, mocker):
    mocker.patch(
        "src.routes.Link.top_most_visited",
        wraps= mocked_link_visit_registry
    )
    
    response = client.get('/top')

    assert response.status == '200 OK'


def mocked_link_creator(long_url, alias):
    return SimpleNamespace(**{
        'long_url': long_url, 
        'alias': alias,
        'save_to_database': (lambda: True)
    })

def mocked_link_visit_registry():
    return [
        mocked_link_visit('t1', 10),
        mocked_link_visit('t2', 20),
        mocked_link_visit('t3', 30),
        mocked_link_visit('t4', 40),
        mocked_link_visit('t5', 50),
        mocked_link_visit('t6', 60),
        mocked_link_visit('t7', 70),
        mocked_link_visit('t8', 80),
        mocked_link_visit('t9', 90),
        mocked_link_visit('t10', 100)
    ]

def mocked_link_visit(alias, visits):
    return SimpleNamespace(**{'alias': alias, 'visits': visits})
