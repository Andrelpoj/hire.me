import pytest
from src.models import Link, shorten_url

def test_shorten_url_collision(client, db, mocker):
    mocker.patch(
        'src.models.Link.find_by_alias', 
        wraps= lambda x : x in db)
    
    long_url = "https://www.google.com/search?q=capivaras&oq=capivaras&aqs=chrome..69i57j35i39j69i59j46j0l4.1204j0j15&sourceid=chrome&ie=UTF-8"
    
    alias1 = shorten_url(long_url)
    db.append(alias1)
    
    alias2 = shorten_url(long_url)
    db.append(alias2)

    assert alias1 != alias2

