from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/', views.cart_add, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
    path('remove/', views.cart_remove, name='cart_remove'),
    path('coupon/apply/', views.apply_coupon_view, name='apply_coupon'),
    path('coupon/remove/', views.remove_coupon_view, name='remove_coupon'),
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/toggle/', views.wishlist_toggle, name='wishlist_toggle'),
    path('wishlist/to-cart/<int:product_id>/', views.wishlist_to_cart, name='wishlist_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
]
