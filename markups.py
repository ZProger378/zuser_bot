from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def main_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("Профиль 👤")
    btn2 = KeyboardButton("Тест ИИ-функций 🟢")
    btn3 = KeyboardButton("Скачать логи 📑")
    btn4 = KeyboardButton("Настройки ⚙️")
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)

    return markup

def settings_markup(settings):
    markup = InlineKeyboardMarkup(row_width=2)
    if settings['animation']['laughter']:
        btn1 = InlineKeyboardButton("Анимация смеха (ВКЛ ✅)", callback_data="settings_laughter")
    else:
        btn1 = InlineKeyboardButton("Анимация смеха (ВЫКЛ ❌)", callback_data="settings_laughter")

    btn2 = InlineKeyboardButton("Изменить модель для text2text", callback_data="edit_model_1")
    btn3 = InlineKeyboardButton("Изменить модель для img2text", callback_data="edit_model_2")

    btn4 = InlineKeyboardButton("Анимированные слова", callback_data="animated_words")

    markup.add(btn1, btn4)
    markup.add(btn2)
    markup.add(btn3)

    return markup


def words_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("Удалить слово 🗑", callback_data="delete_words")
    btn2 = InlineKeyboardButton("Добавить слово ➕", callback_data="add_words")
    btn3 = InlineKeyboardButton("Вернуться ↩️", callback_data="settings")
    markup.add(btn1, btn2, btn3)

    return markup

def to_settings_markup():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Вернуться ↩️", callback_data="settings")
    markup.add(btn1)

    return markup

def delete_words_markup(words):
    markup = InlineKeyboardMarkup(row_width=1)
    for word in words:
        btn = InlineKeyboardButton(word, callback_data=f"delete_{word}")
        markup.add(btn)
    btn1 = InlineKeyboardButton("Вернуться ↩️", callback_data="settings")
    markup.add(btn1)

    return markup
    
def edit_model_markup(models, model):
    markup = InlineKeyboardMarkup(row_width=1)
    for i in models['all']:
        btn = InlineKeyboardButton(f"{i} {'✅' if i == models[model] else ''}", callback_data=f"{model}_{i}")
        markup.add(btn)
    btn1 = InlineKeyboardButton("Вернуться ↩️", callback_data="settings")
    markup.add(btn1)

    return markup

