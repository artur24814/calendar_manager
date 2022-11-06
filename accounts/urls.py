from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    ProfileView,
)

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='create-user'),
    path('profile/<int:user_pk>/', ProfileView.as_view(), name='profile')
]