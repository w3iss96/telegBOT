import requests
import json


class APIException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float, api_url):
        try:
            response = requests.get(f"{api_url}{base}")
            response.raise_for_status()
            data = response.json()

            if quote not in data['rates']:
                raise APIException(f"Валюта {quote} не найдена")

            rate = data['rates'][quote]
            total = amount * rate
            return total

        except requests.exceptions.RequestException:
            raise APIException("Ошибка при получении данных")
        except json.JSONDecodeError:
            raise APIException("Ошибка при парсинге данных")
        except KeyError:
            raise APIException("Ошибка в данных API")