import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile
from django.contrib.messages import get_messages


@pytest.mark.django_db
def test_register_user_(client):
    data = {'username': 'potter_harry',
            'first_name': 'Harry',
            'last_name': 'Mayer',
            'password1': 'Password1476',
            'password2': 'Password1476',
            }
    response = client.post(reverse('accounts:create-user'), data)
    count_users = User.objects.all().count()

    cont_profile = Profile.objects.all().count()

    assert response.status_code == 302
    assert count_users == 1
    assert cont_profile == 1
    assert response['Location'] == '/profile/1/'
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Thanks for registering. You are now logged in."


@pytest.mark.django_db
def test_login_user(client, user):
    response_get = client.get(reverse('accounts:login'))
    response_post = client.post(reverse('accounts:login'), data={'username': 'User1', 'password': 'Password1476'})

    assert response_get.status_code == 200
    assert response_post.status_code == 302
    assert response_post['Location'] == reverse('home')

# @pytest.mark.django_db
# def test_profile_view(client, user):
#     response_get = client.post(reverse('accounts:profile', kwargs={'user_pk': user.pk}), data={})

#     assert response_get.status_code == 200


@pytest.mark.django_db
def test_logout_user(client,user,):
    client.force_login(user)
    response = client.post(reverse('accounts:logout'))

    assert response.status_code == 302
    assert response['Location'] == reverse('accounts:login')