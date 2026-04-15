from django.urls import path
from .views import food_list, create_food, update_food, delete_food, create_category

urlpatterns = [
    path('list/', food_list, name='food_list'),
    path('create/', create_food, name='create_food'),
    path('update/<int:pk>/', update_food, name='update_food'),
    path('delete/<int:pk>/', delete_food, name='delete_food'),
    path('category/create/', create_category, name='create_category'),
]
