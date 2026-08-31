from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('brands/', views.brand_list_view, name='brand_list'),
    path('brand/<slug:slug>/', views.brand_detail_view, name='brand_detail'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('product/<slug:slug>/review/', views.submit_review_view, name='submit_review'),
]

