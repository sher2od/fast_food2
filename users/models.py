from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WAITER = 'waiter', 'Ofitsiant'
        CUSTOMER = 'customer', 'Mijoz'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    class Meta:
        db_table = 'users_user'
