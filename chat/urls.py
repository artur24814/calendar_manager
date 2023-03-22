
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('<str:room_name>/', views.open_room_view, name='chat-room'),
    path('create/<str:username>/', views.create_room_view, name='create-room'),
    path('create-group/company-chat/', views.create_group_company_chat, name='create-company-group-room'),
]