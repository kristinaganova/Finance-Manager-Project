import requests
from decimal import Decimal, ROUND_HALF_UP

class CurrencyConverter:
    def __init__(self):
        self.currency_rates = self.get_currency_rates()

    def get_currency_rates(self):
        api_key = '7edb3c119956489cec150606' 
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {k: Decimal(v) for k, v in data['conversion_rates'].items()}
        else:
            print("Error fetching currency rates")
            return {'USD': Decimal('1.0')}  

    def convert_currency(self, amount, from_currency, to_currency):
        if isinstance(amount, (float, int, str)):
            amount = Decimal(str(amount))
        if from_currency == to_currency:
            return self.round_to_two_decimal(amount)
        rate = self.currency_rates.get(to_currency, Decimal('1.0')) / self.currency_rates.get(from_currency, Decimal('1.0'))
        converted_amount = amount * rate
        return self.round_to_two_decimal(converted_amount)

    def round_to_two_decimal(self, amount):
        return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
