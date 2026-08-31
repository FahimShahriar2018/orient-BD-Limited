from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order_view, name='place_order'),
    path('confirmation/<str:tracking_number>/', views.order_confirmation_view, name='order_confirmation'),
    path('track/', views.public_track_order_view, name='track_order'),
    path('history/', views.order_history_view, name='order_history'),
    path('detail/<str:tracking_number>/', views.order_detail_view, name='order_detail'),
    path('invoice/<str:tracking_number>/', views.print_invoice_view, name='print_invoice'),
]
