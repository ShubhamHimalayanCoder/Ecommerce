from django.urls import path
from . import views

app_name = 'Seller'

urlpatterns = [
    path('admin_dashboard/', views.admin , name='admin_dashboard'),
    path('add_product/', views.product_add , name='add_product'),

]

