from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests
from time import sleep
from .models import CurrencyRate

class GetCurrencyView(View):
    """
    Класс GetCurrencyView представляет собой Django View для получения актуального курса доллара к рублю
    и отображения последних 10 курсов в формате JSON.

    Attributes:
        csrf_exempt: Декоратор для отключения проверки CSRF токена.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Переопределение метода dispatch для применения декоратора csrf_exempt к представлению.
        """
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        """
        Обработка HTTP GET запроса. Получает актуальный курс доллара к рублю, сохраняет его в базе данных
        и возвращает JSON с актуальным курсом и последними 10 курсами.

        Returns:
            JsonResponse: JSON-ответ с актуальным курсом и последними 10 курсами.

        Raises:
            JsonResponse: JSON-ответ с ошибкой, если не удалось получить данные о курсе.
        """
        # API endpoint для получения курса доллара к рублю
        api_url = "https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=b37fa00e5f99931bdb15bb0bf6fa47b1"

        response = requests.get(api_url)

        if response.status_code == 200:
            currency_data = response.json()
            usd_to_rub_rate = currency_data.get("data")

            CurrencyRate.objects.create(usd_to_rub_rate=usd_to_rub_rate)

            last_10_rates = list(
                CurrencyRate.objects.values('timestamp', 'usd_to_rub_rate')
                .order_by('-timestamp')[:10]
            )

            response_data = {
                "current_usd_to_rub_rate": usd_to_rub_rate,
                "last_10_rates": last_10_rates,
            }

            # Пауза между запросами (минимум 10 секунд)
            sleep(10)

            return JsonResponse(response_data, json_dumps_params={'indent': 2})

        return JsonResponse({"error": "Failed to fetch currency data"}, status=500)
