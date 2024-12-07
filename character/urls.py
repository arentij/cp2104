from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('data/<str:short_name>/', views.character_page, name='character_page'),
    path('list/', views.character_list, name='character_list'),
    path('toc/', views.toc, name='toc'),
]