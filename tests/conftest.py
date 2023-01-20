import pytest
from django.test import Client
from django.contrib.auth.models import User
from calendar_manager.models import (
    Day, Meetings
)
import datetime
from django.utils.timezone import get_current_timezone
from datetime import timedelta

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
def login_user(user, client):
    login_user = client.post('/login/', data={'username': 'User1', 'password': 'Password1476'})
    return login_user

@pytest.fixture
def login_user2(user2, client):
    login_user = client.post('/login/', data={'username': 'User2', 'password': 'Password14767'})
    return login_user