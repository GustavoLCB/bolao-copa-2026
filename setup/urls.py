from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('palpite/<int:partida_id>/', views.dar_palpite, name='dar_palpite'),
    path('ranking/', views.ranking, name='ranking'),
    path('contas/', include('django.contrib.auth.urls')),
    path('regras/', views.regras, name='regras'),
]