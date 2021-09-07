
def create(sheet):

    wrk1 = sheet.get_worksheet(0)
    wrk1.update_title("Баланс")
    wrk2 = sheet.add_worksheet(title="Доходы", rows="1000", cols="4")
    wrk3 = sheet.add_worksheet(title="Расходы", rows="1000", cols="5")

    wrk1.update('A1:B3', [['Счет', 'Сумма'], ['Карта', None], ['Наличные', None]])
    wrk2.update('A1:D1', [['ID', 'Дата', 'Категория', 'Сумма']])
    wrk3.update('A1:E1', [['ID', 'Дата', 'Категория', 'Сумма', 'Комментарий']])

    wrk1.format("A1:B1", {
      "backgroundColor": {
        "red": 0.56,
        "green": 0.93,
        "blue": 0.56
      },
      "horizontalAlignment": "CENTER",
      "textFormat": {"bold": True}
    })

    wrk2.format("A1:D1", {
        "backgroundColor": {
            "red": 0.56,
            "green": 0.93,
            "blue": 0.56
        },
        "horizontalAlignment": "CENTER",
        "textFormat": {"bold": True}
    })

    wrk3.format("A1:E1", {
        "backgroundColor": {
            "red": 0.56,
            "green": 0.93,
            "blue": 0.56
        },
        "horizontalAlignment": "CENTER",
        "textFormat": {"bold": True}
    })

    return wrk1, wrk2, wrk3
