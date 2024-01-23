from django.db import models

class CurrencyRate(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    usd_to_rub_rate = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.timestamp}: {self.usd_to_rub_rate}\n"
