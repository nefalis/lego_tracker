from django.db import models
from django.contrib.auth.models import User
from .rebrickable_api import get_lego_set_price

class LegoSet(models.Model):
    name = models.CharField(max_length=255)
    lego_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def update_price(self):
        """Met à jour le prix du set via Rebrickable API."""
        price_data = get_lego_set_price(self.lego_id)
        if "new" in price_data:
            self.price = price_data["new"]["avg_price"]
            self.save()
