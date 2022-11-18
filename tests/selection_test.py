import json

import factory
import pytest

from ads.serializers import AdListSerializer


@pytest.mark.django_db
def test_selection_create(api_client, ad, user):

    data = {"name": "selection test",
            "owner": user.id,
            "items": [ad.pk]}

    expected_response = {'name': "selection test",
                         'owner': user.id,
                         'items': [ad.pk]}
    response = api_client.post('/selection/create/', data=json.dumps(data), content_type='application/json')
    response_data = response.data
    assert response.status_code == 201
    assert response_data['name'] == expected_response['name']
    assert response_data['owner'] == expected_response['owner']
    assert response_data['items'] == expected_response['items']