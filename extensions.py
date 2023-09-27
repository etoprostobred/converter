import requests
import json
from config import keys


class APIException(Exception):
    pass

class Converter():
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}".')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось определить валюту "{quote}".')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось определить валюту "{base}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось определить количество "{amount}".')

        r = requests.get(f'https://api.coingate.com/v2/rates/merchant/{quote_ticker}/{base_ticker}')
        total_base = json.loads(r.content)
        return total_base * amount