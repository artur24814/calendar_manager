import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_logout_user(client, user, user2, in_memory, user3):
    client.logout()
    response = client.get(reverse('calendar:friends'))

    assert response.status_code == 302
    assert response['Location'] == '/login/?next=/calendar/friends/'
    

@pytest.mark.django_db
def test_blank_list(client, user, user2, user3, in_memory, login_user):
    response = client.get(reverse('calendar:friends'))

    assert len(response.context['object_list']) == 0
    assert response.context['is_paginated'] == False
    assert response.status_code == 200
    assertTemplateUsed(response, 'calendar_manager/list_friends.html')

@pytest.mark.django_db
def test_all_friends(client, user_with_folows, user2, user3, in_memory, login_user):
    response = client.get(reverse('calendar:friends'))

    assert len(response.context['object_list']) == 2
    assert response.context['is_paginated'] == False
    assert response.status_code == 200
    assertTemplateUsed(response, 'calendar_manager/list_friends.html')

@pytest.mark.django_db
def test_filtered_friends(client, user_with_folows, user2, user3, in_memory, login_user):
    response = client.get(reverse('calendar:friends') +'?search=Mal')

    assert len(response.context['object_list']) == 1
    assert response.context['is_paginated'] == False
    assert response.status_code == 200
    assertTemplateUsed(response, 'calendar_manager/list_friends.html')