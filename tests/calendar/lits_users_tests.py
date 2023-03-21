import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_list_all_users(client, user, user2, in_memory):
    response = client.get(reverse('calendar:users'))

    assert len(response.context['object_list']) == 2
    assert response.context['is_paginated'] == False
    assert response.status_code == 200
    assertTemplateUsed(response, 'calendar_manager/list_users.html')

@pytest.mark.django_db
def test_list_filtered_users(client, user, user2, in_memory):
    response = client.get(reverse('calendar:users') +'?search=May')

    assert len(response.context['object_list']) == 1
    assert response.context['is_paginated'] == False
    assert response.status_code == 200
    assertTemplateUsed(response, 'calendar_manager/list_users.html')