from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('palpite/<int:partida_id>/', views.dar_palpite, name='dar_palpite'),
    path('ranking/', views.ranking, name='ranking'),
    path('registrar/', views.registrar, name='registrar'),
]