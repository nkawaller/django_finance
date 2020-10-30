from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history', views.history, name='history'),
    path('quote/', views.quote, name='quote'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
]