# создание объявления — POST /ads;
import json

import pytest

from ads.serializers import AdListSerializer
from factories import AdFactory


@pytest.mark.django_db
def test_ad_create(api_client, ad):
    data = {
        "name": "test_ad_name",
        "author": ad.author.id,
        "price": 100,
        "is_published": False,
        "category": ad.category.id,
    }

    expected_response = AdListSerializer(ad).data
    response = api_client.post("/ads/", data=json.dumps(data), content_type='application/json')
    response_data = response.json()
    assert response_data['author_name'] == expected_response['author_name']
    assert response_data['category_name'] == expected_response['category_name']
    assert response_data['created'] == expected_response['created']
    assert response_data['description'] == expected_response['description']
    assert response_data['image'] == expected_response['image']
    assert response_data['is_published'] == expected_response['is_published']
    assert response_data['name'] == expected_response['name']
    assert response_data['price'] == expected_response['price']
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

    response = api_client.get(f'/ad/{ad.pk}/')
    assert response.status_code == 200
    assert response.data == expected_response
