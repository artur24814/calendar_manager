import pytest
from django.test import Client
from django.contrib.auth.models import User
from calendar_manager.models import (
    Day, Meetings
)
from django.conf import settings


# Issue with file storage
@pytest.fixture
def in_memory():
    settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    user = User.objects.create_user(username='User1', first_name='Harry', last_name='Mayer',
                                    email='User1@example.com', password='Password1476')
    return user

@pytest.fixture
def user2():
    user = User.objects.create_user(username='User2', first_name='Harry', last_name='Potter',
                                    email='User2@example.com', password='Password14767')
    return user

@pytest.fixture
def user3():
    user = User.objects.create_user(username='User3', first_name='Jon', last_name='Malkowicz',
                                    email='User3@example.com', password='Password14767')
    return user

@pytest.fixture
def login_user(user, client):
    login_user = client.post('/login/', data={'username': 'User1', 'password': 'Password1476'})
    return login_user

@pytest.fixture
def login_user2(user2, client):
    login_user = client.post('/login/', data={'username': 'User2', 'password': 'Password14767'})
    return login_user

@pytest.fixture
def user_with_folows(user, user2, user3, client):
    user.profile.follows.add(user2.profile)
    user.profile.follows.add(user3.profile)
    return user


