from django.urls import path
from . import views

urlpatterns = [
    path('character/<int:character_id>/', views.character_page, name='character_page'),
]