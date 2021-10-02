import gspread
import telebot
from datetime import date
from create_table import create


bot = telebot.TeleBot('')
gc = gspread.service_account("")


@bot.message_handler(commands=['help'])
def com_help(message):
    bot.send_message(message.chat.id, 'Запустить бота "/start"'
                                      '\nУзнать баланс - "/balance"'
                                      '\nЗаписать расходы - категория сумма комментарий'
                                      '\nЗаписать доходы - категория сумма комментарий')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Мяу, привет! Рад тебя видеть! '
                                      'Пожалуйста, пришли мне свою гугл почту, '
                                      'чтобы я смог привязать таблицу к твоему аккаунту с:')
    bot.register_next_step_handler(message, get_mail)


def get_mail(message):
    user_id = message.from_user.id
    user_mail = message.text
    sheet = gc.open("Тест бот")
    all_users_sheet = sheet.worksheet("Пользователи")
    next_row = next_available_row(all_users_sheet)

    if not all_users_sheet.find(user_mail):
        sh = gc.create('Мой бюджет от cat_wallet')
        sh.share(user_mail, perm_type='user', role='writer')
        url = 'https://docs.google.com/spreadsheets/d/%s' % sh.id
        create(sh)
        bot.send_message(message.chat.id, 'Таблица готова и доступна по адресу: '
                                          '{}'.format(url))

        all_users_sheet.update('A{}:D{}'.format(next_row, next_row),
                               [[str(date.today()), str(user_id), user_mail, url]])

    else:
        cell = all_users_sheet.find(user_mail)
        bot.send_message(message.chat.id, 'У вас уже есть таблица: {}'.format
                                          (all_users_sheet.acell('D{}'.format(cell.row)).value))


@bot.message_handler(commands=['balance'])
def balance(message):
    sheet = open_sheet(message.from_user.id)

    wrk = sheet.worksheet("Баланс")
    list_of_lists = wrk.get_all_values()
    bot.send_message(message.chat.id, 'Ваш баланс: {}'.format(list_of_lists))


@bot.message_handler(content_types=['text'])
def add(message):
    val = message.text.capitalize().split()
    sheet = open_sheet(message.from_user.id)

    wrk_expenses = sheet.worksheet("Расходы")
    wrk_income = sheet.worksheet("Доходы")
    wrk_category = sheet.worksheet("Категории")
    category_exp = wrk_category.col_values(1)
    category_in = wrk_category.col_values(2)

    if val[0] in category_exp:

        next_row = next_available_row(wrk_expenses)

        wrk_expenses.update('A{}:E{}'.format(next_row, next_row),
                            [[str(int(next_row) - 1), str(date.today()), val[0], int(val[1]), val[2]]])

        bot.send_message(message.chat.id, 'Записано в расходы!')

    elif val[0] in category_in:
        next_row = next_available_row(wrk_income)

        wrk_income.update('A{}:D{}'.format(next_row, next_row),
                          [[str(int(next_row) - 1), str(date.today()), val[0], int(val[1])]])

        bot.send_message(message.chat.id, 'Записано в доходы!')

    else:
        bot.send_message(message.chat.id, 'Не удается распознать текст.'
                                          '\nВведите: категория сумма комментарий c:')


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


def open_sheet(user_id):
    sheet = gc.open("Тест бот")
    all_users_sheet = sheet.worksheet("Пользователи")
    cell = all_users_sheet.find(str(user_id))
    url = all_users_sheet.acell('D{}'.format(cell.row)).value
    return gc.open_by_url(url)


def find_category(user_id):
    pass


if __name__ == "__main__":
    bot.polling()
