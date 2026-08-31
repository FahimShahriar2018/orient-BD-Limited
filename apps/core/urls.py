from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/search/', views.search_api, name='search_api'),
    path('api/districts/', views.districts_api, name='districts_api'),
    path('api/cart-data/', views.cart_drawer_api, name='cart_drawer_api'),
]
