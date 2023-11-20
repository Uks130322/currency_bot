"""
Telegram-bot for currency conversion, USD, EUR and RUB.
t.me/CurrencyConversionMyBot
"""


import telebot
from config import TOKEN, CURRENCY_LIST
from extensions import UserException, CurrencyConversion


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def show_help(message: telebot.types.Message) -> None:
    """Show information and required input format"""
    answer = "Введите начальную валюту, валюту для перевода и количество первой валюты,\n" \
             "например: 'доллар рубль 100' - перевести 100 долларов в рубли.\n" \
             "Для информации введите /help или /start, чтобы посмотреть доступные \n" \
             "валюты введите /values"
    bot.reply_to(message, answer)


@bot.message_handler(commands=["values"])
def show_values(message: telebot.types.Message) -> None:
    """Show the list of supported currencies, the list is in config.py"""
    answer = "Доступные валюты: "
    for key in CURRENCY_LIST.keys():
        answer = "\n".join((answer, key))
    bot.reply_to(message, answer)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message) -> None:
    """
    Processes the message from user, convert currency and send the answer.
    Show error with description if something goes wrong
    """
    try:
        quote, base, amount = CurrencyConversion.get_args(message)

        rate = CurrencyConversion.get_exchange_rates(quote, base)
    except UserException as error:
        bot.reply_to(message, error)
    except Exception as error:
        bot.reply_to(message, f"Не удалось выполнить команду\n{error}")
    else:
        quantity = round(float(rate) * float(amount), 2)
        answer = f"{amount} {quote.print_for_quantity(amount)} = " \
                 f"{quantity} {base.print_for_quantity(quantity)}"
        bot.reply_to(message, answer)


bot.polling()
