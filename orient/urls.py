from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.catalog import views as catalog_views

urlpatterns = [
    # Built-in Django Admin (at /django-admin/ to avoid conflicting with custom /admin-panel/)
    path('django-admin/', admin.site.urls),
    
    # Custom Administrative Back-Office Console (Module 9)
    path('admin-panel/', include('apps.adminpanel.urls', namespace='adminpanel')),
    
    # Customer Account & Auth (Module 8)
    path('account/', include('apps.accounts.urls', namespace='accounts')),
    
    # Product Catalog & Exploration (Module 3 & 4)
    path('shop/', include('apps.catalog.urls', namespace='catalog')),
    
    # Direct Root Brand Directory Routes (matches live site URL structure /brand/ and /brand/<slug>/)
    path('brand/', catalog_views.brand_list_view, name='brand_root_list'),
    path('brand/<slug:slug>/', catalog_views.brand_detail_view, name='brand_root_detail'),
    path('brands/', catalog_views.brand_list_view, name='brands_root_alias'),

    # Cart & Wishlist (Module 5)
    path('cart/', include('apps.cart.urls', namespace='cart')),
    
    # Checkout & Orders (Module 6 & 7)
    path('checkout/', include('apps.orders.urls', namespace='orders')),
    
    # Customer Service, Branches, Warranty Complaints (Module 10)
    path('service/', include('apps.service.urls', namespace='service')),
    
    # Storefront Homepage, Live Search & APIs (Module 1 & 2)
    path('', include('apps.core.urls', namespace='core')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
