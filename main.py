import telebot
from extensions import Converter, APIException
import config

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = "Привет! Я валютный бот.\n" \
           "Чтобы узнать курс, отправьте сообщение в формате:\n" \
           "<валюта> <в какую валюту конвертировать> <количество>\n" \
           "Например: USD RUB 100"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\n" \
           "USD - Доллар США\n" \
           "EUR - Евро\n" \
           "RUB - Российский рубль"
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def convert(message):
    try:
        values = message.text.upper().split()

        if len(values) != 3:
            raise APIException("Неверное количество параметров")

        base, quote, amount = values
        amount = float(amount)

        # Передаем API_URL в метод get_price
        result = Converter.get_price(base, quote, amount, config.API_URL)

        text = f"{amount} {base} = {result:.2f} {quote}"
        bot.reply_to(message, text)

    except APIException as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")
    except ValueError:
        bot.reply_to(message, "Ошибка: Неверное число")
    except Exception as e:
        bot.reply_to(message, f"Произошла непредвиденная ошибка: {str(e)}")


if __name__ == '__main__':
    bot.polling(none_stop=True)