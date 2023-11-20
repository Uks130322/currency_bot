import telebot
import requests
import json
from config import API_KEY, CURRENCY_LIST


class UserException(Exception):
    pass


class Currency:

    """Recognize the currency, add its code and print in suitable case"""

    def __init__(self, name: str) -> None:
        name = name.lower()
        if name in CURRENCY_LIST:
            self.name = name
            self.code = CURRENCY_LIST[self.name]
        elif name[:4] == "долл" and len(name) <= 8:
            self.name = "доллар"
            self.code = CURRENCY_LIST[self.name]
        elif name[:3] == "руб" and len(name) <= 7:
            self.name = "рубль"
            self.code = CURRENCY_LIST[self.name]
        else:
            raise UserException(f"Не удалось обработать валюту {name}")

    def print_for_quantity(self, quantity: float) -> str:
        """Return suitable case of currency according to quantity"""
        num = int(quantity)
        if self.name == "евро":
            return self.name
        elif self.name == "доллар":
            if (10 <= num % 100 <= 20
                    or 5 <= num % 10 <= 9
                    or num % 10 == 0):
                return "долларов"
            elif num % 10 == 1:
                return self.name
            else:
                return "доллара"

        elif self.name == "рубль":
            if (10 <= num % 100 <= 20
                    or 5 <= num % 10 <= 9
                    or num % 10 == 0):
                return "рублей"
            elif num % 10 == 1:
                return self.name
            else:
                return "рубля"


class CurrencyConversion:

    @staticmethod
    def get_args(message: telebot.types.Message) -> tuple:
        """
        Split user message to quote, base and amount
        if message format is correct, else raise exceptions
        """
        data_to_convert = message.text.split()
        if len(data_to_convert) < 3:
            raise UserException("Недостаточно параметров")
        if len(data_to_convert) > 3:
            raise UserException("Слишком много параметров")

        quote, base, amount = data_to_convert
        quote = Currency(quote)
        base = Currency(base)

        try:
            amount = float(amount)
            int(amount)
        except ValueError:
            raise UserException(f"Не удалось обработать количество {amount}")

        if quote.name == base.name:
            raise UserException(f"Одинаковые валюты.\n"
                                f"{amount} {quote.print_for_quantity(amount)} = "
                                f"{amount} {base.print_for_quantity(amount)}")

        return quote, base, amount

    """"""

    @staticmethod
    def get_exchange_rates(quote: Currency, base: Currency) -> float:
        """
        Make a request to API and get current exchange rates
        Example of JSON DATA:
        {
            "success": true,
            "timestamp": 1700080083,
            "base": "EUR",
            "date": "2023-11-15",
            "rates": {
                "RUB": 97.010666
            }
        }
        """
        r = requests.get(f"https://api.apilayer.com/fixer/latest?"
                         f"base={quote.code}&symbols={base.code}&apikey=" + API_KEY)
        json_data = json.loads(r.content)
        rate = list(json_data["rates"].values())[0]
        return rate
