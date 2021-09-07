import gspread
import telebot
from datetime import date
from create_table import create


bot = telebot.TeleBot('')
gc = gspread.service_account("")


@bot.message_handler(commands=['начать'])
def start(message):
    bot.send_message(message.chat.id, 'Мяу, привет! Рад тебя видеть! '
                                      'Пожалуйста, пришли мне свою гугл почту, '
                                      'чтобы я смог привязать таблицу к твоему аккаунту с:')
    bot.register_next_step_handler(message, get_mail)


# @bot.message_handler(content_types=['text'])
def get_mail(message):
    key = message.from_user.id
    val = message.text
    sheet = gc.open("Тест бот")
    worksheet = sheet.worksheet("Пользователи")
    next_row = next_available_row(worksheet)

    if not worksheet.find(val):
        sh = gc.create('Мой бюджет от cat_wallet')
        sh.share(val, perm_type='user', role='writer')
        url = 'https://docs.google.com/spreadsheets/d/%s' % sh.id
        create(sh)
        bot.send_message(message.chat.id, 'Таблица готова и доступна по адресу: '
                                          '{}'.format(url))

        worksheet.update('A{}'.format(next_row), str(date.today()))
        worksheet.update('B{}'.format(next_row), str(key))
        worksheet.update('C{}'.format(next_row), val)
        worksheet.update('D{}'.format(next_row), url)
    else:
        cell = worksheet.find(val)
        bot.send_message(message.chat.id, 'У вас уже есть таблица: {}'.format
                                          (worksheet.acell('D{}'.format(cell.row)).value))


@bot.message_handler(content_types=['text'])
def add(message):
    key = message.from_user.id
    val = message.text.capitalize().split()
    sheet = gc.open("Тест бот")
    worksheet = sheet.worksheet("Пользователи")
    cell = worksheet.find(str(key))
    url = worksheet.acell('D{}'.format(cell.row)).value
    sheet = gc.open_by_url(url)

    wrk3 = sheet.worksheet("Расходы")
    wrk2 = sheet.worksheet("Доходы")
    category_exp = wrk3.col_values(3)
    category_in = wrk2.col_values(3)

    if val[0] in category_exp:
        next_row = next_available_row(wrk3)

        wrk3.update('A{}'.format(next_row), str(int(next_row) - 1))
        wrk3.update('B{}'.format(next_row), str(date.today()))
        wrk3.update('C{}'.format(next_row), val[0])
        wrk3.update('D{}'.format(next_row), val[1])
        wrk3.update('E{}'.format(next_row), val[2])

        bot.send_message(message.chat.id, 'Записано в расходы!')

    elif val[0] in category_in:
        next_row = next_available_row(wrk2)

        wrk2.update('A{}'.format(next_row), str(int(next_row) - 1))
        wrk2.update('B{}'.format(next_row), str(date.today()))
        wrk2.update('C{}'.format(next_row), val[0])
        wrk2.update('D{}'.format(next_row), int(val[1]))
        bot.send_message(message.chat.id, 'Записано в доходы!')

    else:
        bot.send_message(message.chat.id, 'Не удается распознать текст.'
                                          '\nВведите: категория сумма комментарий c:')


@bot.message_handler(commands=['help'])
def command_help(message):
    pass


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


if __name__ == "__main__":
    bot.polling()
