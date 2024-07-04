from django.urls import path
from . import views

app_name = 'Customers'

urlpatterns = [
    path('customer_page/', views.customerpage , name='customer_page'),
    path('product/<int:product_id>/action/', views.handle_product_action , name='handle_product_action'),
    path('orderhistory/', views.orderhistory , name='order'),
    path('confirm_orders/', views.confirm_order , name='confirm_order'),
    path('address/', views.address , name='address'),
    path('checkout/', views.checkout , name='checkout'),
    path('cart/', views.cart , name='cart'),
]