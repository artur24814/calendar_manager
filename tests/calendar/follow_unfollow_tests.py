import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_logout_user(client, user, user2, in_memory):
    client.logout()
    response = client.get(reverse('calendar:follow', kwargs={'profile_pk': user2.profile.id}))

    assert response.status_code == 302
    assert response['Location'] == f'/login/?next=/calendar/follow/{user2.profile.id}/'

@pytest.mark.django_db
def test_follow_unfollow(client, user, user2, in_memory, login_user):
    response = client.get(reverse('calendar:follow', kwargs={'profile_pk': user2.profile.id}))

    assert response.status_code == 302
    assert response['Location'] == reverse('calendar:calendar', kwargs={'user_pk': user2.id})

    assert list(user.profile.follows.all()).count(user2.profile) == 1

    response2 = client.get(reverse('calendar:follow', kwargs={'profile_pk': user2.profile.id}))

    assert response2.status_code == 302
    assert response2['Location'] == reverse('calendar:calendar', kwargs={'user_pk': user2.id})

    assert list(user.profile.follows.all()).count(user2.profile) == 0