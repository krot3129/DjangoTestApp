from django.urls import path
from currency_app.views import GetCurrencyView

urlpatterns = [
    path('get-current-usd/', GetCurrencyView.as_view(), name='get_currency'),
]