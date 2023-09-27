import telebot
from config import keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def help_or_start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите три параметра через пробел:\n\
\nКоличество конвертируемой валюты -- Её название  -- Валюта, в которую необходимо перевести\n\
\nP.S. Название валюты следует вводить в единственном числе с большой буквы.\n\
\n(Например: 1 Доллар Рубль)\n\nЧтобы увидеть список доступных валют нажмите: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        amount, quote, base = values
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {keys[quote]} = {total_base} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()