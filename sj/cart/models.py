from django.db import models
from django.core.validators import MinValueValidator


class Cart(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_cart')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ['product', 'user']