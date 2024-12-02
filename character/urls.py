from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('character/<int:character_id>/', views.character_page, name='character_page'),
    path('toc/', views.toc, name='toc'),
]