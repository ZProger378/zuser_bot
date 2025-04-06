from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def main_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("Профиль")
    btn2 = KeyboardButton("Тест ИИ-функций")
    btn3 = KeyboardButton("Скачать логи")
    markup.add(btn1)
    markup.add(btn2, btn3)

    return markup

