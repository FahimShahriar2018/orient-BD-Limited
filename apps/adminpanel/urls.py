from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    # Products CRUD
    path('products/', views.product_list_view, name='products'),
    path('products/create/', views.product_create_view, name='product_create'),
    path('products/edit/<int:product_id>/', views.product_edit_view, name='product_edit'),
    path('products/delete/<int:product_id>/', views.product_delete_view, name='product_delete'),
    # Orders Pipeline
    path('orders/', views.order_list_view, name='orders'),
    path('orders/detail/<str:tracking_number>/', views.order_detail_view, name='order_detail'),
    path('orders/advance/<str:tracking_number>/', views.order_advance_status_view, name='order_advance'),
    # Customers
    path('customers/', views.customer_list_view, name='customers'),
]
