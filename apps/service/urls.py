from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('branches/', views.branches_view, name='branches'),
    path('complain/', views.complain_view, name='complain'),
    path('brands/', views.brands_view, name='brands'),
]
