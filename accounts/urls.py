from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    ProfileView,
    #HTMX
    valid_password,
    check_existing_name
)

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView.as_view(), name='create-user'),
    path('profile/<int:user_pk>/', ProfileView.as_view(), name='profile'),
    #HTMX
    path('valid-password/', valid_password, name='valid-password'),
    path('check-existing-name/', check_existing_name, name='check-existing-name'),
]