# создание объявления — POST /ads;
import json

import pytest

from ads.serializers import AdListSerializer
from factories import AdFactory


@pytest.mark.django_db
def test_ad_create(client, user, category):
    data = {
        "name": "Алиса в стране чудес",
        "author":user.pk,
        "price": 100,
        "category": category.pk

    }
    response = client.post("/ads/create/", data=json.dumps(data), content_type='application/json')
    expected_response = response.data
    response_data = response.json()

    assert response_data['author'] == user.pk
    assert response_data['category'] == category.pk
    # assert response_data['created'] == expected_response['created']
    assert response_data['description'] == None
    assert response_data['image'] == None
    assert response_data['is_published'] == False
    assert response_data['name'] == "Алиса в стране чудес"
    assert response_data['price'] == 100
    assert response.status_code == 201


@pytest.mark.django_db
def test_ad_list(api_client):
    ads = AdFactory.create_batch(2)
    results = AdListSerializer(ads, many=True).data

    expected_response = {
        'count': 2,
        'next': None,
        'previous': None,
        'results': list(map(lambda i: dict(i), results))
    }

    response = api_client.get('/ads/')
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.django_db
def test_ad_detail(api_client, ad):
    expected_response = AdListSerializer(ad).data

    response = api_client.get(f'/ads/{ad.pk}/')
    assert response.status_code == 200
    assert response.data == expected_response
