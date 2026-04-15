from django.urls import path
from .views import create_order, order_list, update_order_status

urlpatterns = [
    path('list/', order_list, name='order_list'),
    path('create/', create_order, name='create_order'),
    path('status/update/<int:pk>/', update_order_status, name='update_order_status'),
]
