from django.db import models
from users.models import User
from foods.models import Food


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PREPARING', 'Preparing'),
        ('SHIPPING', 'Shipping'),
        ('DELIVERED', 'Delivered'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_time = models.IntegerField()  # minutda
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders_order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'orders_orderitem'
