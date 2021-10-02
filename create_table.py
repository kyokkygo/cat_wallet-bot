
def create(sheet):

    wrk_intro = sheet.get_worksheet(0)
    wrk_intro.update_title("CAT_WALLET")
    wrk_balance = sheet.add_worksheet(title="Баланс", rows="1000", cols="13")
    wrk_income = sheet.add_worksheet(title="Доходы", rows="1000", cols="5")
    wrk_expenses = sheet.add_worksheet(title="Расходы", rows="1000", cols="6")
    wrk_category = sheet.add_worksheet(title="Категории", rows="100", cols="2")

    wrk_balance.update('A1:B8', [[None, None], ['СЧЕТ', 'СУММА'], ['БАНК 1 Карта', None],
                                 ['БАНК 2 Карта', None], ['Накопительный счет', None], ['Наличные', None],
                                 [None, None], ['ВСЕГО', '=СУММ(B3:B6)']])
    wrk_income('A1:D1', [['ID', 'Дата', 'Категория', 'Сумма']])
    wrk_expenses('A1:E1', [['ID', 'Дата', 'Категория', 'Сумма', 'Комментарий']])
    wrk_category('A1:B1', [['Доходы', 'Расходы']])

    wrk_balance.format("A1:B1", {
      "backgroundColor": {
        "red": 79.0,
        "green": 121.0,
        "blue": 66.0
      },
      "horizontalAlignment": "CENTER",
      "textFormat": {"bold": True}
    })

    wrk_balance.format("A8:B8", {
        "backgroundColor": {
            "red": 79.0,
            "green": 121.0,
            "blue": 66.0
        },
        "textFormat": {"bold": True}
    })

    wrk_income("A1:D1", {
        "backgroundColor": {
            "red": 0.56,
            "green": 0.93,
            "blue": 0.56
        },
        "horizontalAlignment": "CENTER",
        "textFormat": {"bold": True}
    })

    wrk_expenses("A1:E1", {
        "backgroundColor": {
            "red": 0.56,
            "green": 0.93,
            "blue": 0.56
        },
        "horizontalAlignment": "CENTER",
        "textFormat": {"bold": True}
    })
