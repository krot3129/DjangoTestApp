from django.test import TestCase
from django.urls import reverse
from .models import CurrencyRate
from datetime import datetime, timedelta

class GetCurrencyViewTest(TestCase):
    def test_get_currency_view(self):

        timestamp = datetime.now()

        CurrencyRate.objects.create(usd_to_rub_rate="65.0", timestamp=timestamp)

        # Создаем запрос к представлению
        response = self.client.get(reverse('get_currency'))

        # Проверяем успешность ответа
        self.assertEqual(response.status_code, 200)

        self.assertIn('last_10_rates', response.json())


